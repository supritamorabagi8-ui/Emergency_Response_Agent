
from collections import deque


def bfs(graph, start, goal, blocked_edges=None, return_metrics=False):
    """Find the shortest path in number of edges using BFS."""

    blocked_edges = {
        frozenset(edge) for edge in (blocked_edges or [])
    }

    if start not in graph or goal not in graph:
        result = {"route": None, "nodes_expanded": 0}
        return result if return_metrics else None

    if start == goal:
        result = {"route": [start], "nodes_expanded": 0}
        return result if return_metrics else [start]

    queue = deque([[start]])
    visited = {start}
    nodes_expanded = 0

    while queue:
        path = queue.popleft()
        current = path[-1]
        nodes_expanded += 1

        if current == goal:
            result = {
                "route": path,
                "nodes_expanded": nodes_expanded
            }
            return result if return_metrics else path

        for neighbor in graph.get(current, {}):
            if neighbor in visited:
                continue

            if frozenset((current, neighbor)) in blocked_edges:
                continue

            visited.add(neighbor)
            queue.append(path + [neighbor])

    result = {
        "route": None,
        "nodes_expanded": nodes_expanded
    }

    return result if return_metrics else None
