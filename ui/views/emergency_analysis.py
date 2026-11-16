"""
Emergency Analysis View for Emergency Response Command Center.
Allows operator to configure environmental hazards, activate response, and evaluate routes.
"""

import pandas as pd
import streamlit as st

from environment.campus_graph import CAMPUS_GRAPH, EMERGENCY_EXITS, LOCATIONS, START_LOCATIONS
from services.emergency_service import process_emergency
from ui.speech import get_announcement_text, render_voice_announcer
from ui.state_manager import register_new_incident
from ui.theme import render_disclaimer, render_html, render_page_header, render_route_card


def render_emergency_analysis():
    """Render the Emergency Analysis and Threat Assessment Page."""
    render_page_header(
        "🚨 Emergency Threat Detection & Analysis",
        "Configure Environmental Incident Parameters, Simulate Hazards, and Compute Evacuation Directives",
        badge_text="ANALYSIS ENGINE ACTIVE",
    )

    location_options = list(LOCATIONS.keys())
    corridor_options = {}

    for loc, neighbors in CAMPUS_GRAPH.items():
        for neighbor in neighbors:
            edge = tuple(sorted((loc, neighbor)))
            if edge not in corridor_options:
                corridor_options[edge] = f"{edge[0]} ({LOCATIONS[edge[0]]}) ↔ {edge[1]} ({LOCATIONS[edge[1]]})"

    with st.form("emergency_analysis_form_v2"):
        st.markdown("### 1. Incident Origin & Threat Classification")
        col1, col2 = st.columns(2)

        with col1:
            start = st.selectbox(
                "Evacuation Starting Point",
                START_LOCATIONS,
                format_func=lambda x: f"{x} — {LOCATIONS[x]}",
                help="Building where evacuating students/staff are located.",
            )

            emergency_type = st.selectbox(
                "Emergency Classification Type",
                ["fire", "medical", "security", "other"],
                format_func=lambda x: {
                    "fire": "🔥 Fire Emergency",
                    "medical": "🚑 Medical Emergency",
                    "security": "🛡️ Security Threat",
                    "other": "⚠️ General Incident",
                }[x],
            )

            severity = st.select_slider(
                "Incident Severity Level",
                options=["Low", "Medium", "High", "Critical"],
                value="High",
            )

        with col2:
            emergency_location = st.selectbox(
                "Reported Hazard Epicenter",
                ["None"] + location_options,
                format_func=lambda x: "Not Specified / Diffuse" if x == "None" else f"{x} — {LOCATIONS[x]}",
                help="Building or zone experiencing direct hazard.",
            )

            available_exits = st.multiselect(
                "Operational Emergency Exits",
                EMERGENCY_EXITS,
                default=EMERGENCY_EXITS,
                format_func=lambda x: f"{x} — {LOCATIONS[x]}",
                help="Exits open and unobstructed for evacuation.",
            )

        st.markdown("<hr style='border-color:#3A2854; margin:16px 0;'>", unsafe_allow_html=True)
        st.markdown("### 2. Environmental Obstacles & Bottlenecks")

        col3, col4 = st.columns(2)
        with col3:
            crowded = st.multiselect(
                "Crowded Locations (+5 Travel Cost Penalty)",
                location_options,
                format_func=lambda x: f"{x} — {LOCATIONS[x]}",
                help="Dense crowds that impede rapid movement.",
            )

            restricted = st.multiselect(
                "Security Restricted Zones (Strict No-Entry)",
                location_options,
                format_func=lambda x: f"{x} — {LOCATIONS[x]}",
                help="Quarantined buildings or perimeter lockdowns.",
            )

        with col4:
            blocked = st.multiselect(
                "Blocked Campus Corridors (Impassable Pathways)",
                list(corridor_options.keys()),
                format_func=lambda x: corridor_options[x],
                help="Corridors that cannot be traversed.",
            )

        # Glowing activation button
        submit = st.form_submit_button("⚡ INITIATE EMERGENCY ROUTE PLANNING", width="stretch")

    if submit:
        actual_em_loc = None if emergency_location == "None" else emergency_location

        # Call existing backend service
        result = process_emergency(
            start=start,
            emergency_type=emergency_type,
            emergency_location=actual_em_loc,
            blocked_edges=list(blocked),
            crowded_locations=crowded,
            restricted_locations=restricted,
            available_exits=available_exits,
        )

        st.session_state.last_result = result

        if result.get("success"):
            routes = result.get("routes", {})
            decision = result.get("decision", {})
            state = result.get("emergency_state", {})

            bfs = routes.get("BFS")
            astar = routes.get("A*")
            route_found = (bfs is not None) or (astar is not None)

            # Register incident in state manager
            inc_id, alert_id = register_new_incident(
                emergency_type=emergency_type,
                start=start,
                emergency_location=actual_em_loc,
                severity=severity,
                routes=routes,
                decision=decision,
                state=state,
            )

            if route_found:
                st.balloons()
                exit_str = astar['route'][-1] if astar else bfs['route'][-1]
                render_html(f"""
                <div class="success-banner-custom">
                    <div style="font-size:32px;">✦</div>
                    <div>
                        <div style="font-size:20px; font-weight:800; color:#A7F3D0;">
                            CANDIDATE EVACUATION ROUTE IDENTIFIED
                        </div>
                        <div style="font-size:13.5px; color:#FFFFFF; margin-top:4px;">
                            Incident Registered: <strong style="color:#FFFFFF;">{inc_id}</strong> &nbsp;|&nbsp;
                            Alert Broadcast: <strong style="color:#FFFFFF;">{alert_id}</strong> &nbsp;|&nbsp;
                            Operational Exit: <strong style="color:#22C55E;">Gate {exit_str}</strong>
                        </div>
                    </div>
                </div>
                """)
            else:
                render_html("""
                <div class="alert-banner-active">
                    <div>
                        <div class="alert-banner-title">
                            ⚠️ NO CANDIDATE SAFE ROUTE FOUND!
                        </div>
                        <div style="font-size:14px; color:#FFFFFF; margin-top:6px;">
                            All candidate pathways to designated emergency exits are compromised or blocked.
                            Follow tactical sheltering directives and await security response.
                        </div>
                    </div>
                </div>
                """)
        else:
            st.error(f"Validation Error: {result.get('message')}")

    # Display Calculated Directives & Routes
    res = st.session_state.get("last_result")
    if res and res.get("success"):
        st.markdown("<hr style='border-color:#3A2854; margin:24px 0;'>", unsafe_allow_html=True)
        st.markdown("### 📋 AI Decision-Support Directives & Route Analysis")

        decision = res.get("decision", {})
        routes = res.get("routes", {})
        bfs = routes.get("BFS")
        astar = routes.get("A*")

        # Decision Directives
        c_rules, c_recs = st.columns([1, 2])
        with c_rules:
            matched = decision.get("matched_rules", [])
            rules_html = ""
            if matched:
                for r in matched:
                    rules_html += f"<div style='margin-bottom:6px;'>• <span class='status-pill pill-violet'>{r}</span></div>"
            else:
                rules_html = "<div style='color:#FFFFFF; font-size:13px;'>No specialized rules matched.</div>"

            render_html(f"""
            <div class="glass-card">
                <div class="card-header">📜 Triggered Rules</div>
                {rules_html}
            </div>
            """, container=c_rules)

        with c_recs:
            recs_html = ""
            for rec in decision.get("recommendations", []):
                recs_html += f"<div style='color:#FFFFFF; font-size:13.5px; margin-bottom:8px;'>• <strong>{rec}</strong></div>"

            render_html(f"""
            <div class="glass-card">
                <div class="card-header">🛡️ Tactical Response Directives</div>
                {recs_html}
            </div>
            """, container=c_recs)

        # Route Cards
        r_col1, r_col2 = st.columns(2)
        render_route_card(r_col1, "recommended", astar)
        render_route_card(r_col2, "alternative", bfs)

        # Multilingual Voice Announcement Option
        st.markdown("<hr style='border-color:#3A2854; margin:16px 0;'>", unsafe_allow_html=True)
        st.markdown("### 📢 Broadcast Simulated Evacuation Announcement")
        st_state = res.get("emergency_state", {})
        em_type_str = st_state.get("emergency_type", "fire")
        loc_str = LOCATIONS.get(st_state.get("emergency_location") or st_state.get("start"), "Campus")

        l_col1, l_col2 = st.columns([1, 3])
        with l_col1:
            lang = st.radio("Broadcast Language", ["English (en-US)", "Kannada (kn-IN)"])
            lang_code = "kn-IN" if "Kannada" in lang else "en-US"
        with l_col2:
            ann_text = get_announcement_text(em_type_str, loc_str, lang_code)
            render_voice_announcer(ann_text, lang_code)

    render_disclaimer()
