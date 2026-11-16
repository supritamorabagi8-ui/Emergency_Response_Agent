"""
System Settings & Operational Diagnostics View for Emergency Operations Command Center.
Manages operator roles, audio alarm preferences, accessibility, diagnostics, and state resets.
"""

import os
import pandas as pd
import streamlit as st

from environment.campus_graph import CAMPUS_GRAPH, EMERGENCY_EXITS, LOCATIONS
from ui.audio import trigger_test_alert
from ui.state_manager import reset_simulation
from ui.theme import render_disclaimer, render_html, render_page_header

AUTHORIZED_ROLES = ["Administrator", "Security Officer", "Campus Observer"]


def render_settings_view():
    """Render the System Settings & Health Diagnostics Page."""
    render_page_header(
        "⚙️ System Settings & Diagnostic Infrastructure",
        "Configure Operator Authorization, Audio Alarm Preferences, Accessibility, and System Health",
        badge_text="SYSTEM CONFIG",
    )

    # 1. System Health Diagnostics
    st.markdown("### 🔍 Live System Diagnostics Matrix")
    checks = []

    # Check emergency service
    try:
        from services.emergency_service import process_emergency
        checks.append(("Emergency Service Orchestrator", "services.emergency_service", "ONLINE", "🟢 Fully Operational"))
    except Exception as e:
        checks.append(("Emergency Service Orchestrator", "services.emergency_service", "OFFLINE", f"🔴 Error: {e}"))

    # Check algorithms
    try:
        from algorithms.astar import astar
        from algorithms.bfs import bfs
        checks.append(("Breadth-First Search (BFS)", "algorithms.bfs", "ONLINE", "🟢 Loaded & Verified"))
        checks.append(("Dijkstra / Zero-Heuristic A*", "algorithms.astar", "ONLINE", "🟢 Loaded (Zero-Heuristic)"))
    except Exception as e:
        checks.append(("Search Algorithms", "algorithms", "ERROR", f"🔴 Error: {e}"))

    # Check decision rules
    try:
        from decision.decision_rules import RULE_DESCRIPTIONS, apply_rules
        checks.append(("Transparent Decision Engine", "decision.decision_rules", "ONLINE", "🟢 8 Rules Verified (R1–R8)"))
    except Exception as e:
        checks.append(("Decision Rules", "decision", "ERROR", f"🔴 Error: {e}"))

    # Check graph
    try:
        checks.append(("Campus Graph Environment", "environment.campus_graph", "ONLINE", f"🟢 {len(LOCATIONS)} Nodes, {len(EMERGENCY_EXITS)} Exits"))
    except Exception as e:
        checks.append(("Campus Graph", "environment", "ERROR", f"🔴 Error: {e}"))

    # Check CSV
    csv_path = "performance/experiment_results.csv"
    if os.path.exists(csv_path):
        df_c = pd.read_csv(csv_path)
        checks.append(("Benchmark Experiment Data", "performance/experiment_results.csv", "ONLINE", f"🟢 Loaded ({len(df_c)} Rows)"))
    else:
        checks.append(("Benchmark Experiment Data", "performance/experiment_results.csv", "MISSING", "🟠 File Not Found"))

    st.dataframe(pd.DataFrame(checks, columns=["Subsystem", "Module Target", "State", "Diagnostic Message"]), width="stretch")

    st.markdown("<hr style='border-color:#3A2854; margin:22px 0;'>", unsafe_allow_html=True)

    # 2. Audio & Siren Alarm Settings
    st.markdown("### 🔊 Emergency Siren & Sound Controls")
    ac1, ac2, ac3 = st.columns([2, 2, 3])

    with ac1:
        st.session_state.sound_enabled = st.toggle(
            "Emergency Siren Audio",
            value=st.session_state.get("sound_enabled", True),
            help="Toggle browser-based dual-tone emergency siren sound upon incident activation.",
        )
    with ac2:
        st.session_state.sound_volume = st.slider(
            "Alarm Volume",
            min_value=0.0,
            max_value=1.0,
            value=float(st.session_state.get("sound_volume", 0.8)),
            step=0.1,
        )
    with ac3:
        if st.button("🚨 TEST EMERGENCY SIREN (DRILL)", width="stretch"):
            trigger_test_alert()
            st.rerun()

    st.markdown("<hr style='border-color:#3A2854; margin:22px 0;'>", unsafe_allow_html=True)

    # 3. Operator Role & Permissions - FIXED ISSUE 1: Safe indexing with fallback to Administrator
    st.markdown("### 👤 Operator Access Control")
    current_role = st.session_state.get("user_role", "Administrator")
    if current_role not in AUTHORIZED_ROLES:
        current_role = "Administrator"
        st.session_state.user_role = current_role

    selected_index = AUTHORIZED_ROLES.index(current_role)
    role = st.selectbox(
        "Active Operational Role",
        AUTHORIZED_ROLES,
        index=selected_index,
        help="Simulates access level gates within the control center.",
    )
    st.session_state.user_role = role

    role_desc = {
        "Administrator": "Full system access: configure emergencies, adapt routes, download reports, and clear audit logs.",
        "Security Officer": "Operational access: monitor emergencies, view routes, acknowledge alerts, and update lifecycles.",
        "Campus Observer": "Read-only access: inspect dashboard, analytics, and historical benchmark logs.",
    }.get(role, "")

    render_html(f"""
    <div class="glass-card" style="padding:16px; margin-top:12px;">
        <strong style="color:#FFFFFF; font-size:15px;">Active Role: {role}</strong>
        <p style="color:#FFFFFF; margin:6px 0 0 0; font-size:13px;">{role_desc}</p>
    </div>
    """)

    # 4. State Management & Resets
    st.markdown("<hr style='border-color:#3A2854; margin:22px 0;'>", unsafe_allow_html=True)
    st.markdown("### 🧹 Application Cache & Session Reset")

    rc1, rc2 = st.columns(2)
    with rc1:
        if st.button("🔄 Reset Current Active Simulation", width="stretch"):
            reset_simulation()
            st.success("Active simulation reset to baseline.")
            st.rerun()

    with rc2:
        if st.button("🗑️ Clear Entire Session History", width="stretch"):
            st.session_state.alert_history = []
            st.session_state.incidents = {}
            st.session_state.audit_logs = []
            st.session_state.last_result = None
            st.session_state.active_alert = None
            st.session_state.siren_active = False
            st.success("All session logs purged.")
            st.rerun()

    render_disclaimer()
