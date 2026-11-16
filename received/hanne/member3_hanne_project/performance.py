"""
Member 3: Performance measurement utilities.

The scoring weights are illustrative project settings, not validated safety
weights. The score is for comparing simulation runs, not for real emergencies.
"""

DEFAULT_WEIGHTS = {
    "safe_goal_reached": 50,
    "valid_route": 25,
    "low_route_cost": 15,
    "quick_decision": 10,
    "unsafe_route_penalty": 100,
}


def calculate_score(result, weights=None):
    """
    Calculate a transparent 0-100 style simulation score.

    Expected result keys:
      goal_reached (bool), route_valid (bool), route_cost (number),
      execution_time_ms (number), unsafe_route (bool)

    Route cost is normalized against a configurable reference_cost (default 10).
    Execution time is normalized against a configurable time_limit_ms (default 100).
    """
    if not isinstance(result, dict):
        raise TypeError("result must be a dictionary")

    w = dict(DEFAULT_WEIGHTS)
    if weights:
        w.update(weights)

    goal = bool(result.get("goal_reached", False))
    valid = bool(result.get("route_valid", False))
    unsafe = bool(result.get("unsafe_route", False))
    route_cost = max(0.0, float(result.get("route_cost", 0) or 0))
    elapsed = max(0.0, float(result.get("execution_time_ms", 0) or 0))

    score = 0.0
    if goal:
        score += w["safe_goal_reached"]
    if valid:
        score += w["valid_route"]

    reference_cost = max(1.0, float(result.get("reference_cost", 10)))
    if valid and not unsafe:
        score += w["low_route_cost"] * max(0.0, 1.0 - route_cost / reference_cost)

    time_limit = max(1.0, float(result.get("time_limit_ms", 100)))
    score += w["quick_decision"] * max(0.0, 1.0 - elapsed / time_limit)

    if unsafe:
        score -= w["unsafe_route_penalty"]

    return round(max(0.0, min(100.0, score)), 2)


def summarize_runs(rows):
    """Return aggregate metrics for a list of experiment result dictionaries."""
    if not rows:
        return {
            "runs": 0, "success_rate": 0.0, "average_execution_time_ms": 0.0,
            "average_nodes_expanded": 0.0, "average_route_cost": 0.0,
            "average_score": 0.0,
        }

    count = len(rows)
    successes = sum(bool(row.get("goal_reached")) for row in rows)
    def avg(key):
        values = [float(row.get(key, 0) or 0) for row in rows]
        return round(sum(values) / count, 4)

    return {
        "runs": count,
        "success_rate": round(100.0 * successes / count, 2),
        "average_execution_time_ms": avg("execution_time_ms"),
        "average_nodes_expanded": avg("nodes_expanded"),
        "average_route_cost": avg("route_cost"),
        "average_score": avg("score"),
    }
