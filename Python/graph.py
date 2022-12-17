from typing import NamedTuple
import network as nx
from queues import Queue
from collections import deque
from queues import Queue, Stack
from math import inf as infinity
from queues import MutableMinHeap, Queue, Stack


class City(NamedTuple):
    name: str
    country: str
    year: int | None
    latitude: float
    longitude: float

    @classmethod
    def from_dict(cls, attrs):
        return cls(
            name=attrs["xlabel"],
            country=attrs["country"],
            year=int(attrs["year"]) or None,
            latitude=float(attrs["latitude"]),
            longitude=float(attrs["longitude"])
        )


def load_graph(filename, node_factory):
    graph = nx.nx_agraph.read_dot(filename)
    nodes = {
        name: node_factory(attributes)
        for name, attributes in graph.nodes(data=True)
    }
    return nodes, nx.Graph(
        (nodes[name1], nodes[name2], weights)
        for name1, name2, weights in graph.edges(data=True)
    )


def breadth_first_traverse(graph, source):
    queue = Queue(source)
    visited = {source}
    for node in queue:
        yield node
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.enqueue(neighbor)


def breadth_first_search(graph, source, predicate):
    return search(breadth_first_traverse, graph, source, predicate, order_by)


def shortest_path(graph, source, destination, order_by=None):
    queue = Queue(source)
    visited = {source}
    previous = {}
    while queue:
        node = queue.dequeue()
        neighbors = list(graph.neighbors(node))
        if order_by:
            neighbors.sort(key=order_by)
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.enqueue(neighbor)
                previous[neighbor] = node
                if neighbor == destination:
                    return retrace(previous, source, destination)


def retrace(previous, source, destination):
    path = deque()

    current = destination
    while current!= source:
        path.appendleft(current)
        current = previous.get(current)
        if current is None:
            return None

    path.appendleft(source)
    return list(path)


def connected(graph, source, destination):
    return shortest_path(graph, source, destination) is not None


def recursive_depth_first_traverse(graph, source, order_by=None):
    visited = set()

    def visited(node):

        yield node
        visited.add(node)
        neighbors = list(graph.neighbors(node))
        if order_by:
            neighbors.sort(key=order_by)
        for neighbor in reversed(neighbors):
            if neighbor not in visited:
                yield from visit(neighbor)

    return visit(source)


def depth_first_search(graph, source, predicate, order_by=None):
    return search(recursive_depth_first_traverse, graph, source, predicate, order_by)


def search(traverse, graph, source, predicate, order_by=None):
    for node in traverse(graph, source, order_by):
        if predicate(node):
            return node
