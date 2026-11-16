"""
What-If Simulation View for Emergency Operations Command Center.
Evaluates algorithmic resilience across pre-configured and custom contingency drills.
"""

import pandas as pd
import streamlit as st

from environment.campus_graph import CAMPUS_GRAPH, EMERGENCY_EXITS, LOCATIONS, START_LOCATIONS
from services.emergency_service import process_emergency
from ui.theme import render_disclaimer, render_html, render_page_header, render_route_card


def render_what_if_view():
    """Render the Interactive What-If Scenario Simulation Page."""
    render_page_header(
        "🧪 What-If Contingency & Stress Simulation",
        "Simulate Dynamic Campus Disruptions, Hazard Cascades, and Measure Algorithmic Robustness",
        badge_text="SCENARIO SIMULATOR",
    )

    scenarios = {
        "Scenario 1: Major Fire Near Library": {
            "start": "A",
            "type": "fire",
            "em_loc": "L",
            "blocked": [("A", "L"), ("B", "L"), ("L", "C"), ("L", "M")],
            "crowded": [],
            "restricted": [],
            "exits": ["G1", "G2"],
            "desc": "Intense blaze engulfs the central Library, severing all 4 central connector pathways.",
        },
        "Scenario 2: Fire at Canteen with Crowded Parking": {
            "start": "B",
            "type": "fire",
            "em_loc": "C",
            "blocked": [("B", "C"), ("L", "C"), ("C", "M"), ("C", "P")],
            "crowded": ["P"],
            "restricted": [],
            "exits": ["G1", "G2"],
            "desc": "Structural fire at the Canteen with severe pedestrian congestion at Parking Area.",
        },
        "Scenario 3: Main Gate (G1) Structural Blockage": {
            "start": "A",
            "type": "security",
            "em_loc": "G1",
            "blocked": [("P", "G1")],
            "crowded": [],
            "restricted": [],
            "exits": ["G2"],
            "desc": "Main Gate collapse forces 100% of campus evacuation traffic toward secondary Gate 2.",
        },
        "Scenario 4: Dense Crowd Congestion at Block B": {
            "start": "A",
            "type": "other",
            "em_loc": None,
            "blocked": [],
            "crowded": ["B"],
            "restricted": [],
            "exits": ["G1", "G2"],
            "desc": "Academic Block B experiences heavy rush (+5 cost); evaluates Dijkstra's cost avoidance vs BFS.",
        },
        "Scenario 5: Complete Security Lockdown (No Routes)": {
            "start": "A",
            "type": "security",
            "em_loc": None,
            "blocked": [("P", "G1"), ("P", "G2")],
            "crowded": [],
            "restricted": ["P"],
            "exits": ["G1", "G2"],
            "desc": "All exit portals obstructed; evaluates system ability to report failure without hallucinating routes.",
        },
    }

    st.markdown("### 🎯 Pre-Configured Benchmark Contingency Drills")
    choice = st.selectbox("Select Benchmark Scenario to Execute", list(scenarios.keys()))
    sc = scenarios[choice]

    render_html(f"""
    <div class="glass-card" style="border-left: 4px solid #E879F9;">
        <strong style="color:#FFFFFF; font-size:15px;">Scenario Brief:</strong>
        <p style="color:#FFFFFF; margin:6px 0 0 0; font-size:13.5px;">{sc['desc']}</p>
    </div>
    """)

    if st.button("🚀 EXECUTE CONTINGENCY DRILL", width="stretch"):
        res = process_emergency(
            start=sc["start"],
            emergency_type=sc["type"],
            emergency_location=sc["em_loc"],
            blocked_edges=sc["blocked"],
            crowded_locations=sc["crowded"],
            restricted_locations=sc["restricted"],
            available_exits=sc["exits"],
        )

        st.session_state.last_result = res
        routes = res.get("routes", {})
        bfs = routes.get("BFS")
        astar = routes.get("A*")

        c1, c2 = st.columns(2)
        render_route_card(
            c1,
            "recommended",
            astar,
            title="🟢 Dijkstra Output (Cost-Optimal)",
            subtitle=f"Scenario: {choice}",
        )
        render_route_card(
            c2,
            "alternative",
            bfs,
            title="🟣 BFS Output (Fewest Hops)",
            subtitle=f"Scenario: {choice}",
        )

    render_disclaimer()
