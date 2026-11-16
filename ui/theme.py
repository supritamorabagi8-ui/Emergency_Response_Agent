"""
=============================================================================
EMERGENCY RESPONSE AGENT AI — FUTURISTIC DESIGN SYSTEM ENGINE
Futuristic Dark Purple, Neon Violet, Magenta & Emerald Theme Engine.
High-Contrast Text System: All primary text styled in bright #FFFFFF.
Bulletproof HTML Renderer: Eliminates CommonMark 4-space code block triggers.
=============================================================================
"""

import datetime
import streamlit as st
from environment.campus_graph import LOCATIONS


def render_html(html_code: str, container=None):
    """
    Safely render HTML without Markdown indented-code-block artifacts.
    Strips leading whitespace from every line individually, guaranteeing that CommonMark
    never treats 4+ leading spaces as an indented <pre><code> code block.
    """
    if not html_code:
        return
    lines = html_code.strip().splitlines()
    clean_lines = [line.lstrip() for line in lines if line.strip()]
    clean_html = "\n".join(clean_lines)
    target = container if container is not None else st
    target.markdown(clean_html, unsafe_allow_html=True)


def inject_custom_css():
    """Inject global CSS rules to create an elite futuristic command-center experience."""
    css = """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

        /* Color Tokens matching user specifications */
        :root {
            --bg-main: #080511;
            --bg-secondary: #100A20;
            --sidebar-bg: #100B1D;
            --card-main: #17102A;
            --card-secondary: #211438;
            --deep-purple: #30105A;
            --primary-violet: #8B5CF6;
            --neon-purple: #A855F7;
            --lavender-glow: #C4B5FD;
            --magenta-accent: #E879F9;
            --pink-highlight: #F0ABFC;
            --text-main: #FFFFFF;
            --text-secondary: #B9AECF;
            --border-subtle: #3A2854;
            --border-glow: rgba(168, 85, 247, 0.45);

            /* Emergency severity functional colors */
            --sev-critical: #EF4444;
            --sev-high: #F97316;
            --sev-medium: #F59E0B;
            --sev-safe: #22C55E;
            --sev-info: #3B82F6;
        }

        /* App Background with ambient violet/magenta mesh glow */
        .stApp {
            background-color: var(--bg-main) !important;
            background-image: 
                radial-gradient(circle at 15% 10%, rgba(48, 16, 90, 0.45) 0%, transparent 45%),
                radial-gradient(circle at 85% 15%, rgba(139, 92, 246, 0.25) 0%, transparent 50%),
                radial-gradient(circle at 50% 85%, rgba(232, 121, 249, 0.15) 0%, transparent 60%) !important;
            color: #FFFFFF !important;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }

        /* Scoped text contrast - preserve component-specific colors */
        .stApp {
            color: #FFFFFF;
        }

        .stApp h1,
        .stApp h2,
        .stApp h3,
        .stApp h4,
        .stApp h5,
        .stApp h6 {
            color: #FFFFFF !important;
        }

        .stApp p,
        .stApp li,
        .stApp label,
        .stApp strong,
        .stApp b {
            color: inherit;
        }

        .stApp h1,
        .stApp h2,
        .stApp h3,
        .stApp h4,
        .stApp h5,
        .stApp h6 {
            font-weight: 700 !important;
        }

        header[data-testid="stHeader"] {
            background: transparent !important;
        }

        /* Code Block Safeguard: Prevent white rectangular code blocks */
        code, pre, div[data-testid="stCodeBlock"], pre code {
            background-color: #17102A !important;
            color: #C4B5FD !important;
            border: 1px solid #3A2854 !important;
            border-radius: 8px !important;
            font-family: 'JetBrains Mono', monospace !important;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: var(--sidebar-bg) !important;
            border-right: 1px solid var(--border-subtle) !important;
            box-shadow: 6px 0 30px rgba(8, 5, 17, 0.7) !important;
        }

        [data-testid="stSidebar"] * {
            color: #FFFFFF !important;
        }

        /* Radio Navigation in Sidebar */
        [data-testid="stSidebar"] .stRadio > div {
            gap: 6px;
        }

        [data-testid="stSidebar"] .stRadio label {
            background: rgba(23, 16, 42, 0.7) !important;
            border: 1px solid rgba(58, 40, 84, 0.6) !important;
            border-radius: 10px !important;
            padding: 10px 14px !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            margin-bottom: 4px !important;
            display: flex !important;
            align-items: center !important;
        }

        [data-testid="stSidebar"] .stRadio label:hover {
            background: rgba(48, 16, 90, 0.6) !important;
            border-color: var(--neon-purple) !important;
            color: #FFFFFF !important;
            transform: translateX(3px);
            box-shadow: 0 0 16px rgba(168, 85, 247, 0.25);
        }

        [data-testid="stSidebar"] .stRadio label[data-checked="true"],
        [data-testid="stSidebar"] .stRadio div[aria-checked="true"] {
            background: linear-gradient(90deg, rgba(139, 92, 246, 0.35) 0%, rgba(232, 121, 249, 0.25) 100%) !important;
            border: 1px solid var(--neon-purple) !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            box-shadow: 0 0 20px rgba(168, 85, 247, 0.45) !important;
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 7px;
            height: 7px;
        }

        ::-webkit-scrollbar-track {
            background: #080511;
        }

        ::-webkit-scrollbar-thumb {
            background: #30105A;
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #8B5CF6;
        }

        /* Glassmorphism Cards */
        .glass-card {
            background: rgba(23, 16, 42, 0.9);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border: 1px solid var(--border-subtle);
            border-radius: 16px;
            padding: 22px;
            margin-bottom: 18px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45), 0 0 1px 1px rgba(139, 92, 246, 0.15);
            transition: all 0.3s ease;
        }

        .glass-card:hover {
            border-color: var(--neon-purple);
            box-shadow: 0 12px 36px rgba(0, 0, 0, 0.55), 0 0 20px rgba(168, 85, 247, 0.2);
        }

        .card-header {
            font-size: 17px;
            font-weight: 800;
            color: #FFFFFF;
            letter-spacing: -0.2px;
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 14px;
            border-bottom: 1px solid rgba(58, 40, 84, 0.7);
            padding-bottom: 10px;
        }

        /* Futuristic Hero Banner */
        .hero-command {
            position: relative;
            background: linear-gradient(135deg, rgba(23, 16, 42, 0.95) 0%, rgba(48, 16, 90, 0.85) 50%, rgba(33, 20, 56, 0.95) 100%);
            border: 1px solid var(--border-glow);
            border-radius: 20px;
            padding: 30px 36px;
            margin-bottom: 24px;
            box-shadow: 0 16px 45px rgba(0, 0, 0, 0.55), 0 0 35px rgba(139, 92, 246, 0.25);
            overflow: hidden;
            backdrop-filter: blur(16px);
        }

        .hero-command::before {
            content: "";
            position: absolute;
            top: -50%;
            right: -20%;
            width: 320px;
            height: 320px;
            background: radial-gradient(circle, rgba(232, 121, 249, 0.35) 0%, transparent 70%);
            filter: blur(40px);
            pointer-events: none;
        }

        .hero-command::after {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #8B5CF6, #E879F9, #F0ABFC, #8B5CF6);
            background-size: 200% auto;
            animation: borderGradient 4s linear infinite;
        }

        @keyframes borderGradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .hero-title {
            font-size: 30px;
            font-weight: 800;
            letter-spacing: -0.5px;
            color: #FFFFFF !important;
            margin: 0 0 8px 0;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .hero-subtitle {
            font-size: 14.5px;
            color: #B9AECF !important;
            margin: 0;
            line-height: 1.6;
            max-width: 900px;
            font-weight: 500;
        }

        /* Top Header Control Bar */
        .top-header-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: rgba(16, 11, 29, 0.95);
            border: 1px solid var(--border-subtle);
            border-radius: 14px;
            padding: 12px 24px;
            margin-bottom: 22px;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }

        .top-header-left {
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .top-header-right {
            display: flex;
            align-items: center;
            gap: 16px;
            font-size: 13px;
            color: #FFFFFF !important;
            font-weight: 600;
        }

        /* Statistical Metric Cards */
        .stat-card {
            background: linear-gradient(145deg, rgba(23, 16, 42, 0.95) 0%, rgba(33, 20, 56, 0.9) 100%);
            border: 1px solid var(--border-subtle);
            border-radius: 14px;
            padding: 20px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
            transition: all 0.25s ease;
        }

        .stat-card:hover {
            border-color: var(--neon-purple);
            transform: translateY(-2px);
            box-shadow: 0 8px 28px rgba(139, 92, 246, 0.2);
        }

        .stat-card::after {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(180deg, #8B5CF6, #E879F9);
        }

        .stat-label {
            font-size: 11.5px;
            font-weight: 700;
            color: #B9AECF !important;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 8px;
        }

        .stat-value {
            font-size: 28px;
            font-weight: 800;
            color: #FFFFFF !important;
            font-family: 'JetBrains Mono', monospace;
            letter-spacing: -0.5px;
            margin-bottom: 4px;
        }

        .stat-sub {
            font-size: 12px;
            color: #C4B5FD !important;
            font-weight: 500;
        }

        /* Streamlit Native Metric Overrides */
        [data-testid="stMetric"] {
            background-color: #17102A !important;
            border: 1px solid #3A2854 !important;
            border-radius: 12px !important;
            padding: 14px 18px !important;
        }

        [data-testid="stMetricLabel"] {
            color: #B9AECF !important;
            font-weight: 700 !important;
            font-size: 12px !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
        }

        [data-testid="stMetricValue"] {
            color: #FFFFFF !important;
            font-weight: 800 !important;
            font-family: 'JetBrains Mono', monospace !important;
        }

        /* Glowing Emergency Action Buttons */
        div.stButton > button {
            background: linear-gradient(135deg, #8B5CF6 0%, #A855F7 50%, #E879F9 100%) !important;
            color: #FFFFFF !important;
            border: 1px solid rgba(240, 171, 252, 0.4) !important;
            border-radius: 12px !important;
            font-weight: 700 !important;
            font-size: 13.5px !important;
            letter-spacing: 0.4px !important;
            padding: 10px 22px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 20px rgba(168, 85, 247, 0.4), 0 0 12px rgba(232, 121, 249, 0.3) !important;
        }

        div.stButton > button:hover {
            background: linear-gradient(135deg, #7C3AED 0%, #9333EA 50%, #D946EF 100%) !important;
            border-color: #F0ABFC !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 30px rgba(168, 85, 247, 0.6), 0 0 20px rgba(240, 171, 252, 0.5) !important;
        }

        /* Form Controls & Inputs */
        div[data-baseweb="select"] > div {
            background-color: #17102A !important;
            border: 1px solid #3A2854 !important;
            border-radius: 10px !important;
        }

        div[data-baseweb="select"] > div:hover {
            border-color: #A855F7 !important;
            box-shadow: 0 0 12px rgba(168, 85, 247, 0.25) !important;
        }

        div[data-baseweb="select"] > div,
        div[data-baseweb="select"] > div span,
        div[data-baseweb="select"] > div div,
        div[data-baseweb="select"] > div p,
        div[data-baseweb="select"] > div svg {
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
        }

        div[data-baseweb="select"] input {
            background-color: transparent !important;
            color: #FFFFFF !important;
        }

        /* Multiselect selected tags inside closed input */
        div[data-baseweb="tag"] {
            background-color: #30105A !important;
            border: 1px solid #8B5CF6 !important;
            border-radius: 6px !important;
        }

        div[data-baseweb="tag"] * {
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
        }

        /* Dropdown Popover Menus: Dark Purple with Crisp White Text */
        div[data-baseweb="popover"],
        div[data-baseweb="popover"] > div,
        ul[role="listbox"],
        div[data-baseweb="menu"],
        [data-testid="stSelectboxVirtualDropdown"] {
            background-color: #17102A !important;
            border: 1px solid #3A2854 !important;
            border-radius: 12px !important;
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.6) !important;
            overflow: hidden !important;
        }

        div[data-baseweb="popover"] *,
        div[data-baseweb="menu"] *,
        ul[role="listbox"] *,
        li[role="option"],
        li[role="option"] *,
        li[role="option"] div,
        li[role="option"] span,
        li[role="option"] p,
        [data-testid="stSelectboxVirtualDropdown"] *,
        div[role="listbox"] * {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }

        li[role="option"] {
            background-color: #17102A !important;
            color: #FFFFFF !important;
            font-size: 13.5px !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            margin-bottom: 3px !important;
            padding: 10px 14px !important;
            transition: all 0.15s ease !important;
        }

        li[role="option"]:hover,
        li[role="option"][aria-selected="true"],
        li[role="option"][data-highlighted="true"] {
            background-color: #30105A !important;
            border-left: 3px solid #8B5CF6 !important;
        }

        input {
            background-color: #17102A !important;
            color: #FFFFFF !important;
            border-color: #3A2854 !important;
        }

        /* Forms Styling */
        div[data-testid="stForm"] {
            background-color: rgba(23, 16, 42, 0.6) !important;
            border: 1px solid #3A2854 !important;
            border-radius: 16px !important;
            padding: 22px !important;
        }

        /* Animated Emergency Alert Banner */
        @keyframes pulse-emergency-purple {
            0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.6), 0 0 15px rgba(168, 85, 247, 0.3); }
            70% { box-shadow: 0 0 0 16px rgba(239, 68, 68, 0), 0 0 25px rgba(232, 121, 249, 0); }
            100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0), 0 0 15px rgba(168, 85, 247, 0.3); }
        }

        .alert-banner-active {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.3) 0%, rgba(48, 16, 90, 0.85) 100%);
            border: 2px solid #EF4444;
            border-radius: 16px;
            padding: 20px 26px;
            margin-bottom: 22px;
            animation: pulse-emergency-purple 2.2s infinite;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 16px;
        }

        .alert-banner-title {
            font-size: 19px;
            font-weight: 800;
            color: #FFFFFF !important;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        /* Success Banner */
        .success-banner-custom {
            background: linear-gradient(135deg, rgba(34, 197, 94, 0.25) 0%, rgba(48, 16, 90, 0.75) 100%);
            border: 1px solid #22C55E;
            border-radius: 16px;
            padding: 20px 26px;
            margin-bottom: 22px;
            display: flex;
            align-items: center;
            gap: 18px;
            box-shadow: 0 0 25px rgba(34, 197, 94, 0.25);
        }

        /* Status Pills */
        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.6px;
        }

        .pill-critical {
            background: rgba(239, 68, 68, 0.25);
            color: #FFFFFF !important;
            border: 1px solid #EF4444;
            box-shadow: 0 0 10px rgba(239, 68, 68, 0.3);
        }

        .pill-high {
            background: rgba(249, 115, 22, 0.25);
            color: #FFFFFF !important;
            border: 1px solid #F97316;
        }

        .pill-medium {
            background: rgba(245, 158, 11, 0.25);
            color: #FFFFFF !important;
            border: 1px solid #F59E0B;
        }

        .pill-safe {
            background: rgba(34, 197, 94, 0.25);
            color: #FFFFFF !important;
            border: 1px solid #22C55E;
            box-shadow: 0 0 10px rgba(34, 197, 94, 0.25);
        }

        .pill-violet {
            background: rgba(139, 92, 246, 0.3);
            color: #FFFFFF !important;
            border: 1px solid #A855F7;
            box-shadow: 0 0 12px rgba(168, 85, 247, 0.3);
        }

        /* Dataframe styling */
        [data-testid="stDataFrame"], [data-testid="stTable"] {
            background: #17102A !important;
            border: 1px solid #3A2854 !important;
            border-radius: 12px !important;
            overflow: hidden !important;
        }

        [data-testid="stDataFrame"] * {
            color: #FFFFFF !important;
        }

        /* Disclaimer Card */
        .disclaimer-futuristic {
            background: rgba(16, 10, 32, 0.95);
            border: 1px solid #3A2854;
            border-radius: 12px;
            padding: 14px 20px;
            font-size: 12px;
            color: #B9AECF !important;
            margin-top: 26px;
            line-height: 1.6;
        }
        </style>
    """
    render_html(css)


def render_top_header():
    """Render the executive top navigation bar with high-contrast text."""
    now_str = datetime.datetime.now().strftime("%A, %d %B %Y • %H:%M:%S")

    html = f"""
    <div class="top-header-bar">
        <div class="top-header-left">
            <span style="font-size:24px;">🚨</span>
            <div>
                <div style="font-size:15px; font-weight:800; color:#FFFFFF; letter-spacing:0.4px;">
                    EMERGENCY RESPONSE AGENT AI
                </div>
                <div style="font-size:11px; font-weight:700; color:#E879F9; letter-spacing:0.8px;">
                    ENTERPRISE COMMAND & CONTROL MATRIX
                </div>
            </div>
        </div>
        <div class="top-header-right">
            <span class="status-pill pill-safe">🟢 SYSTEM NOMINAL</span>
            <span style="color:#FFFFFF; font-weight:600;">🕒 {now_str}</span>
            <span class="status-pill pill-violet">👤 ADMIN OP-01</span>
        </div>
    </div>
    """
    render_html(html)


def render_page_header(title: str, subtitle: str, badge_text: str = "COMMAND ACTIVE"):
    """Render a futuristic hero banner with ambient lighting and bright white text."""
    html = f"""
    <div class="hero-command">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;">
            <h1 class="hero-title">{title}</h1>
            <span class="status-pill pill-violet">✦ {badge_text}</span>
        </div>
        <p class="hero-subtitle">{subtitle}</p>
    </div>
    """
    render_html(html)


def render_stat_card(col, label: str, value: str, subtext: str = "", badge: str = None):
    """Render a statistical metric card with crisp white text."""
    badge_html = f'<span class="status-pill pill-violet" style="float:right; font-size:10px;">{badge}</span>' if badge else ""
    html = f"""
    <div class="stat-card">
        {badge_html}
        <div class="stat-label">{label}</div>
        <div class="stat-value">{value}</div>
        <div class="stat-sub">{subtext}</div>
    </div>
    """
    render_html(html, container=col)


def render_route_card(
    container,
    card_type: str,
    route_data: dict,
    title: str = None,
    subtitle: str = None,
):
    """
    Render a beautifully styled, robust Emergency Route Card with dark purple background,
    subtle violet border, white readable text, colored status accents, and accurate backend metrics.
    Guaranteed zero raw HTML code leakage.
    """
    is_rec = card_type.lower() == "recommended"
    accent = "#22C55E" if is_rec else "#A855F7"
    pill_cls = "pill-safe" if is_rec else "pill-violet"
    default_title = "🟢 RECOMMENDED EVACUATION ROUTE" if is_rec else "🟣 ALTERNATIVE EVACUATION ROUTE"
    default_sub = "Cost-Optimal Safe Path (Dijkstra / Zero-Heuristic A*)" if is_rec else "Fewest Corridor Hops (Breadth-First Search)"
    badge_label = "COST-OPTIMAL" if is_rec else "MINIMUM HOPS"

    card_title = title or default_title
    card_sub = subtitle or default_sub

    if route_data and route_data.get("route"):
        route = route_data["route"]
        route_cost = route_data.get("route_cost", 0)
        time_ms = route_data.get("execution_time_ms", 0.0)
        nodes_exp = route_data.get("nodes_expanded", 0)
        score = route_data.get("score")
        target_exit = route[-1]
        exit_name = LOCATIONS.get(target_exit, "Emergency Exit")

        # Build clean breadcrumb path
        hops = []
        for i, n in enumerate(route):
            loc_name = LOCATIONS.get(n, n)
            if i == len(route) - 1:
                hops.append(f'<span style="background:rgba(34,197,94,0.25); color:#A7F3D0; border:1px solid #22C55E; padding:5px 10px; border-radius:6px; font-weight:bold; font-size:13px;">🚪 Gate {n} ({loc_name})</span>')
            elif i == 0:
                hops.append(f'<span style="background:rgba(139,92,246,0.25); color:#F0ABFC; border:1px solid #8B5CF6; padding:5px 10px; border-radius:6px; font-weight:bold; font-size:13px;">📍 {n} ({loc_name})</span>')
            else:
                hops.append(f'<span style="background:#211438; color:#FFFFFF; border:1px solid #3A2854; padding:5px 10px; border-radius:6px; font-weight:600; font-size:13px;">{n} ({loc_name})</span>')
        breadcrumb_html = ' <span style="color:#C4B5FD; font-size:14px; font-weight:bold;">➔</span> '.join(hops)

        score_html = f'<div>• <strong style="color:#FFFFFF;">Safety Score:</strong> <span style="color:#A7F3D0; font-weight:bold;">{score} / 100</span></div>' if score is not None else ""
        note = "*Evaluates physical corridor distances and crowd penalties (+5 cost) to guarantee lowest total effort." if is_rec else "*Evaluates topological connection count only; guarantees minimal building hops ignoring distances."

        html = f"""
        <div class="glass-card" style="border-left: 4px solid {accent}; margin-bottom: 16px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; border-bottom:1px solid #3A2854; padding-bottom:10px;">
                <div>
                    <h3 style="margin:0; color:#FFFFFF; font-size:17px; font-weight:800; display:flex; align-items:center; gap:8px;">
                        {card_title}
                    </h3>
                    <div style="font-size:12px; color:#C4B5FD; margin-top:2px;">{card_sub}</div>
                </div>
                <span class="status-pill {pill_cls}">{badge_label}</span>
            </div>

            <div style="background:#100A20; border:1px solid #3A2854; border-radius:10px; padding:12px 14px; margin-bottom:14px;">
                <div style="font-size:11px; font-weight:700; color:#B9AECF; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:8px;">Verified Evacuation Trajectory</div>
                <div style="display:flex; align-items:center; flex-wrap:wrap; gap:6px;">
                    {breadcrumb_html}
                </div>
            </div>

            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px; font-size:13px; color:#FFFFFF; background:#17102A; border-radius:8px; padding:4px 0;">
                <div>• <strong style="color:#FFFFFF;">Total Route Cost:</strong> <span style="color:#FFFFFF; font-weight:700;">{route_cost} units</span></div>
                <div>• <strong style="color:#FFFFFF;">Execution Time:</strong> <span style="color:#FFFFFF;">{time_ms:.4f} ms</span></div>
                <div>• <strong style="color:#FFFFFF;">Nodes Expanded:</strong> <span style="color:#FFFFFF;">{nodes_exp} nodes</span></div>
                <div>• <strong style="color:#FFFFFF;">Target Exit:</strong> <span style="color:#22C55E; font-weight:bold;">Gate {target_exit}</span></div>
                {score_html}
            </div>

            <div style="font-size:11.5px; color:#B9AECF; margin-top:10px; border-top:1px solid #3A2854; padding-top:8px; font-style:italic;">
                {note}
            </div>
        </div>
        """
    else:
        html = f"""
        <div class="glass-card" style="border-left: 4px solid #EF4444; margin-bottom: 16px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; border-bottom:1px solid #3A2854; padding-bottom:10px;">
                <div>
                    <h3 style="margin:0; color:#FFFFFF; font-size:17px; font-weight:800;">{card_title}</h3>
                    <div style="font-size:12px; color:#C4B5FD; margin-top:2px;">{card_sub}</div>
                </div>
                <span class="status-pill pill-critical">NO ROUTE</span>
            </div>
            <div style="background:#100A20; border:1px solid rgba(239,68,68,0.4); border-radius:10px; padding:14px; color:#FFFFFF;">
                <div style="color:#EF4444; font-weight:800; font-size:14px; margin-bottom:6px;">⚠️ No Viable Evacuation Route Found</div>
                <div style="font-size:12.5px; line-height:1.6; color:#FFFFFF;">
                    All candidate pathways to designated emergency exits are impassable or compromised under the active environmental constraints.
                    Please consult tactical sheltering directives and await security coordination.
                </div>
            </div>
        </div>
        """
    render_html(html, container=container)


def render_building_card(
    container,
    nid: str,
    name: str,
    b_type: str,
    connections: dict,
    is_exit: bool = False,
    is_start: bool = False,
    is_hazard: bool = False,
    is_crowded: bool = False,
    is_restricted: bool = False,
):
    """
    Render a campus building card in the dark purple futuristic design system.
    Guarantees dark background #17102A, border #3A2854, white text #FFFFFF,
    and lavender/green connection badges.
    """
    accent_border = "#3A2854"
    status_badges = []

    if is_exit:
        accent_border = "#22C55E"
        status_badges.append('<span class="status-pill pill-safe">🚪 EMERGENCY EXIT</span>')
    if is_start:
        accent_border = "#8B5CF6"
        status_badges.append('<span class="status-pill pill-violet">📍 STARTING POINT</span>')
    if is_hazard:
        accent_border = "#EF4444"
        status_badges.append('<span class="status-pill pill-critical">🚨 HAZARD EPICENTER</span>')
    if is_restricted:
        accent_border = "#F59E0B"
        status_badges.append('<span class="status-pill pill-high">⛔ RESTRICTED</span>')
    if is_crowded:
        status_badges.append('<span class="status-pill pill-medium">⚠️ CROWDED (+5)</span>')

    if not status_badges:
        status_badges.append('<span class="status-pill pill-safe">🟢 PASSABLE</span>')

    badge_row = " ".join(status_badges)

    # Connections tags
    if connections:
        conn_pills = []
        for nbr, dist in connections.items():
            nbr_name = LOCATIONS.get(nbr, nbr)
            conn_pills.append(
                f'<span style="display:inline-block; background:#211438; color:#C4B5FD; border:1px solid #3A2854; padding:3px 8px; margin:2px 4px 2px 0; border-radius:6px; font-size:11.5px; font-weight:600;">'
                f'{nbr} ({nbr_name}): {dist}m'
                f'</span>'
            )
        connections_html = "".join(conn_pills)
    else:
        connections_html = '<span style="color:#B9AECF; font-size:12px;">No direct corridor connections</span>'

    html = f"""
    <div style="background:#17102A; border:1px solid {accent_border}; border-radius:14px; padding:18px; margin-bottom:14px; box-shadow:0 4px 18px rgba(0,0,0,0.4); color:#FFFFFF;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:8px;">
            <div style="font-size:16px; font-weight:800; color:#FFFFFF;">
                Zone {nid} — {name}
            </div>
            <div>
                {badge_row}
            </div>
        </div>
        <div style="font-size:12.5px; font-weight:600; color:#E879F9; margin-bottom:10px;">
            {b_type}
        </div>
        <div style="font-size:12px; color:#B9AECF; margin-bottom:6px; font-weight:700; text-transform:uppercase; letter-spacing:0.5px;">
            Direct Corridor Connections:
        </div>
        <div style="line-height:1.7;">
            {connections_html}
        </div>
    </div>
    """
    render_html(html, container=container)


def render_legend_card(container=None):
    """Render the standard map legend card in futuristic dark purple aesthetics."""
    html = """
    <div style="background:#17102A; border:1px solid #3A2854; border-radius:14px; padding:18px; color:#FFFFFF; margin-bottom:18px; box-shadow:0 4px 18px rgba(0,0,0,0.35);">
        <div style="font-size:14px; font-weight:800; color:#FFFFFF; margin-bottom:12px; border-bottom:1px solid #3A2854; padding-bottom:8px;">
            🗺️ CAMPUS TOPOLOGY MAP LEGEND & STATUS SPECIFICATIONS
        </div>
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(210px, 1fr)); gap:12px; font-size:12.5px; color:#FFFFFF;">
            <div>
                <span style="color:#22C55E; font-weight:bold;">🟢 Recommended Safe Route</span>
                <div style="color:#B9AECF; font-size:11.5px;">Cost-optimal path (Dijkstra / Zero-Heuristic A*)</div>
            </div>
            <div>
                <span style="color:#A855F7; font-weight:bold;">🟣 Alternative Candidate Route</span>
                <div style="color:#B9AECF; font-size:11.5px;">Fewest building transitions (BFS Hops)</div>
            </div>
            <div>
                <span style="color:#8B5CF6; font-weight:bold;">📍 Evacuation Starting Point</span>
                <div style="color:#B9AECF; font-size:11.5px;">Designated assembly origin zone</div>
            </div>
            <div>
                <span style="color:#22C55E; font-weight:bold;">🎯 Target Recommended Exit</span>
                <div style="color:#B9AECF; font-size:11.5px;">Assigned safe gate for exit</div>
            </div>
            <div>
                <span style="color:#EF4444; font-weight:bold;">🚨 Hazard Epicenter</span>
                <div style="color:#B9AECF; font-size:11.5px;">Active fire / security breach zone</div>
            </div>
            <div>
                <span style="color:#F97316; font-weight:bold;">⚠️ Crowded Corridor</span>
                <div style="color:#B9AECF; font-size:11.5px;">Pedestrian congestion (+5 travel cost)</div>
            </div>
            <div>
                <span style="color:#EF4444; font-weight:bold;">⛔ Security Restricted Zone</span>
                <div style="color:#B9AECF; font-size:11.5px;">Quarantine perimeter (Strict No-Entry)</div>
            </div>
            <div>
                <span style="color:#EF4444; font-weight:bold;">🚧 Blocked Corridor (❌)</span>
                <div style="color:#B9AECF; font-size:11.5px;">Impassable / structural collapse</div>
            </div>
        </div>
        <div style="border-top:1px solid #3A2854; margin-top:14px; padding-top:10px; font-size:11.5px; color:#B9AECF; line-height:1.5;">
            ℹ️ <strong>Simulated 2D Topological Campus Layout:</strong> Node coordinates represent schematic topological relationships
            and physical corridor distance weights defined in the campus graph model (CAMPUS_GRAPH). Not arbitrary GPS coordinates.
        </div>
    </div>
    """
    render_html(html, container=container)


def render_disclaimer():
    """Render the standard simulation disclaimer card in bright white text."""
    html = """
    <div class="disclaimer-futuristic">
        <strong style="color:#FFFFFF;">⚠️ CAMPUS EMERGENCY SIMULATION SYSTEM NOTICE:</strong>
        All emergency routes, siren sounds, risk heatmaps, and decision-support directives are 
        simulations computed using the configured campus graph model. This software operates as an internal 
        decision-support demonstration and does not trigger physical municipal or campus-wide emergency sirens.
    </div>
    """
    render_html(html)