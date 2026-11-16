"""
Member 2 module: rule-based decision recommendations.

Rules are transparent IF-THEN statements suitable for explaining in the
project report and viva. The rules produce recommendations, not a route.
"""

from actions import ACTIONS


# Each rule is represented as (rule_id, explanation, condition, action_ids).
# Conditions are evaluated in apply_rules() to keep the logic readable.
RULE_DESCRIPTIONS = [
    ("R1", "Fire reported", "If the emergency is fire, avoid entering the fire-affected area and notify security."),
    ("R2", "Medical emergency", "If the emergency is medical, notify the simulated medical team."),
    ("R3", "Blocked corridor", "If a corridor/edge is blocked, do not traverse that connection."),
    ("R4", "Heavy crowd", "If a location is crowded, add a crowd penalty during route evaluation where supported."),
    ("R5", "Security restriction", "If a location is restricted, do not enter it."),
    ("R6", "Power failure", "If power has failed, re-check route options and notify security."),
    ("R7", "Alternative exit", "If multiple exits are available, allow the route planner to compare them."),
    ("R8", "No available exit", "If no exit is available, report that no safe route can be recommended."),
]


def apply_rules(state):
    """
    Apply all matching rules and return structured decision recommendations.

    Returns:
        {
          "actions": [action IDs],
          "recommendations": [human-readable strings],
          "matched_rules": [rule IDs],
          "status": "Recommendations generated" or "No safe exit available"
        }

    This function does not select a route. Member 4's search algorithm must
    calculate a route using blocked edges, restricted locations, crowd costs,
    and available exits.
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
    matched_rules = []

    def add(rule_id, *action_ids):
        matched_rules.append(rule_id)
        actions.extend(action_ids)

    # R1: fire
    if emergency_type == "fire":
        add("R1", "avoid_danger_area", "notify_security")

    # R2: medical
    if emergency_type == "medical":
        add("R2", "notify_medical_team")

    # R3: blocked corridor
    if emergency_type == "blocked_corridor" or blocked_edges:
        add("R3", "avoid_blocked_corridor")

    # R4: heavy crowd
    if emergency_type == "heavy_crowd" or crowded_locations:
        add("R4", "avoid_crowded_location")

    # R5: security restriction
    if emergency_type == "security_restriction" or restricted_locations:
        add("R5", "avoid_restricted_area", "notify_security")

    # R6: power failure
    if power_failure or emergency_type == "power_failure":
        add("R6", "check_power_failure", "notify_security")

    # R7: compare exits when there is a choice.
    if len(set(available_exits)) > 1:
        add("R7", "select_alternative_exit")

    # R8: no available exit. The route planner must also report if all exits
    # are unreachable even when this list is non-empty.
    if not available_exits:
        add("R8", "report_no_safe_route")

    actions = list(dict.fromkeys(actions))
    recommendations = [ACTIONS[action_id] for action_id in actions]

    status = "No safe exit available" if not available_exits else "Recommendations generated"

    return {
        "actions": actions,
        "recommendations": recommendations,
        "matched_rules": list(dict.fromkeys(matched_rules)),
        "status": status,
    }


def display_decision(decision):
    """Print a decision dictionary returned by apply_rules()."""
    print(f"\nDecision status: {decision['status']}")

    if decision["matched_rules"]:
        print("Matched rules:", ", ".join(decision["matched_rules"]))

    if decision["recommendations"]:
        print("Recommendations:")
        for number, recommendation in enumerate(decision["recommendations"], start=1):
            print(f"{number}. {recommendation}")
    else:
        print("No special recommendations were generated.")
