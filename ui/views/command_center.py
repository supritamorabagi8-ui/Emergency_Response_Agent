"""
Command Center Dashboard View for Emergency Operations Command Center.
Features futuristic hero section, statistical cards, real-time activity stream, and quick navigation.
"""

import pandas as pd
import streamlit as st

from environment.campus_graph import CAMPUS_GRAPH, EMERGENCY_EXITS, LOCATIONS
from ui.audio import trigger_test_alert
from ui.theme import render_disclaimer, render_html, render_page_header, render_route_card, render_stat_card


def render_command_center():
    """Render the primary futuristic Command Center Dashboard."""
    # 1. Futuristic Hero Section
    render_html("""
    <div class="hero-command">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;">
            <div>
                <h1 class="hero-title">
                    <span>🚨</span> Emergency Operations Command Center
                </h1>
                <p class="hero-subtitle">
                    Intelligent Emergency Detection, Safe Route Planning & Campus Response Management
                </p>
            </div>
            <span class="status-pill pill-violet">✦ MATRIX CONTROL ACTIVE</span>
        </div>
    </div>
    """)

    # 2. Compute Ground-Truth Statistics
    total_locations = len(LOCATIONS)
    total_exits = len(EMERGENCY_EXITS)

    last_res = st.session_state.get("last_result")
    state = last_res.get("emergency_state", {}) if last_res else {}

    blocked_corridors_count = len(state.get("blocked_edges", []))
    active_incidents = len([
        inc for inc in st.session_state.get("incidents", {}).values()
        if inc.get("status") != "Resolved"
    ])
    total_analyses = len(st.session_state.get("alert_history", []))

    # Safe locations count
    unsafe_set = set(state.get("restricted_locations", []))
    if state.get("emergency_location"):
        unsafe_set.add(state.get("emergency_location"))
    safe_locations_count = total_locations - len(unsafe_set)

    # Route Availability
    routes = last_res.get("routes", {}) if last_res else {}
    astar = routes.get("A*")
    bfs = routes.get("BFS")
    route_status = "Available (Optimal)" if astar else ("Available (BFS)" if bfs else "Awaiting Analysis")

    # 3. Statistical Grid Cards with Purple Gradients
    col1, col2, col3, col4 = st.columns(4)
    render_stat_card(col1, "TOTAL CAMPUS LOCATIONS", str(total_locations), "All 8 Configured Zones", "8 Nodes")
    render_stat_card(col2, "ACTIVE INCIDENTS", str(active_incidents), "Unresolved Contingencies", "Live")
    render_stat_card(col3, "SAFE LOCATIONS", f"{safe_locations_count} / {total_locations}", "Clear from Hazard Epizones", "Secured")
    render_stat_card(col4, "BLOCKED CORRIDORS", str(blocked_corridors_count), "Impassable Connections", "Restricted")

    col5, col6, col7, col8 = st.columns(4)
    render_stat_card(col5, "AVAILABLE EXITS", str(total_exits), "Primary Portals G1 & G2", "Nominal")
    render_stat_card(col6, "SYSTEM STATUS", "OPERATIONAL", "Inference & Graph Active", "Online")
    render_stat_card(col7, "ROUTE AVAILABILITY", "RESOLVED" if astar else "PENDING", route_status, "AI Routing")
    render_stat_card(col8, "TOTAL SIMULATIONS", str(total_analyses), "Session Benchmark Runs", "Tracked")

    st.markdown("<hr style='border-color:#3A2854; margin:22px 0;'>", unsafe_allow_html=True)

    # 4. Quick Action Controls
    st.markdown("### ⚡ Quick Navigation & Operational Commands")
    q1, q2, q3, q4 = st.columns(4)
    with q1:
        if st.button("🚨 New Emergency Analysis", width="stretch"):
            st.session_state.nav_page = "2. Emergency Analysis"
            st.rerun()
    with q2:
        if st.button("🗺️ Interactive Campus Map", width="stretch"):
            st.session_state.nav_page = "3. Live Campus Map"
            st.rerun()
    with q3:
        if st.button("🛣️ Route Planning & Detours", width="stretch"):
            st.session_state.nav_page = "4. Route Planning"
            st.rerun()
    with q4:
        if st.button("🔔 Trigger Siren Drill", width="stretch"):
            trigger_test_alert()
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # 5. Dual Dashboard Panels: Activity Timeline & Route Status
    c_left, c_right = st.columns([3, 2])

    with c_left:
        history = st.session_state.get("alert_history", [])
        activity_items_html = ""

        if history:
            for item in history[:5]:
                sev = item.get("severity", "Medium")
                pill_class = (
                    "pill-critical" if sev == "Critical" else (
                        "pill-high" if sev == "High" else "pill-medium"
                    )
                )
                route_str = "🟢 Route Found" if item.get("route_found") else "🔴 No Route"
                ack_str = "✅ Acknowledged" if item.get("acknowledged") else "⏳ Unacknowledged"

                activity_items_html += f"""
                <div style="background:#100A20; border:1px solid #3A2854; border-radius:10px; padding:12px; margin-bottom:10px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <strong style="color:#FFFFFF; font-size:14px;">{item.get('type')} Incident</strong>
                        <span class="status-pill {pill_class}">{sev}</span>
                    </div>
                    <div style="font-size:12.5px; color:#FFFFFF; margin-top:6px;">
                        Epicenter: <strong style="color:#FFFFFF;">{item.get('location')}</strong> &nbsp;|&nbsp; 
                        Time: <span style="color:#FFFFFF;">{item.get('timestamp')}</span> &nbsp;|&nbsp; 
                        <span style="color:#FFFFFF;">{route_str}</span> &nbsp;|&nbsp; <span style="color:#FFFFFF;">{ack_str}</span>
                    </div>
                </div>
                """
        else:
            activity_items_html = "<div style='color:#FFFFFF; font-size:13px;'>No active emergency events recorded in current session memory.</div>"

        render_html(f"""
        <div class="glass-card">
            <div class="card-header">📋 Recent Emergency Activity Stream</div>
            {activity_items_html}
        </div>
        """, container=c_left)

    with c_right:
        if last_res and last_res.get("success"):
            if astar:
                render_route_card(c_right, "recommended", astar, title="🟢 Active Evacuation Route", subtitle="Real-time Dispatch Status")
            elif bfs:
                render_route_card(c_right, "alternative", bfs, title="🟣 Active Candidate Route (BFS)", subtitle="Real-time Dispatch Status")
            else:
                render_route_card(c_right, "recommended", None, title="⚠️ No Evacuation Route", subtitle="Incident Epizone Compromised")
        else:
            render_html("""
            <div class="glass-card" style="border-left: 4px solid #8B5CF6;">
                <div class="card-header">📡 Current Route Status</div>
                <div style="background:#100A20; border:1px solid #3A2854; border-radius:10px; padding:14px; color:#FFFFFF;">
                    <div style="font-size:14px; font-weight:700; color:#FFFFFF; margin-bottom:6px;">No Active Route Calculation in Memory</div>
                    <div style="font-size:12.5px; color:#B9AECF; line-height:1.6;">
                        Simulated campus routing engine is standing by in nominal mode. Navigate to <strong>Emergency Analysis</strong> to simulate environmental incidents and generate optimal evacuation routes.
                    </div>
                </div>
            </div>
            """, container=c_right)

    render_disclaimer()
