"""
Risk Monitoring & Hazard Assessment View for Emergency Operations Command Center.
Displays classified risk levels across campus nodes, explaining hazard causality and safe zones.
"""

import pandas as pd
import streamlit as st

from environment.campus_graph import CAMPUS_GRAPH, EMERGENCY_EXITS, LOCATIONS
from ui.graph_visualizer import create_campus_figure
from ui.theme import render_disclaimer, render_html, render_page_header


def render_risk_monitoring():
    """Render the Campus Risk Monitoring & Threat Zoning Page."""
    render_page_header(
        "🛡️ Real-Time Campus Risk Monitoring & Threat Zoning",
        "Spatial Danger Dispersion Analysis, Hazard Causality, and Secure Zone Identification",
        badge_text="THREAT INTELLIGENCE",
    )

    last_res = st.session_state.get("last_result")
    state = last_res.get("emergency_state", {}) if last_res else {}

    em_loc = state.get("emergency_location")
    blocked_edges = state.get("blocked_edges", [])
    crowded = state.get("crowded_locations", [])
    restricted = state.get("restricted_locations", [])

    # Display Risk Heatmap View
    st.markdown("### 🌡️ Spatial Danger Dispersion Heatmap")
    routes = last_res.get("routes", {}) if last_res else {}
    astar_route = routes.get("A*", {}).get("route") if routes.get("A*") else None

    fig = create_campus_figure(
        start=state.get("start"),
        emergency_location=em_loc,
        blocked_edges=blocked_edges,
        crowded_locations=crowded,
        restricted_locations=restricted,
        available_exits=state.get("available_exits", EMERGENCY_EXITS),
        astar_route=astar_route,
        show_heatmap=True,
        title="Campus Risk Heatmap & Danger Contour Analysis",
    )
    st.plotly_chart(fig, width="stretch")

    # Detailed Zone Risk Classification Cards
    st.markdown("### 🔍 Zone-by-Zone Risk Diagnostics")
    grid_cols = st.columns(4)

    for idx, (nid, name) in enumerate(LOCATIONS.items()):
        col = grid_cols[idx % 4]

        risk_level = "LOW / SAFE"
        pill_class = "pill-safe"
        reason = "Normal structural integrity and open corridor connectivity."

        if nid == em_loc:
            risk_level = "CRITICAL HAZARD"
            pill_class = "pill-critical"
            reason = "Reported epicenter of active emergency threat (Fire/Security)."
        elif nid in restricted:
            risk_level = "SECURITY RESTRICTED"
            pill_class = "pill-high"
            reason = "Quarantined by security enforcement; no personnel permitted."
        elif nid in crowded:
            risk_level = "ELEVATED CROWD"
            pill_class = "pill-medium"
            reason = "Heavy pedestrian congestion creates bottleneck (+5 travel cost penalty)."
        elif nid in EMERGENCY_EXITS:
            risk_level = "SECURED EXIT"
            pill_class = "pill-safe"
            reason = "Open evacuation portal leading out of campus grounds."

        render_html(f"""
        <div class="glass-card" style="padding:16px; margin-bottom:12px;">
            <div style="font-size:16px; font-weight:700; color:#FFFFFF;">Zone {nid}</div>
            <div style="font-size:12px; color:#E879F9; margin-bottom:8px; font-weight:600;">{name}</div>
            <span class="status-pill {pill_class}">{risk_level}</span>
            <div style="font-size:12px; color:#FFFFFF; margin-top:8px; line-height:1.5;">
                {reason}
            </div>
        </div>
        """, container=col)

    render_disclaimer()
