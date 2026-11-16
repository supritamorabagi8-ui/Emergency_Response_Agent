
import heapq
from itertools import count


def astar(
    graph,
    start,
    goal,
    blocked_edges=None,
    crowded_locations=None,
    return_metrics=False
):
    """Find the minimum-cost path using Dijkstra (A* with h=0)."""

    blocked_edges = {
        frozenset(edge) for edge in (blocked_edges or [])
    }
    crowded_locations = set(crowded_locations or [])

    if start not in graph or goal not in graph:
        result = {"route": None, "nodes_expanded": 0}
        return result if return_metrics else None

    if start == goal:
        result = {"route": [start], "nodes_expanded": 0}
        return result if return_metrics else [start]

    counter = count()

    priority_queue = [
        (0, next(counter), start, [start])
    ]

    best_cost = {start: 0}
    nodes_expanded = 0

    while priority_queue:
        cost, _, current, path = heapq.heappop(priority_queue)

        if cost > best_cost.get(current, float("inf")):
            continue

        nodes_expanded += 1

        if current == goal:
            result = {
                "route": path,
                "nodes_expanded": nodes_expanded
            }
            return result if return_metrics else path

        for neighbor, travel_cost in graph.get(current, {}).items():

            if frozenset((current, neighbor)) in blocked_edges:
                continue

            if travel_cost < 0:
                continue

            extra_cost = travel_cost

            if neighbor in crowded_locations:
                extra_cost += 5

            new_cost = cost + extra_cost

            if new_cost < best_cost.get(
                neighbor, float("inf")
            ):
                best_cost[neighbor] = new_cost

                heapq.heappush(
                    priority_queue,
                    (
                        new_cost,
                        next(counter),
                        neighbor,
                        path + [neighbor]
                    )
                )

    result = {
        "route": None,
        "nodes_expanded": nodes_expanded
    }

    return result if return_metrics else None
