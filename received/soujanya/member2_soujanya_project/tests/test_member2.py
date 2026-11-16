import unittest

from actions import get_possible_actions, describe_actions
from decision_rules import apply_rules


class TestMember2ActionsAndRules(unittest.TestCase):

    def test_fire_blocked_and_crowded(self):
        state = {
            "emergency_type": "fire",
            "emergency_location": "A",
            "current_location": "A",
            "blocked_edges": [("A", "B")],
            "crowded_locations": ["G1"],
            "restricted_locations": [],
            "available_exits": ["G1", "G2"],
            "power_failure": False,
        }
        actions = get_possible_actions(state)
        self.assertIn("avoid_danger_area", actions)
        self.assertIn("avoid_blocked_corridor", actions)
        self.assertIn("avoid_crowded_location", actions)
        self.assertIn("select_alternative_exit", actions)

        decision = apply_rules(state)
        self.assertIn("R1", decision["matched_rules"])
        self.assertIn("R3", decision["matched_rules"])
        self.assertIn("R4", decision["matched_rules"])
        self.assertEqual(decision["status"], "Recommendations generated")

    def test_medical(self):
        state = {
            "emergency_type": "medical",
            "blocked_edges": [],
            "crowded_locations": [],
            "restricted_locations": [],
            "available_exits": ["G1"],
            "power_failure": False,
        }
        self.assertIn("notify_medical_team", get_possible_actions(state))
        self.assertIn("R2", apply_rules(state)["matched_rules"])

    def test_security_restriction_and_power_failure(self):
        state = {
            "emergency_type": "security_restriction",
            "blocked_edges": [],
            "crowded_locations": [],
            "restricted_locations": ["P"],
            "available_exits": ["G2"],
            "power_failure": True,
        }
        actions = get_possible_actions(state)
        self.assertIn("avoid_restricted_area", actions)
        self.assertIn("check_power_failure", actions)
        decision = apply_rules(state)
        self.assertIn("R5", decision["matched_rules"])
        self.assertIn("R6", decision["matched_rules"])

    def test_no_available_exit(self):
        state = {
            "emergency_type": "fire",
            "blocked_edges": [],
            "crowded_locations": [],
            "restricted_locations": [],
            "available_exits": [],
            "power_failure": False,
        }
        decision = apply_rules(state)
        self.assertEqual(decision["status"], "No safe exit available")
        self.assertIn("report_no_safe_route", decision["actions"])

    def test_descriptions(self):
        self.assertTrue(describe_actions(["notify_security"])[0].startswith("Send"))

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            get_possible_actions(None)
        with self.assertRaises(TypeError):
            apply_rules(None)


if __name__ == "__main__":
    unittest.main(verbosity=2)
