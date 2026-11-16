"""
=============================================================================
EMERGENCY RESPONSE AGENT AI — CAMPUS NETWORK GRAPH VISUALIZER
Futuristic Interactive Campus Network Map & Risk Visualizer.
Styled in dark charcoal-purple (#080511), neon violet (#A855F7), magenta (#E879F9),
and luminous emerald (#22C55E) for recommended evacuation paths.
=============================================================================
"""

import plotly.graph_objects as go
from environment.campus_graph import CAMPUS_GRAPH, EMERGENCY_EXITS, LOCATIONS

# Schematic 2D topological positions for the 8 campus buildings
NODE_COORDS = {
    "A": (1.5, 3.8),
    "B": (4.0, 4.0),
    "L": (2.5, 2.5),
    "C": (5.0, 2.4),
    "M": (3.2, 1.3),
    "P": (5.2, 1.1),
    "G1": (4.0, 0.0),
    "G2": (6.2, 0.0),
}

# Building semantic type mappings for distinct icons/symbols
NODE_TYPES = {
    "A": {"type": "Academic Block", "symbol": "circle"},
    "B": {"type": "Academic Block", "symbol": "circle"},
    "L": {"type": "Knowledge Center / Library", "symbol": "diamond"},
    "C": {"type": "Campus Canteen", "symbol": "hexagon"},
    "M": {"type": "Medical Health Centre", "symbol": "cross"},
    "P": {"type": "Transit & Parking Hub", "symbol": "square"},
    "G1": {"type": "Primary Gate (Exit 1)", "symbol": "star"},
    "G2": {"type": "Secondary Gate (Exit 2)", "symbol": "star"},
}


def create_campus_figure(
    start: str = None,
    emergency_location: str = None,
    blocked_edges: list = None,
    crowded_locations: list = None,
    restricted_locations: list = None,
    available_exits: list = None,
    bfs_route: list = None,
    astar_route: list = None,
    show_heatmap: bool = False,
    title: str = "Campus Evacuation Network — Topological Control View",
) -> go.Figure:
    """Build an interactive Plotly graph in futuristic purple aesthetics."""
    blocked_edges = blocked_edges or []
    crowded_locations = crowded_locations or []
    restricted_locations = restricted_locations or []
    available_exits = available_exits if available_exits is not None else EMERGENCY_EXITS

    # Identify the target exit recommended by Dijkstra / A*
    recommended_exit = astar_route[-1] if (astar_route and len(astar_route) > 0) else None

    blocked_set = {frozenset(edge) for edge in blocked_edges}
    fig = go.Figure()

    # 1. Base Campus Pathways (Edges)
    drawn_edges = set()
    for u, neighbors in CAMPUS_GRAPH.items():
        for v, cost in neighbors.items():
            edge_key = frozenset((u, v))
            if edge_key in drawn_edges:
                continue
            drawn_edges.add(edge_key)

            x0, y0 = NODE_COORDS[u]
            x1, y1 = NODE_COORDS[v]
            is_blocked = edge_key in blocked_set

            if is_blocked:
                fig.add_trace(
                    go.Scatter(
                        x=[x0, x1, None],
                        y=[y0, y1, None],
                        mode="lines",
                        line=dict(color="#EF4444", width=3.5, dash="dash"),
                        hoverinfo="text",
                        text=f"🚧 BLOCKED PATHWAY: {u} ↔ {v} (Impassable)",
                        name="Blocked Corridor",
                        showlegend=False,
                    )
                )
            else:
                fig.add_trace(
                    go.Scatter(
                        x=[x0, x1, None],
                        y=[y0, y1, None],
                        mode="lines",
                        line=dict(color="#3A2854", width=2.5),
                        hoverinfo="text",
                        text=f"Passable Corridor: {u} ↔ {v} (Distance Cost: {cost}m)",
                        name="Passable Pathway",
                        showlegend=False,
                    )
                )

            # Midpoint Cost Annotation
            mx, my = (x0 + x1) / 2.0, (y0 + x1) / 2.0 if False else ((x0 + x1) / 2.0, (y0 + y1) / 2.0)
            fig.add_annotation(
                x=mx,
                y=my,
                text=f"<b>{cost}</b>" if not is_blocked else "❌",
                showarrow=False,
                font=dict(size=10, color="#EF4444" if is_blocked else "#C4B5FD", family="JetBrains Mono"),
                bgcolor="#100A20",
                bordercolor="#EF4444" if is_blocked else "#3A2854",
                borderwidth=1,
                borderpad=2,
            )

    # 2. Alternative Route Overlay (BFS / Fewest Hops)
    if bfs_route and len(bfs_route) > 1 and bfs_route != astar_route:
        rx, ry = [NODE_COORDS[n][0] for n in bfs_route], [NODE_COORDS[n][1] for n in bfs_route]
        fig.add_trace(
            go.Scatter(
                x=rx,
                y=ry,
                mode="lines+markers",
                line=dict(color="#A855F7", width=4, dash="dot"),
                marker=dict(size=9, color="#C4B5FD"),
                name="Alternative Route (BFS Fewest Hops)",
                hoverinfo="text",
                text="Alternative (BFS): " + " → ".join(bfs_route),
            )
        )

    # 3. Recommended Evacuation Route (Glowing Emerald Green)
    if astar_route and len(astar_route) > 1:
        rx, ry = [NODE_COORDS[n][0] for n in astar_route], [NODE_COORDS[n][1] for n in astar_route]
        # Luminous outer glow halo
        fig.add_trace(
            go.Scatter(
                x=rx,
                y=ry,
                mode="lines",
                line=dict(color="rgba(34, 197, 94, 0.35)", width=14),
                hoverinfo="none",
                showlegend=False,
            )
        )
        # Core sharp neon route line
        fig.add_trace(
            go.Scatter(
                x=rx,
                y=ry,
                mode="lines+markers",
                line=dict(color="#22C55E", width=6),
                marker=dict(size=12, color="#22C55E", symbol="circle", line=dict(color="#FFFFFF", width=2)),
                name="RECOMMENDED SAFE ROUTE (Cost-Optimal)",
                hoverinfo="text",
                text="Recommended Safe Route: " + " → ".join(astar_route),
            )
        )

    # 4. Risk Dispersion Heatmap Zones if enabled
    if show_heatmap:
        hx, hy, h_colors, h_sizes = [], [], [], []
        for nid, (x, y) in NODE_COORDS.items():
            hx.append(x)
            hy.append(y)
            if nid == emergency_location or nid in restricted_locations:
                h_colors.append("rgba(239, 68, 68, 0.38)")
                h_sizes.append(70)
            elif nid in crowded_locations:
                h_colors.append("rgba(249, 115, 22, 0.32)")
                h_sizes.append(55)
            elif (astar_route and nid in astar_route) or nid in available_exits:
                h_colors.append("rgba(34, 197, 94, 0.25)")
                h_sizes.append(48)
            else:
                h_colors.append("rgba(139, 92, 246, 0.16)")
                h_sizes.append(38)

        fig.add_trace(
            go.Scatter(
                x=hx,
                y=hy,
                mode="markers",
                marker=dict(size=h_sizes, color=h_colors),
                hoverinfo="none",
                name="Risk Dispersion Zone",
                showlegend=True,
            )
        )

    # 5. Campus Location Markers (Nodes)
    nx, ny, n_colors, n_symbols, n_labels, n_hovers, n_sizes, n_line_colors, n_line_widths = [], [], [], [], [], [], [], [], []

    for nid, (x, y) in NODE_COORDS.items():
        nx.append(x)
        ny.append(y)
        full_name = LOCATIONS[nid]
        building_info = NODE_TYPES[nid]["type"]
        symbol = NODE_TYPES[nid]["symbol"]

        color = "#17102A"
        line_color = "#8B5CF6"
        line_width = 2.5
        size = 38
        status_label = "Passable / Secure"

        if nid == emergency_location:
            color = "#EF4444"
            line_color = "#FCA5A5"
            line_width = 3.5
            size = 44
            status_label = "🚨 CRITICAL HAZARD EPICENTER"
            symbol = "diamond"
        elif nid in restricted_locations:
            color = "#DC2626"
            line_color = "#FCA5A5"
            line_width = 3.0
            size = 38
            status_label = "⛔ SECURITY RESTRICTED (No Entry)"
            symbol = "x"
        elif nid in crowded_locations:
            color = "#EA580C"
            line_color = "#FED7AA"
            line_width = 3.0
            size = 40
            status_label = "⚠️ HEAVY CROWD CONGESTION (+5 Cost Penalty)"
            symbol = "hexagon"
        elif nid == recommended_exit:
            color = "#22C55E"
            line_color = "#4ADE80"
            line_width = 3.5
            size = 46
            status_label = "🎯 TARGET EMERGENCY EXIT (RECOMMENDED)"
            symbol = "star"
        elif nid in available_exits:
            color = "#10B981"
            line_color = "#BBF7D0"
            line_width = 2.5
            size = 40
            status_label = "🚪 OPERATIONAL EVACUATION EXIT"
            symbol = "star"

        if nid == start:
            color = "#8B5CF6"
            line_color = "#F0ABFC"
            line_width = 3.5
            size = 44
            status_label = "📍 STARTING EVACUATION POINT"

        n_colors.append(color)
        n_symbols.append(symbol)
        n_sizes.append(size)
        n_line_colors.append(line_color)
        n_line_widths.append(line_width)
        n_labels.append(f"<b>{nid}</b>")
        n_hovers.append(
            f"<b>Zone {nid}: {full_name}</b><br>"
            f"Classification: {building_info}<br>"
            f"Status: {status_label}<br>"
            f"Adjacencies: {', '.join(CAMPUS_GRAPH[nid].keys())}"
        )

    fig.add_trace(
        go.Scatter(
            x=nx,
            y=ny,
            mode="markers+text",
            marker=dict(
                size=n_sizes,
                color=n_colors,
                symbol=n_symbols,
                line=dict(color=n_line_colors, width=n_line_widths),
            ),
            text=n_labels,
            textposition="middle center",
            textfont=dict(color="#FFFFFF", size=13, family="JetBrains Mono"),
            hoverinfo="text",
            hovertext=n_hovers,
            name="Campus Nodes",
        )
    )

    # Layout: Dark Charcoal-Purple Theme
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(color="#FFFFFF", size=16, family="Plus Jakarta Sans"),
            x=0.02,
            y=0.96,
        ),
        paper_bgcolor="#080511",
        plot_bgcolor="#100A20",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#FFFFFF", size=11),
            bgcolor="rgba(23, 16, 42, 0.85)",
            bordercolor="#3A2854",
            borderwidth=1,
        ),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(l=15, r=15, t=55, b=15),
        height=540,
    )

    return fig
