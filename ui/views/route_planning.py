"""
Route Planning & Comparison View for Emergency Operations Command Center.
Features detailed side-by-side algorithmic breakdown, comparative charts, and step-by-step corridor walkthrough.
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from environment.campus_graph import CAMPUS_GRAPH, EMERGENCY_EXITS, LOCATIONS
from services.emergency_service import process_emergency
from ui.graph_visualizer import create_campus_figure
from ui.theme import render_disclaimer, render_page_header, render_route_card


def render_route_planning():
    """Render the Dedicated Route Planning & Recalculation Page."""
    render_page_header(
        "🛣️ Evacuation Route Planning & Algorithmic Evaluation",
        "Comparative Assessment Between BFS and Dijkstra's Search Algorithms with Dynamic Pathway Adaptation",
        badge_text="ROUTING MATRIX",
    )

    last_res = st.session_state.get("last_result")
    if not last_res or not last_res.get("success"):
        st.info("No active emergency analysis loaded. Please run an analysis in 'Emergency Analysis' to evaluate routes.")
        render_disclaimer()
        return

    routes = last_res.get("routes", {})
    state = last_res.get("emergency_state", {})
    bfs = routes.get("BFS")
    astar = routes.get("A*")

    # Algorithmic Comparison Cards
    c1, c2 = st.columns(2)
    render_route_card(
        c1,
        "recommended",
        astar,
        title="🟢 Recommended: Dijkstra / Zero-Heuristic A*",
        subtitle="Cost-Optimal Evacuation Path (Distance & Crowd Weighted)",
    )
    render_route_card(
        c2,
        "alternative",
        bfs,
        title="🟣 Alternative: Breadth-First Search (BFS)",
        subtitle="Unweighted Fewest Building Transitions (Hops)",
    )

    # Comparative Metric Visualizations
    comp_rows = []
    if astar:
        comp_rows.append({
            "Algorithm": "Dijkstra (A* h=0)",
            "Route Cost": astar["route_cost"],
            "Execution Time (ms)": astar["execution_time_ms"],
            "Nodes Expanded": astar["nodes_expanded"],
            "Score": astar["score"],
        })
    if bfs:
        comp_rows.append({
            "Algorithm": "BFS",
            "Route Cost": bfs["route_cost"],
            "Execution Time (ms)": bfs["execution_time_ms"],
            "Nodes Expanded": bfs["nodes_expanded"],
            "Score": bfs["score"],
        })

    if comp_rows:
        df_comp = pd.DataFrame(comp_rows)
        chart_c1, chart_c2 = st.columns(2)

        with chart_c1:
            fig_cost = px.bar(
                df_comp,
                x="Algorithm",
                y="Route Cost",
                color="Algorithm",
                color_discrete_sequence=["#22C55E", "#A855F7"],
                title="Route Cost Comparison (Lower is Better)",
            )
            fig_cost.update_layout(
                paper_bgcolor="#100A20",
                plot_bgcolor="#100A20",
                font_color="#FFFFFF",
                margin=dict(l=20, r=20, t=40, b=20),
            )
            st.plotly_chart(fig_cost, width="stretch")

        with chart_c2:
            fig_nodes = px.bar(
                df_comp,
                x="Algorithm",
                y="Nodes Expanded",
                color="Algorithm",
                color_discrete_sequence=["#22C55E", "#A855F7"],
                title="Search Efficiency (Nodes Expanded)",
            )
            fig_nodes.update_layout(
                paper_bgcolor="#100A20",
                plot_bgcolor="#100A20",
                font_color="#FFFFFF",
                margin=dict(l=20, r=20, t=40, b=20),
            )
            st.plotly_chart(fig_nodes, width="stretch")

    # Step-by-Step Corridor Walkthrough
    active_route = astar.get("route") if astar else (bfs.get("route") if bfs else None)
    if active_route:
        st.markdown("### 🚶 Step-by-Step Evacuation Path Walkthrough")
        steps = []
        cum_cost = 0
        crowded = state.get("crowded_locations", [])

        for i in range(len(active_route) - 1):
            u, v = active_route[i], active_route[i + 1]
            base_cost = CAMPUS_GRAPH[u][v]
            penalty = 5 if v in crowded else 0
            step_cost = base_cost + penalty
            cum_cost += step_cost
            steps.append({
                "Step #": i + 1,
                "From": f"{u} ({LOCATIONS[u]})",
                "To": f"{v} ({LOCATIONS[v]})",
                "Base Corridor Weight": base_cost,
                "Crowd Congestion Penalty": f"+{penalty}" if penalty else "0",
                "Total Step Effort": step_cost,
                "Cumulative Travel Effort": cum_cost,
                "Corridor Status": "🟢 Clear & Verified",
            })
        st.dataframe(pd.DataFrame(steps), width="stretch")

    # Dynamic Route Recalculation Section
    st.markdown("<hr style='border-color:#3A2854; margin:22px 0;'>", unsafe_allow_html=True)
    st.markdown("### 🔄 Dynamic Route Recalculation (In-Flight Obstacle Injection)")

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        add_blocked = st.multiselect(
            "Dynamically Block Additional Corridors",
            [
                (u, v) for u, nbrs in CAMPUS_GRAPH.items()
                for v in nbrs if u < v
            ],
            format_func=lambda e: f"{e[0]} ({LOCATIONS[e[0]]}) ↔ {e[1]} ({LOCATIONS[e[1]]})",
            help="Simulate a structural collapse or smoke barrier closing off a path.",
        )
    with col_d2:
        new_exits = st.multiselect(
            "Permitted Operational Exits",
            EMERGENCY_EXITS,
            default=state.get("available_exits", EMERGENCY_EXITS),
            format_func=lambda x: f"{x} — {LOCATIONS[x]}",
            help="Simulate closure of an exit gate.",
        )

    if st.button("⚡ RECALCULATE EVACUATION ROUTES", width="stretch"):
        all_blocked = list(state.get("blocked_edges", [])) + list(add_blocked)
        updated_res = process_emergency(
            start=state.get("start"),
            emergency_type=state.get("emergency_type"),
            emergency_location=state.get("emergency_location"),
            blocked_edges=all_blocked,
            crowded_locations=state.get("crowded_locations", []),
            restricted_locations=state.get("restricted_locations", []),
            available_exits=new_exits,
        )
        st.session_state.last_result = updated_res
        upd_astar = updated_res.get("routes", {}).get("A*")

        if upd_astar:
            st.success(f"✅ Route adapted: {' → '.join(upd_astar['route'])} (New Cost: {upd_astar['route_cost']})")
        else:
            st.error("⚠️ All viable evacuation pathways are now exhausted.")
        st.rerun()

    render_disclaimer()
