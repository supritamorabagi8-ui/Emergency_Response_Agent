"""
Performance Analytics View for Emergency Operations Command Center.
Visualizes algorithm benchmarks with custom purple/violet/magenta Plotly charts using real CSV data.
"""

import os
import pandas as pd
import plotly.express as px
import streamlit as st

from ui.theme import render_disclaimer, render_page_header


def render_performance_view():
    """Render the Algorithmic Performance Analytics Page."""
    render_page_header(
        "📊 Algorithmic Search & Performance Analytics",
        "Empirical Search Complexity, Latency Distribution, and Accuracy Metrics Across Benchmark Scenarios",
        badge_text="METRICS ENGINE",
    )

    csv_path = "performance/experiment_results.csv"
    if not os.path.exists(csv_path):
        st.warning("Benchmark CSV file not found at 'performance/experiment_results.csv'.")
        render_disclaimer()
        return

    df = pd.read_csv(csv_path)

    # High-Level Summary Metrics
    col1, col2, col3, col4 = st.columns(4)
    total_runs = len(df)
    success_rate = int(df["goal_reached"].sum() / total_runs * 100)
    avg_dijkstra_cost = df[df["algorithm"] == "A*"]["route_cost"].mean()
    avg_bfs_cost = df[df["algorithm"] == "BFS"]["route_cost"].mean()

    col1.metric("Total Benchmark Runs", total_runs)
    col2.metric("Goal Reached Rate", f"{success_rate}%")
    col3.metric("Avg Dijkstra Cost", f"{avg_dijkstra_cost:.1f}")
    col4.metric("Avg BFS Cost", f"{avg_bfs_cost:.1f}")

    st.markdown("<hr style='border-color:#3A2854; margin:22px 0;'>", unsafe_allow_html=True)
    st.markdown("### 📈 Comparative Algorithmic Visualizations (Purple Palette)")

    c1, c2 = st.columns(2)

    with c1:
        # Route Cost by Scenario and Algorithm
        fig_cost = px.bar(
            df,
            x="experiment",
            y="route_cost",
            color="algorithm",
            barmode="group",
            color_discrete_map={"BFS": "#8B5CF6", "A*": "#E879F9"},
            title="Route Cost by Scenario: Dijkstra (Magenta) vs BFS (Violet)",
        )
        fig_cost.update_layout(
            paper_bgcolor="#100A20",
            plot_bgcolor="#100A20",
            font_color="#FFFFFF",
            legend=dict(font=dict(color="#FFFFFF")),
            xaxis=dict(tickangle=-25, tickfont=dict(color="#FFFFFF")),
            yaxis=dict(tickfont=dict(color="#FFFFFF")),
            margin=dict(l=20, r=20, t=40, b=50),
        )
        st.plotly_chart(fig_cost, width="stretch")

    with c2:
        # Execution Latency Comparison
        fig_time = px.bar(
            df,
            x="experiment",
            y="execution_time_ms",
            color="algorithm",
            barmode="group",
            color_discrete_map={"BFS": "#A855F7", "A*": "#F0ABFC"},
            title="Execution Latency (ms) Across Scenarios",
        )
        fig_time.update_layout(
            paper_bgcolor="#100A20",
            plot_bgcolor="#100A20",
            font_color="#FFFFFF",
            legend=dict(font=dict(color="#FFFFFF")),
            xaxis=dict(tickangle=-25, tickfont=dict(color="#FFFFFF")),
            yaxis=dict(tickfont=dict(color="#FFFFFF")),
            margin=dict(l=20, r=20, t=40, b=50),
        )
        st.plotly_chart(fig_time, width="stretch")

    # Nodes Expanded Search Space
    st.markdown("### 🔍 Search Space Complexity (Nodes Expanded)")
    fig_nodes = px.line(
        df,
        x="experiment",
        y="nodes_expanded",
        color="algorithm",
        markers=True,
        color_discrete_map={"BFS": "#8B5CF6", "A*": "#22C55E"},
        title="Nodes Expanded: Search Frontier Comparison",
    )
    fig_nodes.update_layout(
        paper_bgcolor="#100A20",
        plot_bgcolor="#100A20",
        font_color="#FFFFFF",
        legend=dict(font=dict(color="#FFFFFF")),
        xaxis=dict(tickfont=dict(color="#FFFFFF")),
        yaxis=dict(tickfont=dict(color="#FFFFFF")),
        margin=dict(l=20, r=20, t=40, b=20),
    )
    st.plotly_chart(fig_nodes, width="stretch")

    # Benchmark Data Table
    st.markdown("### 📋 All 12 Benchmark Experiment Records")
    st.dataframe(df, width="stretch")

    render_disclaimer()
