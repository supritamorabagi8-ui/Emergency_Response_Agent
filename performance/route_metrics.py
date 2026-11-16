import time

from algorithms.bfs import bfs
from algorithms.astar import astar
from environment.campus_graph import CAMPUS_GRAPH
from performance.performance import calculate_score


def calculate_route_cost(graph, path, crowded_locations=None):
    """Calculate the total weighted cost of a route."""

    if not path:
        return 0

    crowded_locations = crowded_locations or []
    total_cost = 0

    for current, neighbor in zip(path, path[1:]):
        cost = graph[current][neighbor]

        if neighbor in crowded_locations:
            cost += 5

        total_cost += cost

    return total_cost


def run_route_algorithm(
    algorithm_name,
    start,
    goal,
    blocked_edges=None,
    crowded_locations=None
):
    """Run BFS or A* and collect performance metrics."""

    blocked_edges = blocked_edges or []
    crowded_locations = crowded_locations or []

    start_time = time.perf_counter()

    if algorithm_name.lower() == "bfs":

        metrics = bfs(
            CAMPUS_GRAPH,
            start,
            goal,
            blocked_edges,
            return_metrics=True
        )

    elif algorithm_name.lower() in ("astar", "a*"):

        metrics = astar(
            CAMPUS_GRAPH,
            start,
            goal,
            blocked_edges,
            crowded_locations,
            return_metrics=True
        )

    else:
        raise ValueError("Algorithm must be BFS or A*.")

    execution_time_ms = (time.perf_counter() - start_time) * 1000

    route = metrics["route"]
    nodes_expanded = metrics["nodes_expanded"]

    route_cost = calculate_route_cost(
        CAMPUS_GRAPH,
        route,
        crowded_locations
    )

    result = {
        "algorithm": algorithm_name,
        "route": route,
        "goal_reached": route is not None,
        "route_valid": route is not None,
        "route_cost": route_cost,
        "execution_time_ms": execution_time_ms,
        "nodes_expanded": nodes_expanded,
        "unsafe_route": False
    }

    result["score"] = calculate_score(result)

    return result