"""
=============================================================================
EMERGENCY RESPONSE AGENT AI — LIVE CAMPUS MAP VIEW
Interactive Topological Infrastructure Network with Real-Time Hazard Overlays,
Algorithmic Evacuation Routing, Interactive Zone Inspector & Building Directory.
=============================================================================
"""

import streamlit as st

from environment.campus_graph import (
    CAMPUS_GRAPH,
    EMERGENCY_EXITS,
    LOCATIONS,
)
from ui.graph_visualizer import (
    NODE_TYPES,
    create_campus_figure,
)
from ui.theme import (
    render_building_card,
    render_disclaimer,
    render_html,
    render_legend_card,
    render_page_header,
)


def render_campus_map_view():
    """Render the Interactive Live Campus Map View."""

    # 1. Page Header
    render_page_header(
        "🗺️ Live Campus Evacuation Map",
        "Interactive Topological Infrastructure Network with Real-Time Hazard Overlays, Algorithmic Routing & Zone Diagnostics",
        badge_text="LIVE MAP MATRIX",
    )

    # 2. Load Incident Telemetry
    last_res = st.session_state.get("last_result")
    state = last_res.get("emergency_state", {}) if last_res else {}
    routes = last_res.get("routes", {}) if last_res else {}

    bfs_data = routes.get("BFS")
    astar_data = routes.get("A*")

    bfs_route = bfs_data.get("route") if bfs_data and bfs_data.get("route") else None
    astar_route = astar_data.get("route") if astar_data and astar_data.get("route") else None

    start_loc = state.get("start")
    em_loc = state.get("emergency_location")
    blocked_edges = state.get("blocked_edges", [])
    crowded = state.get("crowded_locations", [])
    restricted = state.get("restricted_locations", [])
    available_exits = state.get("available_exits", EMERGENCY_EXITS)

    # 3. Telemetry Status Banner
    if last_res and last_res.get("success"):
        exit_badge = f"Gate {astar_route[-1]}" if astar_route else (f"Gate {bfs_route[-1]}" if bfs_route else "None")
        status_text = "Active Incident Loaded • Evacuation Trajectories Mapped" if (astar_route or bfs_route) else "Active Incident Loaded • No Safe Route Available"
        status_color = "#22C55E" if (astar_route or bfs_route) else "#EF4444"

        render_html(f"""
        <div style="background:#17102A; border:1px solid #3A2854; border-left:4px solid {status_color}; border-radius:12px; padding:12px 18px; margin-bottom:18px;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
                <div style="font-size:13.5px; color:#FFFFFF;">
                    <strong>Active Incident:</strong> <span style="color:#E879F9;">{state.get('emergency_type', 'General').upper()}</span> &nbsp;|&nbsp;
                    <strong>Origin:</strong> {start_loc} ({LOCATIONS.get(start_loc, 'N/A')}) &nbsp;|&nbsp;
                    <strong>Epicenter:</strong> <span style="color:#EF4444; font-weight:bold;">{em_loc or 'None'}</span> &nbsp;|&nbsp;
                    <strong>Target Exit:</strong> <span style="color:#22C55E; font-weight:bold;">{exit_badge}</span>
                </div>
                <span class="status-pill {'pill-safe' if (astar_route or bfs_route) else 'pill-critical'}">{status_text}</span>
            </div>
        </div>
        """)
    else:
        render_html("""
        <div style="background:#17102A; border:1px solid #3A2854; border-left:4px solid #8B5CF6; border-radius:12px; padding:12px 18px; margin-bottom:18px;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
                <div style="font-size:13.5px; color:#FFFFFF;">
                    <strong>Network Baseline Status:</strong> All 8 Campus Zones Passable • Nominal Security State
                </div>
                <span class="status-pill pill-violet">BASELINE MAP VIEW</span>
            </div>
        </div>
        """)

    # 4. Map Visualization Controls
    st.markdown("### 🎛️ Map Layer & Visualization Controls")
    f1, f2, f3 = st.columns(3)

    with f1:
        show_rec = st.checkbox("Show Recommended Route (Dijkstra / Zero-Heuristic A*)", value=True)
    with f2:
        show_alt = st.checkbox("Show Alternative Route (BFS Fewest Hops)", value=True)
    with f3:
        show_heat = st.checkbox("Show Risk Dispersion Heatmap", value=False)

    active_astar = astar_route if show_rec else None
    active_bfs = bfs_route if show_alt else None

    # 5. Interactive Plotly Campus Map
    st.markdown("### 🗺️ Campus Infrastructure & Evacuation Topology")

    fig = create_campus_figure(
        start=start_loc,
        emergency_location=em_loc,
        blocked_edges=blocked_edges,
        crowded_locations=crowded,
        restricted_locations=restricted,
        available_exits=available_exits,
        bfs_route=active_bfs,
        astar_route=active_astar,
        show_heatmap=show_heat,
        title="Campus Evacuation Network — Topological Control View",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": True, "responsive": True},
    )

    # 6. Map Legend
    render_legend_card()

    # 7. Interactive Campus Zone Inspector
    st.markdown("### 🔍 Interactive Campus Zone Inspector")
    st.caption("Select any campus location to inspect real-time safety status, structural type, and corridor weights.")

    inspector_options = ["Overview (All Zones)"] + [f"{nid} — {LOCATIONS[nid]}" for nid in LOCATIONS.keys()]
    selected_inspect = st.selectbox(
        "Select Campus Zone to Inspect",
        inspector_options,
        index=0,
        help="Inspect real-time telemetry and connectivity for a specific building.",
    )

    if selected_inspect != "Overview (All Zones)":
        sel_nid = selected_inspect.split(" — ")[0]
        sel_name = LOCATIONS[sel_nid]
        sel_info = NODE_TYPES.get(sel_nid, {})
        sel_type = sel_info.get("type", "Campus Facility")

        # Determine current zone status
        is_hazard = sel_nid == em_loc
        is_restricted = sel_nid in restricted
        is_crowded = sel_nid in crowded
        is_exit = sel_nid in EMERGENCY_EXITS
        is_start = sel_nid == start_loc
        is_on_rec = astar_route and sel_nid in astar_route
        is_on_alt = bfs_route and sel_nid in bfs_route

        if is_hazard:
            status_text = "🚨 CRITICAL HAZARD EPICENTER — Active Incident Focus"
            status_pill = '<span class="status-pill pill-critical">CRITICAL HAZARD</span>'
        elif is_restricted:
            status_text = "⛔ SECURITY RESTRICTED — Quarantined / Strict No Entry"
            status_pill = '<span class="status-pill pill-high">RESTRICTED</span>'
        elif is_crowded:
            status_text = "⚠️ HIGH CROWD DENSITY — +5 Travel Cost Penalty Applied"
            status_pill = '<span class="status-pill pill-medium">CROWD CONGESTION</span>'
        elif is_exit:
            status_text = "🚪 OPERATIONAL EVACUATION EXIT — Direct Path to Safety"
            status_pill = '<span class="status-pill pill-safe">EMERGENCY EXIT</span>'
        elif is_start:
            status_text = "📍 EVACUATION ORIGIN — Evacuee Assembly Point"
            status_pill = '<span class="status-pill pill-violet">STARTING POINT</span>'
        else:
            status_text = "🟢 SECURE & PASSABLE — Structural Integrity Intact"
            status_pill = '<span class="status-pill pill-safe">PASSABLE</span>'

        # Role in routing
        route_roles = []
        if is_on_rec:
            route_roles.append('<span style="color:#22C55E; font-weight:bold;">★ Recommended Safe Route Traversal</span>')
        if is_on_alt:
            route_roles.append('<span style="color:#A855F7; font-weight:bold;">✦ Alternative BFS Route Traversal</span>')
        route_role_str = " &nbsp;|&nbsp; ".join(route_roles) if route_roles else "Not utilized in current evacuation route"

        # Connections list
        conn_dict = CAMPUS_GRAPH.get(sel_nid, {})
        conn_items = []
        for nbr, dist in conn_dict.items():
            edge = tuple(sorted((sel_nid, nbr)))
            edge_blocked = edge in [tuple(sorted(e)) for e in blocked_edges]
            status_tag = '<span style="color:#EF4444; font-weight:bold;">[BLOCKED ❌]</span>' if edge_blocked else f'<span style="color:#A7F3D0;">({dist}m travel effort)</span>'
            conn_items.append(f"• <strong>Zone {nbr} ({LOCATIONS[nbr]}):</strong> {status_tag}")
        conn_list_html = "<br>".join(conn_items)

        render_html(f"""
        <div class="glass-card" style="border-left:4px solid #8B5CF6; margin-bottom:20px;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:12px; border-bottom:1px solid #3A2854; padding-bottom:10px;">
                <div>
                    <h3 style="margin:0; color:#FFFFFF; font-size:18px;">Zone {sel_nid} Dossier: {sel_name}</h3>
                    <div style="font-size:12.5px; color:#E879F9; margin-top:3px;">{sel_type}</div>
                </div>
                {status_pill}
            </div>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:14px; font-size:13px; color:#FFFFFF;">
                <div>
                    <div><strong>Operational Status:</strong> {status_text}</div>
                    <div style="margin-top:8px;"><strong>Evacuation Routing Role:</strong> {route_role_str}</div>
                    <div style="margin-top:8px;"><strong>Graph Degree:</strong> {len(conn_dict)} Direct Corridors</div>
                </div>
                <div style="background:#100A20; border:1px solid #3A2854; border-radius:10px; padding:12px;">
                    <div style="font-size:11.5px; font-weight:700; color:#B9AECF; text-transform:uppercase; margin-bottom:6px;">Connected Corridors & Distance Weights:</div>
                    <div style="font-size:12.5px; line-height:1.7;">
                        {conn_list_html}
                    </div>
                </div>
            </div>
        </div>
        """)

    # 8. Campus Building Directory & Pathway Adjacency Grid
    st.markdown("### 🏢 Campus Building Directory & Pathway Adjacency")
    st.caption("Comprehensive inventory of all 8 campus facilities and their configured corridor connections.")

    cols = st.columns(2)
    for idx, (nid, name) in enumerate(LOCATIONS.items()):
        col = cols[idx % 2]
        node_info = NODE_TYPES.get(nid, {})
        b_type = node_info.get("type", "Campus Facility")
        connections = CAMPUS_GRAPH.get(nid, {})

        render_building_card(
            container=col,
            nid=nid,
            name=name,
            b_type=b_type,
            connections=connections,
            is_exit=(nid in EMERGENCY_EXITS),
            is_start=(nid == start_loc),
            is_hazard=(nid == em_loc),
            is_crowded=(nid in crowded),
            is_restricted=(nid in restricted),
        )

    # 9. Disclaimer
    render_disclaimer()
