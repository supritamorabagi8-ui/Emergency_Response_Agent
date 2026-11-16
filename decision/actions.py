"""
Member 2 module: possible actions for the Emergency Response Decision Agent.

Input contract:
    state: normalized dictionary returned by Member 1's create_state()

This module recommends actions only. It does NOT calculate or guarantee a safe
route. The route must be validated by Member 4's BFS/A* search implementation.
"""

ACTIONS = {
    "avoid_danger_area": "Avoid entering the known emergency area.",
    "avoid_blocked_corridor": "Do not use blocked corridor connections.",
    "avoid_crowded_location": "Prefer routes that reduce exposure to crowded locations.",
    "avoid_restricted_area": "Do not enter security-restricted locations.",
    "select_alternative_exit": "Consider another available exit.",
    "notify_security": "Send a simulated notification to campus security.",
    "notify_medical_team": "Send a simulated notification to the medical team.",
    "check_power_failure": "Re-check route options because lighting or powered systems may be unavailable.",
    "report_no_safe_route": "Report that no safe route was found; do not invent a route.",
}


def get_possible_actions(state):
    """
    Return a de-duplicated list of action IDs supported by the current state.

    Expected state keys:
      emergency_type, emergency_location, current_location, blocked_edges,
      crowded_locations, restricted_locations, available_exits, power_failure

    Missing optional list values are treated as empty lists. The caller should
    normally pass a validated state from Member 1.
    """
    if not isinstance(state, dict):
        raise TypeError("state must be a dictionary")

    emergency_type = state.get("emergency_type")
    blocked_edges = state.get("blocked_edges") or []
    crowded_locations = state.get("crowded_locations") or []
    restricted_locations = state.get("restricted_locations") or []
    available_exits = state.get("available_exits") or []
    power_failure = bool(state.get("power_failure", False))

    actions = []

    if emergency_type == "fire":
        actions.extend(["avoid_danger_area", "notify_security"])

    if emergency_type == "medical":
        actions.append("notify_medical_team")

    if emergency_type == "blocked_corridor" or blocked_edges:
        actions.append("avoid_blocked_corridor")

    if emergency_type == "heavy_crowd" or crowded_locations:
        actions.append("avoid_crowded_location")

    if emergency_type == "security_restriction" or restricted_locations:
        actions.extend(["avoid_restricted_area", "notify_security"])

    if power_failure or emergency_type == "power_failure":
        actions.extend(["check_power_failure", "notify_security"])

    # If more than one exit is available, an alternative may be considered.
    if len(set(available_exits)) > 1:
        actions.append("select_alternative_exit")

    # Preserve order while removing duplicates.
    return list(dict.fromkeys(actions))


def describe_actions(action_ids):
    """Convert action IDs into readable descriptions."""
    descriptions = []
    for action_id in action_ids:
        if action_id not in ACTIONS:
            raise ValueError(f"Unknown action ID: {action_id}")
        descriptions.append(ACTIONS[action_id])
    return descriptions


def display_actions(action_ids):
    """Print the recommended actions in a readable format."""
    if not action_ids:
        print("No special action was triggered by the supplied state.")
        return

    print("\nRecommended agent actions:")
    for number, action_id in enumerate(action_ids, start=1):
        print(f"{number}. {ACTIONS[action_id]}")
