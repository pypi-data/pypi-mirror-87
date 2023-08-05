from collections import deque
from functools import wraps
from typing import Dict, List, Callable

from ..enums import SocketType, FlowOptimizeLevel, FlowBuildLevel, PodRoleType
from ..excepts import FlowBuildLevelError
from ..peapods.pod import FlowPod

if False:
    from . import Flow


def build_required(required_level: 'FlowBuildLevel'):
    """Annotate a function so that it requires certain build level to run.

    :param required_level: required build level to run this function.

    Example:

    .. highlight:: python
    .. code-block:: python

        @build_required(FlowBuildLevel.RUNTIME)
        def foo():
            print(1)

    """

    def __build_level(func):
        @wraps(func)
        def arg_wrapper(self, *args, **kwargs):
            if hasattr(self, '_build_level'):
                if self._build_level.value >= required_level.value:
                    return func(self, *args, **kwargs)
                else:
                    raise FlowBuildLevelError(
                        f'build_level check failed for {func!r}, required level: {required_level}, actual level: {self._build_level}')
            else:
                raise AttributeError(f'{self!r} has no attribute "_build_level"')

        return arg_wrapper

    return __build_level


def _traverse_graph(op_flow: 'Flow', outgoing_map: Dict[str, List[str]],
                    func: Callable[['Flow', str, str], None]) -> 'Flow':
    _outgoing_idx = dict.fromkeys(outgoing_map.keys(), 0)
    stack = deque()
    stack.append('gateway')
    op_flow.logger.debug('Traversing dependency graph:')
    while stack:
        start_node_name = stack.pop()
        if start_node_name in _outgoing_idx:
            end_node_idx = _outgoing_idx[start_node_name]
            if end_node_idx < len(outgoing_map[start_node_name]):
                # else, you are back to the gateway
                end_node_name = outgoing_map[start_node_name][end_node_idx]
                func(op_flow, start_node_name, end_node_name)
                stack.append(end_node_name)
                if end_node_idx + 1 < len(outgoing_map[start_node_name]):
                    stack.append(start_node_name)
                _outgoing_idx[start_node_name] = end_node_idx + 1
    return op_flow


def _hanging_pods(op_flow: 'Flow') -> List[str]:
    """Return the names of hanging pods (nobody recv from them) in the flow"""
    all_needs = {v for p in op_flow._pod_nodes.values() for v in p.needs}
    all_names = {p for p in op_flow._pod_nodes.keys()}
    # all_names is always a superset of all_needs
    return list(all_names.difference(all_needs))


def _build_flow(op_flow: 'Flow', outgoing_map: Dict[str, List[str]]) -> 'Flow':
    def _build_two_connections(flow: 'Flow', start_node_name: str, end_node_name: str):
        # Rule
        # if a node has multiple income/outgoing peas,
        # then its socket_in/out must be PULL_BIND or PUB_BIND
        # otherwise it should be different than its income
        # i.e. income=BIND => this=CONNECT, income=CONNECT => this = BIND
        #
        # when a socket is BIND, then host must NOT be set, aka default host 0.0.0.0
        # host_in and host_out is only set when corresponding socket is CONNECT
        start_node = flow._pod_nodes[start_node_name]
        end_node = flow._pod_nodes[end_node_name]
        first_socket_type = SocketType.PUSH_CONNECT
        if len(outgoing_map[start_node_name]) > 1:
            first_socket_type = SocketType.PUB_BIND
        elif end_node_name == 'gateway':
            first_socket_type = SocketType.PUSH_BIND
        FlowPod.connect(start_node, end_node, first_socket_type=first_socket_type)
        flow.logger.debug(f'Connect {start_node_name} '
                          f'with {end_node_name} {str(end_node.role)} require {end_node.head_args.num_part} messages')

    return _traverse_graph(op_flow, outgoing_map, _build_two_connections)


def _optimize_flow(op_flow, outgoing_map: Dict[str, List[str]], pod_edges: {str, str}) -> 'Flow':
    def _optimize_two_connections(flow: 'Flow', start_node_name: str, end_node_name: str):
        """ THIS CODE IS NEVER TESTED AND THE LOGIC MAY NOT APPLIED ANYMORE

        :param flow:
        :param start_node_name:
        :param end_node_name:
        :return:
        """
        start_node = flow._pod_nodes[start_node_name]
        end_node = flow._pod_nodes[end_node_name]
        edges_with_same_start = [ed for ed in pod_edges if ed[0].startswith(start_node_name)]
        edges_with_same_end = [ed for ed in pod_edges if ed[1].endswith(end_node_name)]
        if len(edges_with_same_start) > 1 or len(edges_with_same_end) > 1:
            flow.logger.info(f'Connection between {start_node_name} and {end_node_name} cannot be optimized')
        else:
            if start_node.role == PodRoleType.GATEWAY:
                if flow.args.optimize_level > FlowOptimizeLevel.IGNORE_GATEWAY and end_node.is_head_router:
                    flow.logger.info(
                        f'Node {end_node_name} connects to tail of {start_node_name}')
                    end_node.connect_to_tail_of(start_node)
            elif end_node.role == PodRoleType.GATEWAY:
                # TODO: this part of the code is never executed given the current optimization level. Never tested.
                if flow.args.optimize_level > FlowOptimizeLevel.IGNORE_GATEWAY and \
                        start_node.is_tail_router and start_node.tail_args.num_part <= 1:
                    # connect gateway directly to peas only if this is unblock router
                    # as gateway can not block & reduce message
                    flow.logger.info(
                        f'Node {start_node_name} connects to head of {end_node_name}')
                    start_node.connect_to_head_of(end_node)
            else:
                if end_node.is_head_router and not start_node.is_tail_router:
                    flow.logger.info(
                        f'Node {end_node_name} connects to tail of {start_node_name}')
                    end_node.connect_to_tail_of(start_node)
                elif start_node.is_tail_router and start_node.tail_args.num_part <= 1:
                    flow.logger.info(
                        f'Node {start_node_name} connects to head of {end_node_name}')
                    start_node.connect_to_head_of(end_node)

    if op_flow.args.optimize_level > FlowOptimizeLevel.NONE:
        return _traverse_graph(op_flow, outgoing_map, _optimize_two_connections)
    else:
        return op_flow
