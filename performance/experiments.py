
"""
Member 3: Reproducible campus experiments and algorithm comparison.

Uses the integrated campus graph, BFS, A* and performance modules.
"""

from performance.performance import calculate_score, summarize_runs
from performance.route_metrics import run_route_algorithm
from environment.campus_graph import CAMPUS_GRAPH, EMERGENCY_EXITS


def _run_one(
    algorithm,
    scenario_name,
    start,
    exits,
    blocked=(),
    crowded=(),
    restricted=(),
    emergency_location=None,
    partial_unknown_crowds=()
):
    """
    Run one experiment using the integrated route algorithms.
    """

    # Avoid the emergency location unless it is the starting location.
    forbidden = set()

    if emergency_location and emergency_location != start:
        forbidden.add(emergency_location)

    # Combine restricted and emergency-affected locations.
    unsafe_locations = set(restricted) | forbidden

    # Create blocked edges from restricted locations.
    effective_blocked_edges = list(blocked)

    for location in unsafe_locations:
        for neighbor in CAMPUS_GRAPH.get(location, {}):
            effective_blocked_edges.append((location, neighbor))

    best_result = None
    best_exit = None

    # Try each available exit.
    for exit_location in exits:

        if exit_location in unsafe_locations:
            continue

        result = run_route_algorithm(
            algorithm,
            start,
            exit_location,
            blocked_edges=effective_blocked_edges,
            crowded_locations=list(crowded)
        )

        if result["route"] is None:
            continue

        if (
            best_result is None
            or result["route_cost"] < best_result["route_cost"]
        ):
            best_result = result
            best_exit = exit_location

    # No safe route found.
    if best_result is None:

        row = {
            "experiment": scenario_name,
            "algorithm": algorithm,
            "route": [],
            "goal_reached": False,
            "route_valid": False,
            "unsafe_route": False,
            "route_cost": 0,
            "execution_time_ms": 0,
            "nodes_expanded": 0,
            "unknown_crowd_information": list(partial_unknown_crowds),
            "uncertainty_note": "No available route found."
        }

    else:

        path = best_result["route"]

        # Verify blocked edges.
        blocked_set = {
            frozenset(edge) for edge in effective_blocked_edges
        }

        unsafe = any(
            frozenset((path[i], path[i + 1])) in blocked_set
            for i in range(len(path) - 1)
        )

        # Verify restricted and emergency-affected locations.
        unsafe = unsafe or any(
            node in unsafe_locations
            for node in path[1:]
        )

        # Verify that every route connection exists.
        valid = (
            path[0] == start
            and path[-1] == best_exit
            and all(
                path[i + 1] in CAMPUS_GRAPH[path[i]]
                for i in range(len(path) - 1)
            )
        )

        row = {
            "experiment": scenario_name,
            "algorithm": algorithm,
            "route": path,
            "goal_reached": path[-1] in exits,
            "route_valid": valid and not unsafe,
            "unsafe_route": unsafe,
            "route_cost": best_result["route_cost"],
            "execution_time_ms": best_result["execution_time_ms"],
            "nodes_expanded": best_result["nodes_expanded"],
            "unknown_crowd_information": list(partial_unknown_crowds),
            "uncertainty_note": (
                "Crowd status unknown at: "
                + ", ".join(partial_unknown_crowds)
                if partial_unknown_crowds
                else "All configured crowd observations known."
            )
        }

    row["score"] = calculate_score(row)

    return row


def run_experiments():
    """
    Run six emergency scenarios and compare BFS and A*.
    """

    scenarios = [
        {
            "name": "E1_Normal",
            "start": "A",
            "exits": EMERGENCY_EXITS,
            "blocked": [],
            "crowded": [],
            "restricted": [],
            "emergency": None
        },
        {
            "name": "E2_Fire_Blocked_Corridor",
            "start": "A",
            "exits": EMERGENCY_EXITS,
            "blocked": [("A", "B")],
            "crowded": [],
            "restricted": [],
            "emergency": "A"
        },
        {
            "name": "E3_Crowded_Main_Gate",
            "start": "A",
            "exits": EMERGENCY_EXITS,
            "blocked": [],
            "crowded": ["G1"],
            "restricted": [],
            "emergency": "A"
        },
        {
            "name": "E4_Restricted_Block_B",
            "start": "A",
            "exits": EMERGENCY_EXITS,
            "blocked": [],
            "crowded": [],
            "restricted": ["B"],
            "emergency": "A"
        },
        {
            "name": "E5_Partially_Observable_Crowd",
            "start": "A",
            "exits": EMERGENCY_EXITS,
            "blocked": [],
            "crowded": [],
            "restricted": [],
            "emergency": "A",
            "unknown": ["G2"]
        },
        {
            "name": "E6_Dynamic_Exit_Closure",
            "start": "A",
            "exits": EMERGENCY_EXITS,
            "blocked": [("P", "G1")],
            "crowded": [],
            "restricted": [],
            "emergency": "A"
        }
    ]

    results = []

    for scenario in scenarios:

        for algorithm in ("BFS", "A*"):

            result = _run_one(
                algorithm=algorithm,
                scenario_name=scenario["name"],
                start=scenario["start"],
                exits=scenario["exits"],
                blocked=scenario["blocked"],
                crowded=scenario["crowded"],
                restricted=scenario["restricted"],
                emergency_location=scenario["emergency"],
                partial_unknown_crowds=scenario.get("unknown", [])
            )

            results.append(result)

    grouped = {}

    for row in results:
        grouped.setdefault(row["experiment"], []).append(row)

    return results, grouped


def print_results(results):

    print("\nEXPERIMENTAL RESULTS (measured on this run)")
    print("-" * 110)

    print(
        f"{'Scenario':30} {'Algorithm':8} {'Route':28} "
        f"{'Nodes':>7} {'Time ms':>10} {'Cost':>8} {'Score':>8}"
    )

    print("-" * 110)

    for row in results:

        route = (
            " -> ".join(row["route"])
            if row["route"]
            else "NO SAFE ROUTE"
        )

        print(
            f"{row['experiment']:30} "
            f"{row['algorithm']:8} "
            f"{route:28.28} "
            f"{row['nodes_expanded']:7d} "
            f"{row['execution_time_ms']:10.4f} "
            f"{row['route_cost']:8.2f} "
            f"{row['score']:8.2f}"
        )


if __name__ == "__main__":

    rows, grouped = run_experiments()

    print_results(rows)

    summary = summarize_runs(rows)

    print("\nOVERALL PERFORMANCE SUMMARY")
    print("-" * 40)

    for key, value in summary.items():
        print(f"{key}: {value}")

    print(
        "\nNote: Execution time varies by computer and run. "
        "Results use simulated campus data."
    )
