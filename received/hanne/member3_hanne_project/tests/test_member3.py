import unittest
from performance import calculate_score, summarize_runs
from experiments import bfs_search, astar_search, run_experiments


class TestMember3(unittest.TestCase):
    def test_score_is_bounded(self):
        score = calculate_score({
            "goal_reached": True, "route_valid": True,
            "route_cost": 2, "execution_time_ms": 1,
            "unsafe_route": False
        })
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

    def test_unsafe_route_penalized(self):
        safe = calculate_score({
            "goal_reached": True, "route_valid": True,
            "route_cost": 2, "execution_time_ms": 1
        })
        unsafe = calculate_score({
            "goal_reached": True, "route_valid": True,
            "route_cost": 2, "execution_time_ms": 1,
            "unsafe_route": True
        })
        self.assertLess(unsafe, safe)

    def test_bfs_finds_exit(self):
        route, expanded, cost = bfs_search("A", ["G1", "G2"])
        self.assertIsNotNone(route)
        self.assertIn(route[-1], ["G1", "G2"])
        self.assertGreaterEqual(expanded, 1)

    def test_blocked_edge_not_used(self):
        route, _, _ = bfs_search("A", ["G1", "G2"], blocked_edges=[("A", "B")])
        self.assertNotIn(("A", "B"), list(zip(route, route[1:])))

    def test_astar_finds_exit(self):
        route, expanded, cost = astar_search("A", ["G1", "G2"])
        self.assertIsNotNone(route)
        self.assertIn(route[-1], ["G1", "G2"])

    def test_experiments_produce_rows(self):
        rows, grouped = run_experiments()
        self.assertEqual(len(rows), 12)
        self.assertIn("E5_Partially_Observable_Crowd", grouped)

    def test_empty_summary(self):
        self.assertEqual(summarize_runs([])["runs"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
