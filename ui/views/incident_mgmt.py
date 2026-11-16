"""
Incident Management View for Emergency Operations Command Center.
Tracks incident lifecycle progression (Reported -> Analyzing -> Route Assigned -> Response in Progress -> Resolved).
"""

import pandas as pd
import streamlit as st

from ui.state_manager import acknowledge_current_alert, log_audit_event
from ui.theme import render_disclaimer, render_html, render_page_header


def render_incident_mgmt():
    """Render the Incident Management & Response Coordination Page."""
    render_page_header(
        "📋 Campus Incident Lifecycle Management",
        "Orchestrate Simulated Emergency Lifecycles, Coordinate Response Stages, and Maintain Response Accountability",
        badge_text="INCIDENT CONTROL",
    )

    incidents = st.session_state.get("incidents", {})
    if not incidents:
        st.info("No emergency incidents registered in current session memory. Initiate an incident via 'Emergency Analysis'.")
        render_disclaimer()
        return

    # Incident Selection
    sel_id = st.selectbox(
        "Select Active Incident Dossier",
        list(incidents.keys()),
        index=0,
    )
    inc = incidents[sel_id]

    sev = inc.get("severity", "High")
    pill_class = (
        "pill-critical" if sev == "Critical" else (
            "pill-high" if sev == "High" else "pill-medium"
        )
    )

    # Incident Header Card
    routes = inc.get("routes", {})
    astar = routes.get("A*")
    exit_assigned = f"Gate {astar['route'][-1]}" if astar else "Unassigned / None"
    route_str = ' → '.join(astar['route']) if astar else 'None'

    render_html(f"""
    <div class="glass-card" style="border-left: 4px solid #A855F7;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
            <div>
                <h3 style="margin:0; color:#FFFFFF;">Incident Dossier: {inc['id']}</h3>
                <div style="font-size:13.5px; color:#FFFFFF; margin-top:6px;">
                    Type: <strong style="color:#FFFFFF;">{inc['type']} Emergency</strong> &nbsp;|&nbsp; 
                    Location: <strong style="color:#FFFFFF;">{inc['emergency_location']}</strong> &nbsp;|&nbsp; 
                    Activation: <span style="color:#FFFFFF;">{inc['timestamp']}</span>
                </div>
            </div>
            <div style="display:flex; gap:8px;">
                <span class="status-pill {pill_class}">{sev} SEVERITY</span>
                <span class="status-pill pill-violet">{inc['status']}</span>
            </div>
        </div>
        <div style="margin-top:14px; padding-top:12px; border-top:1px solid #3A2854; font-size:13.5px; color:#FFFFFF;">
            Assigned Evacuation Portal: <strong style="color:#22C55E;">{exit_assigned}</strong> &nbsp;|&nbsp; 
            Candidate Route: <code style="color:#A7F3D0; font-size:13px; font-weight:bold;">{route_str}</code>
        </div>
    </div>
    """)

    # 5-Stage Incident Lifecycle Timeline
    st.markdown("### 🔄 Incident Lifecycle Timeline Progression")
    stages = [
        ("Reported", "Initial detection & threat logged"),
        ("Analyzing", "Environmental graph & constraint evaluation"),
        ("Route Assigned", "Verified evacuation path computed"),
        ("Response in Progress", "Security & medical coordination dispatched"),
        ("Resolved", "Perimeter secured & threat normalized"),
    ]

    current_status = inc.get("status", "Route Assigned")
    active_idx = 2  # default to Route Assigned if route found
    if "Reported" in current_status:
        active_idx = 0
    elif "Analyzing" in current_status:
        active_idx = 1
    elif "Route Assigned" in current_status or "Candidate Route" in current_status:
        active_idx = 2
    elif "Response in Progress" in current_status or "Acknowledged" in current_status:
        active_idx = 3
    elif "Resolved" in current_status:
        active_idx = 4

    cols = st.columns(len(stages))
    for idx, (stg_name, desc) in enumerate(stages):
        col = cols[idx]
        is_past = idx <= active_idx
        is_current = idx == active_idx

        border_c = "#22C55E" if is_past else "#3A2854"
        bg_c = "rgba(34, 197, 94, 0.2)" if is_current else ("#17102A" if is_past else "#100A20")
        icon = "✦" if is_past else "○"

        render_html(f"""
        <div style="background:{bg_c}; border:1px solid {border_c}; border-radius:12px; padding:14px; text-align:center; min-height:120px;">
            <div style="font-size:18px; color:#E879F9;">{icon}</div>
            <div style="font-size:13px; font-weight:700; color:#FFFFFF; margin-top:6px;">{stg_name}</div>
            <div style="font-size:11.5px; color:#FFFFFF; margin-top:4px;">{desc}</div>
        </div>
        """, container=col)

    st.markdown("<br>", unsafe_allow_html=True)

    # Incident Response Controls
    st.markdown("### 🎛️ Tactical Incident State Controls")
    b1, b2, b3 = st.columns(3)

    with b1:
        if st.button("🔔 Acknowledge & Dispatch Response", width="stretch"):
            acknowledge_current_alert()
            inc["status"] = "Response in Progress"
            log_audit_event("INCIDENT_DISPATCH", f"Operator dispatched response team to {inc['id']}.", inc["id"])
            st.success(f"Incident {inc['id']} moved to 'Response in Progress'.")
            st.rerun()

    with b2:
        if st.button("🛡️ Re-Analyze Active Hazards", width="stretch"):
            st.session_state.nav_page = "2. Emergency Analysis"
            st.rerun()

    with b3:
        if st.button("🏁 Mark Incident as Resolved", width="stretch"):
            inc["status"] = "Resolved"
            log_audit_event("INCIDENT_RESOLVED", f"Operator closed and resolved {inc['id']}.", inc["id"])
            st.success(f"Incident {inc['id']} has been officially resolved.")
            st.rerun()

    render_disclaimer()
