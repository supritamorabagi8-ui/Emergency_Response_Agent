"""
Member 3: reproducible campus experiments and algorithm comparison.

BFS and A* are included here as small transparent benchmark implementations
so Member 3's experiment script can run independently. In the integrated
team application, replace/import these with Member 4's tested implementations
after agreeing on the same return format.

Campus IDs and connections are exactly the shared team blueprint.
"""

from collections import deque
from heapq import heappush, heappop
from math import hypot
from time import perf_counter

from performance import calculate_score, summarize_runs

GRAPH = {
    "A": ["B", "L"],
    "B": ["A", "C", "P"],
    "L": ["A", "C", "M"],
    "C": ["B", "L", "P"],
    "M": ["L", "P"],
    "P": ["B", "C", "M", "G1", "G2"],
    "G1": ["P"],
    "G2": ["P"],
}

# Coordinates are only for an admissible A* heuristic illustration.
COORDS = {
    "A": (0, 2), "B": (2, 2), "L": (0, 0), "C": (2, 0),
    "M": (0, -2), "P": (3, -1), "G1": (5, 0), "G2": (5, -2),
}

EDGE_COSTS = {}
for node, neighbors in GRAPH.items():
    for neighbor in neighbors:
        key = tuple(sorted((node, neighbor)))
        EDGE_COSTS[key] = 1.0


def edge_key(u, v):
    return tuple(sorted((u, v)))


def edge_cost(u, v, crowded_locations=()):
    # Crowd is a soft penalty. It is not automatically a blocked location.
    penalty = 2.0 if v in crowded_locations else 0.0
    return EDGE_COSTS[edge_key(u, v)] + penalty


def valid_neighbors(node, blocked_edges=(), restricted_locations=(), forbidden_locations=()):
    blocked = {edge_key(*edge) for edge in blocked_edges}
    forbidden = set(restricted_locations) | set(forbidden_locations)
    return [
        nxt for nxt in GRAPH[node]
        if edge_key(node, nxt) not in blocked and nxt not in forbidden
    ]


def bfs_search(start, goals, blocked_edges=(), restricted_locations=(), forbidden_locations=()):
    """Unweighted BFS. Returns route, nodes_expanded, route_cost."""
    goals = set(goals)
    if start in goals:
        return [start], 0, 0.0
    queue = deque([start])
    parent = {start: None}
    expanded = 0
    found = None
    while queue:
        current = queue.popleft()
        expanded += 1
        if current in goals:
            found = current
            break
        for nxt in valid_neighbors(current, blocked_edges, restricted_locations, forbidden_locations):
            if nxt not in parent:
                parent[nxt] = current
                queue.append(nxt)
    if found is None:
        return None, expanded, float("inf")
    path = []
    cur = found
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path, expanded, float(len(path) - 1)


def _heuristic(node, goals):
    # Euclidean distance is admissible here because each edge costs at least 1
    # and the coordinate distance between connected nodes is <= 1 only if scaled.
    # To guarantee admissibility for this toy graph, use 0: A* reduces to UCS.
    # This is deliberately conservative and guarantees no overestimation.
    return 0.0


def astar_search(start, goals, blocked_edges=(), restricted_locations=(),
                 forbidden_locations=(), crowded_locations=()):
    """A* with a conservative admissible h(n)=0; route cost includes crowd penalty."""
    goals = set(goals)
    if start in goals:
        return [start], 0, 0.0
    frontier = []
    heappush(frontier, (0.0, 0.0, start))
    g_cost = {start: 0.0}
    parent = {start: None}
    expanded = 0
    found = None
    while frontier:
        _, current_cost, current = heappop(frontier)
        if current_cost != g_cost.get(current):
            continue
        expanded += 1
        if current in goals:
            found = current
            break
        for nxt in valid_neighbors(current, blocked_edges, restricted_locations, forbidden_locations):
            candidate = current_cost + edge_cost(current, nxt, crowded_locations)
            if candidate < g_cost.get(nxt, float("inf")):
                g_cost[nxt] = candidate
                parent[nxt] = current
                heappush(frontier, (candidate + _heuristic(nxt, goals), candidate, nxt))
    if found is None:
        return None, expanded, float("inf")
    path = []
    cur = found
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path, expanded, g_cost[found]


def _run_one(algorithm, scenario_name, start, exits, blocked=(), crowded=(), restricted=(),
             emergency_location=None, partial_unknown_crowds=()):
    # The known fire-affected node is treated as a forbidden destination/intermediate
    # location, but the agent is allowed to start there and leave it.
    forbidden = set()
    if emergency_location and emergency_location != start:
        forbidden.add(emergency_location)

    t0 = perf_counter()
    if algorithm == "BFS":
        path, expanded, cost = bfs_search(
            start, exits, blocked, restricted, forbidden
        )
    else:
        path, expanded, cost = astar_search(
            start, exits, blocked, restricted, forbidden, crowded
        )
    elapsed_ms = (perf_counter() - t0) * 1000.0

    valid = path is not None
    goal = bool(valid and path[-1] in exits)
    unsafe = False
    if path:
        unsafe = any(
            edge_key(path[i], path[i + 1]) in {edge_key(*e) for e in blocked}
            for i in range(len(path) - 1)
        ) or any(node in restricted for node in path[1:])

    row = {
        "experiment": scenario_name,
        "algorithm": algorithm,
        "route": path or [],
        "goal_reached": goal,
        "route_valid": valid and not unsafe,
        "unsafe_route": unsafe,
        "route_cost": cost if valid else 0,
        "execution_time_ms": elapsed_ms,
        "nodes_expanded": expanded,
        "unknown_crowd_information": list(partial_unknown_crowds),
        "uncertainty_note": (
            "Crowd status unknown at: " + ", ".join(partial_unknown_crowds)
            if partial_unknown_crowds else "All configured crowd observations known."
        ),
    }
    row["score"] = calculate_score(row)
    return row


def run_experiments():
    """Run deterministic scenarios and return measured rows and summaries."""
    scenarios = [
        {
            "name": "E1_Normal",
            "start": "A", "exits": ["G1", "G2"],
            "blocked": [], "crowded": [], "restricted": [],
            "emergency": None,
        },
        {
            "name": "E2_Fire_Blocked_Corridor",
            "start": "A", "exits": ["G1", "G2"],
            "blocked": [("A", "B")], "crowded": [],
            "restricted": [], "emergency": "A",
        },
        {
            "name": "E3_Crowded_Main_Gate",
            "start": "A", "exits": ["G1", "G2"],
            "blocked": [], "crowded": ["G1"], "restricted": [],
            "emergency": "A",
        },
        {
            "name": "E4_Restricted_Block_B",
            "start": "A", "exits": ["G1", "G2"],
            "blocked": [], "crowded": [], "restricted": ["B"],
            "emergency": "A",
        },
        {
            "name": "E5_Partially_Observable_Crowd",
            "start": "A", "exits": ["G1", "G2"],
            "blocked": [], "crowded": [], "restricted": [],
            "emergency": "A", "unknown": ["G2"],
        },
        {
            "name": "E6_Dynamic_Exit_Closure",
            "start": "A", "exits": ["G1", "G2"],
            "blocked": [], "crowded": [], "restricted": [],
            "emergency": "A",
        },
    ]

    results = []
    for scenario in scenarios:
        # E6 models a changed environment after a closure is observed.
        blocked = list(scenario["blocked"])
        exits = list(scenario["exits"])
        if scenario["name"] == "E6_Dynamic_Exit_Closure":
            # P-G1 becomes unavailable during the dynamic update.
            blocked.append(("P", "G1"))
        for algorithm in ("BFS", "A*"):
            results.append(_run_one(
                algorithm, scenario["name"], scenario["start"], exits,
                blocked=blocked,
                crowded=scenario["crowded"],
                restricted=scenario["restricted"],
                emergency_location=scenario["emergency"],
                partial_unknown_crowds=scenario.get("unknown", ()),
            ))

    grouped = {}
    for row in results:
        grouped.setdefault(row["experiment"], []).append(row)

    return results, grouped


def print_results(results):
    print("\nEXPERIMENTAL RESULTS (measured on this run)")
    print("-" * 105)
    print(f"{'Scenario':30} {'Algorithm':8} {'Route':28} {'Nodes':>7} {'Time ms':>10} {'Cost':>8} {'Score':>8}")
    print("-" * 105)
    for row in results:
        route = " -> ".join(row["route"]) if row["route"] else "NO SAFE ROUTE"
        print(
            f"{row['experiment']:30} {row['algorithm']:8} "
            f"{route:28.28} {row['nodes_expanded']:7d} "
            f"{row['execution_time_ms']:10.4f} {row['route_cost']:8.2f} "
            f"{row['score']:8.2f}"
        )


if __name__ == "__main__":
    rows, _ = run_experiments()
    print_results(rows)
    print("\nNote: execution time varies by computer and run. Record your own output.")
