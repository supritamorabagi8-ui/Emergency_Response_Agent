"""
=============================================================================
EMERGENCY RESPONSE AGENT AI — FUTURISTIC COMMAND CENTER
Main Application Entry Point & Navigation Router
Inspired by Elite Cybernetic Command & Control Interfaces
=============================================================================
"""

import streamlit as st

# Configure wide page layout and branding
st.set_page_config(
    page_title="Emergency Response Agent AI | Operations Command Center",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Import internal modular components
from ui.theme import inject_custom_css, render_html, render_top_header
from ui.state_manager import init_session_state
from ui.audio import render_audio_controller

from ui.views.command_center import render_command_center
from ui.views.emergency_analysis import render_emergency_analysis
from ui.views.campus_map_view import render_campus_map_view
from ui.views.route_planning import render_route_planning
from ui.views.incident_mgmt import render_incident_mgmt
from ui.views.risk_monitoring import render_risk_monitoring
from ui.views.what_if_view import render_what_if_view
from ui.views.performance_view import render_performance_view
from ui.views.reports_view import render_reports_view
from ui.views.settings_view import render_settings_view

# 1. Initialize persistent session state
init_session_state()

# 2. Inject global custom design system CSS (Dark Purple / Neon Violet Theme)
inject_custom_css()

# 3. Render Top Executive Header Bar
render_top_header()

# 4. Render Active Emergency Siren & Alert Banner Controller
render_audio_controller()

# 5. Render Futuristic Left Sidebar Navigation (10 Core Command Pages)
with st.sidebar:
    render_html(
        """
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:14px; padding: 4px 6px;">
            <div style="font-size:32px; filter: drop-shadow(0 0 10px rgba(168, 85, 247, 0.6));">🚨</div>
            <div>
                <div style="font-size:16px; font-weight:800; color:#FFFFFF; letter-spacing:0.5px;">RESPONSE AI</div>
                <div style="font-size:11px; font-weight:700; color:#E879F9; letter-spacing:0.8px;">COMMAND MATRIX</div>
            </div>
        </div>
        """
    )

    render_html("<hr style='border-color:#3A2854; margin:8px 0 16px 0;'>")

    # Exactly the 10 requested navigation sections
    nav_options = [
        "1. Command Center",
        "2. Emergency Analysis",
        "3. Live Campus Map",
        "4. Route Planning",
        "5. Incident Management",
        "6. Risk Monitoring",
        "7. What-If Simulation",
        "8. Performance Analytics",
        "9. Emergency Reports",
        "10. System Settings",
    ]

    current_idx = 0
    if st.session_state.nav_page in nav_options:
        current_idx = nav_options.index(st.session_state.nav_page)

    selected_page = st.radio(
        "OPERATIONAL NAVIGATION",
        nav_options,
        index=current_idx,
        label_visibility="collapsed",
    )
    st.session_state.nav_page = selected_page

    render_html("<hr style='border-color:#3A2854; margin:16px 0;'>")

    # Real-Time Operational Badges
    st.markdown("#### 📡 OPERATIONAL TELEMETRY")
    st.markdown("🟢 **System Health:** 100% Nominal")
    st.markdown("🟣 **BFS Hop Engine:** Online")
    st.markdown("🟢 **Dijkstra Cost Engine:** Online")
    st.markdown(f"👤 **Access Level:** `{st.session_state.get('user_role', 'Administrator')}`")

    render_html("<hr style='border-color:#3A2854; margin:16px 0;'>")
    st.caption("Campus Emergency Response Agent AI")
    st.caption("Academic Project • 2026")


# 6. Page Router Dispatcher
PAGE_ROUTING = {
    "1. Command Center": render_command_center,
    "2. Emergency Analysis": render_emergency_analysis,
    "3. Live Campus Map": render_campus_map_view,
    "4. Route Planning": render_route_planning,
    "5. Incident Management": render_incident_mgmt,
    "6. Risk Monitoring": render_risk_monitoring,
    "7. What-If Simulation": render_what_if_view,
    "8. Performance Analytics": render_performance_view,
    "9. Emergency Reports": render_reports_view,
    "10. System Settings": render_settings_view,
}

# Execute active view function
render_fn = PAGE_ROUTING.get(st.session_state.nav_page, render_command_center)
render_fn()

# 7. Global Futuristic Footer
render_html("<hr style='border-color:#3A2854; margin:36px 0 16px 0;'>")
render_html(
    """
    <div style="text-align:center; color:#FFFFFF; font-size:12px; padding-bottom:24px;">
        🚨 <strong style="color:#FFFFFF;">Emergency Response Agent AI</strong> — Futuristic Campus Emergency Operations Command Center<br>
        <span style="color:#FFFFFF;">Simulated Artificial Intelligence Decision-Support System • Academic Demonstration 2026</span>
    </div>
    """
)
