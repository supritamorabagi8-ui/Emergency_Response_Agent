
"""
Central service connecting all Emergency Response Agent modules.
"""

from environment.state import create_emergency_state
from environment.validation import validate_emergency_input
from environment.campus_graph import (
    CAMPUS_GRAPH,
    EMERGENCY_EXITS,
    LOCATIONS
)

from decision.decision_rules import apply_rules
from performance.route_metrics import run_route_algorithm


def process_emergency(
    start,
    emergency_type,
    emergency_location=None,
    blocked_edges=None,
    crowded_locations=None,
    restricted_locations=None,
    available_exits=None
):
    """
    Process emergency details and calculate safe available routes.
    """

    blocked_edges = blocked_edges or []
    crowded_locations = crowded_locations or []
    restricted_locations = restricted_locations or []

    # 1. Validate emergency input.
    valid, message = validate_emergency_input(start, emergency_type)

    if not valid:
        return {
            "success": False,
            "message": message,
            "routes": {"BFS": None, "A*": None}
        }

    # 2. Validate emergency location.
    if emergency_location and emergency_location not in LOCATIONS:
        return {
            "success": False,
            "message": "Invalid emergency location.",
            "routes": {"BFS": None, "A*": None}
        }

    # 3. Validate campus locations.
    for location in restricted_locations + crowded_locations:
        if location not in LOCATIONS:
            return {
                "success": False,
                "message": f"Invalid campus location: {location}",
                "routes": {"BFS": None, "A*": None}
            }

    # 4. Select emergency exits.
    exits = (
        list(available_exits)
        if available_exits is not None
        else EMERGENCY_EXITS.copy()
    )

    if not exits:
        return {
            "success": False,
            "message": "No emergency exits are available.",
            "routes": {"BFS": None, "A*": None}
        }

    for exit_location in exits:
        if exit_location not in EMERGENCY_EXITS:
            return {
                "success": False,
                "message": f"Invalid emergency exit: {exit_location}",
                "routes": {"BFS": None, "A*": None}
            }

    # 5. Create emergency state.
    state = create_emergency_state(
        start=start,
        emergency_type=emergency_type,
        emergency_location=emergency_location,
        blocked_edges=blocked_edges,
        crowded_locations=crowded_locations,
        restricted_locations=restricted_locations,
        available_exits=exits
    )

    # 6. Apply decision rules.
    decision = apply_rules(state)

    # 7. Identify unsafe locations.
    unsafe_locations = set(restricted_locations)

    if emergency_location and emergency_location != start:
        unsafe_locations.add(emergency_location)

    # 8. Block user-specified edges and connections to unsafe locations.
    effective_blocked_edges = list(blocked_edges)

    for location in unsafe_locations:
        for neighbor in CAMPUS_GRAPH.get(location, {}):
            edge = (location, neighbor)

            # Avoid adding duplicate blocked edges.
            if edge not in effective_blocked_edges:
                effective_blocked_edges.append(edge)

    # 9. Calculate routes using BFS and A*.
    algorithm_results = {}

    for algorithm in ("BFS", "A*"):

        best_result = None

        for exit_location in exits:

            # Never route through an unsafe exit.
            if exit_location in unsafe_locations:
                continue

            result = run_route_algorithm(
                algorithm,
                start,
                exit_location,
                blocked_edges=effective_blocked_edges,
                crowded_locations=crowded_locations
            )

            route = result.get("route")

            if not route:
                continue

            if (
                best_result is None
                or result["route_cost"] < best_result["route_cost"]
            ):
                best_result = result

        algorithm_results[algorithm] = best_result

    # 10. Check whether any safe route exists.
    safe_route_found = any(
        result is not None
        for result in algorithm_results.values()
    )

    if not safe_route_found:
        message = (
            "No safe route is currently available. "
            "Please review blocked paths, restricted areas, "
            "and available emergency exits."
        )
    else:
        message = "Emergency analysis completed. Safe route(s) found."

    # 11. Return results to frontend.
    return {
        "success": True,
        "message": message,
        "emergency_state": state,
        "decision": decision,
        "routes": algorithm_results,
        "safe_route_found": safe_route_found,
        "unsafe_locations": list(unsafe_locations),
        "available_exits": exits
    }
