"""
Grounded AI Emergency Assistant for Emergency Response Agent AI.
Provides deterministic, factually grounded answers based strictly on the active campus graph,
rules, and simulation state. Includes disclaimer regarding simulation limitations.
"""

from decision.decision_rules import RULE_DESCRIPTIONS
from environment.campus_graph import CAMPUS_GRAPH, EMERGENCY_EXITS, LOCATIONS


def answer_emergency_question(question: str, current_state: dict, current_result: dict) -> str:
    """Analyze the user question and generate a grounded, accurate response."""
    q = question.lower().strip()

    # Disclaimer header
    disclaimer = "ℹ️ [SIMULATION GROUNDED RESPONSE] "

    # 1. Current emergency query
    if any(k in q for k in ["current", "active", "status", "happening", "what is"]):
        if not current_result or not current_result.get("success"):
            return (
                disclaimer + "No active simulated emergency is currently loaded. "
                "Configure an incident in the 'Emergency Analysis' view to begin simulation."
            )

        st = current_result.get("emergency_state", {})
        em_type = st.get("emergency_type", "General").title()
        start = st.get("start", "Unknown")
        em_loc = st.get("emergency_location") or "Unspecified"
        return (
            disclaimer + f"Current active simulated emergency: **{em_type} Emergency**.<br>"
            f"• Originating Evacuation Point: **{start} ({LOCATIONS.get(start)})**<br>"
            f"• Reported Epicenter: **{em_loc} ({LOCATIONS.get(em_loc, 'N/A')})**<br>"
            f"• Blocked Corridors: {len(st.get('blocked_edges', []))} connection(s) unavailable."
        )

    # 2. Routes and available exits
    if any(k in q for k in ["route", "path", "candidate", "evacuate", "exit"]):
        if not current_result or not current_result.get("routes"):
            return disclaimer + "No candidate routes have been computed yet."

        routes = current_result.get("routes", {})
        bfs = routes.get("BFS")
        astar = routes.get("A*")

        parts = []
        if astar:
            p = " → ".join(astar["route"])
            parts.append(
                f"• **Dijkstra / A* Route (Cost-Optimal)**: `{p}` (Cost: {astar['route_cost']}, Time: {astar['execution_time_ms']:.4f} ms, Goal Exit: **{astar['route'][-1]}**)"
            )
        else:
            parts.append("• **Dijkstra / A* Route**: No candidate route available.")

        if bfs:
            p = " → ".join(bfs["route"])
            parts.append(
                f"• **BFS Route (Minimum Hops)**: `{p}` (Cost: {bfs['route_cost']}, Time: {bfs['execution_time_ms']:.4f} ms, Goal Exit: **{bfs['route'][-1]}**)"
            )
        else:
            parts.append("• **BFS Route**: No candidate route available.")

        return disclaimer + "Calculated Candidate Evacuation Routes:<br>" + "<br>".join(parts)

    # 3. Decision rules
    if any(k in q for k in ["rule", "decision", "why did", "recommend"]):
        if not current_result or not current_result.get("decision"):
            rules_str = ", ".join(f"**{r[0]}**: {r[1]}" for r in RULE_DESCRIPTIONS)
            return (
                disclaimer + f"The decision engine evaluates 8 transparent IF-THEN rules:<br>{rules_str}"
            )

        dec = current_result.get("decision", {})
        matched = dec.get("matched_rules", [])
        recs = dec.get("recommendations", [])
        recs_str = "<br>• " + "<br>• ".join(recs) if recs else "None"
        return (
            disclaimer + f"Triggered Rules: **{', '.join(matched) or 'None'}**<br>"
            f"Tactical Action Directives:{recs_str}"
        )

    # 4. Compare BFS and Dijkstra
    if any(k in q for k in ["compare", "bfs vs", "dijkstra", "difference", "algorithm"]):
        return (
            disclaimer + "<strong>Comparison between BFS and Dijkstra (Zero-Heuristic A*):</strong><br>"
            "1. **BFS (Breadth-First Search)** treats every campus corridor equally (unweighted hops = 1). It finds the path with the fewest building transitions, ignoring physical travel distances and crowd congestion.<br>"
            "2. **Dijkstra (A* with h=0)** evaluates actual corridor travel costs and incorporates dynamic crowd penalties (+5 cost per crowded node). It guarantees the mathematically minimum travel effort route."
        )

    # 5. Fallback campus graph summary
    return (
        disclaimer + f"I can answer questions regarding the active simulation, campus topology, "
        f"decision rules, or route comparisons. The campus graph contains {len(LOCATIONS)} locations: "
        f"{', '.join(f'{k} ({v})' for k, v in LOCATIONS.items())} with designated emergency exits: {', '.join(EMERGENCY_EXITS)}."
    )
