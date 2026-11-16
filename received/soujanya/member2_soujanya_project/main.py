"""
Standalone demonstration for Member 2.
Run: python main.py
"""

from actions import get_possible_actions, display_actions
from decision_rules import apply_rules, display_decision


def main():
    # Shared team input format. Keep location names and keys consistent with
    # Member 1's state.py and the campus graph.
    emergency_data = {
        "emergency_type": "fire",
        "emergency_location": "A",
        "current_location": "A",
        "blocked_edges": [("A", "B")],
        "crowded_locations": ["G1"],
        "restricted_locations": [],
        "available_exits": ["G1", "G2"],
        "power_failure": False,
    }

    print("EMERGENCY RESPONSE DECISION AGENT")
    print("Member 2: Actions and Decision Rules")
    print("=" * 48)

    possible_actions = get_possible_actions(emergency_data)
    display_actions(possible_actions)

    decision = apply_rules(emergency_data)
    display_decision(decision)

    print("\nIntegration note:")
    print("Pass the state and restrictions to Member 4's route planner.")
    print("This module does not claim that a route is safe or reachable.")


if __name__ == "__main__":
    main()
