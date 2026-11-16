"""
Standalone Pure-Python PDF Incident Report Generator.
Generates publication-quality standard PDF 1.4 documents without requiring third-party libraries.
Includes full incident metadata, routing metrics, decision rules, and simulation disclaimers.
"""

import datetime


def sanitize_text(text: str) -> str:
    """Sanitize strings for PDF Type 1 standard ASCII font output."""
    if text is None:
        return "N/A"
    clean = str(text).replace("(", "[").replace(")", "]").replace("\\", "/")
    return clean.encode("ascii", "replace").decode("ascii")


def generate_pdf_report(incident_data: dict) -> bytes:
    """Generate a standard PDF 1.4 document from an incident dictionary."""
    lines = []
    lines.append(("HEADER", "CAMPUS EMERGENCY MANAGEMENT CONTROL CENTER"))
    lines.append(("SUBHEADER", "OFFICIAL INCIDENT SIMULATION & ROUTE PLANNING REPORT"))
    lines.append(("LINE", "-" * 85))

    inc_id = sanitize_text(incident_data.get("id", "INC-001"))
    alert_id = sanitize_text(incident_data.get("alert_id", "ALERT-001"))
    ts = sanitize_text(incident_data.get("timestamp", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    etype = sanitize_text(incident_data.get("type", "General"))
    sev = sanitize_text(incident_data.get("severity", "High"))
    start_loc = sanitize_text(incident_data.get("start", "N/A"))
    em_loc = sanitize_text(incident_data.get("emergency_location", "N/A"))
    status = sanitize_text(incident_data.get("status", "Analyzed"))

    lines.append(("SECTION", "1. INCIDENT OVERVIEW & CLASSIFICATION"))
    lines.append(("TEXT", f"Incident Identifier: {inc_id}   |   Alert ID: {alert_id}"))
    lines.append(("TEXT", f"Timestamp: {ts}   |   Classification: {etype}"))
    lines.append(("TEXT", f"Severity Level: {sev.upper()}   |   Status: {status}"))
    lines.append(("TEXT", f"Starting Location: {start_loc}   |   Emergency Epicenter: {em_loc}"))
    lines.append(("SPACE", ""))

    state = incident_data.get("state", {})
    blocked = sanitize_text(", ".join(str(e) for e in state.get("blocked_edges", [])) or "None")
    crowded = sanitize_text(", ".join(state.get("crowded_locations", [])) or "None")
    restricted = sanitize_text(", ".join(state.get("restricted_locations", [])) or "None")
    exits = sanitize_text(", ".join(state.get("available_exits", [])) or "None")

    lines.append(("SECTION", "2. ENVIRONMENTAL HAZARDS & CONSTRAINTS"))
    lines.append(("TEXT", f"Blocked Corridors: {blocked}"))
    lines.append(("TEXT", f"Crowded Locations (+5 cost penalty): {crowded}"))
    lines.append(("TEXT", f"Security Restricted Nodes (No Entry): {restricted}"))
    lines.append(("TEXT", f"Available Emergency Exits: {exits}"))
    lines.append(("SPACE", ""))

    decision = incident_data.get("decision", {})
    matched_rules = sanitize_text(", ".join(decision.get("matched_rules", [])) or "None")
    lines.append(("SECTION", "3. DECISION ENGINE & RULE RECOMMENDATIONS"))
    lines.append(("TEXT", f"Matched Rule IDs: {matched_rules}"))
    for rec in decision.get("recommendations", [])[:4]:
        lines.append(("BULLET", f"- {sanitize_text(rec)}"))
    lines.append(("SPACE", ""))

    routes = incident_data.get("routes", {})
    bfs = routes.get("BFS")
    astar = routes.get("A*")

    lines.append(("SECTION", "4. ALGORITHMIC ROUTING & EVACUATION PATHS"))
    if bfs:
        bfs_p = sanitize_text(" -> ".join(bfs.get("route", [])))
        lines.append(("TEXT", f"BFS Route (Unweighted Minimum Hops): {bfs_p}"))
        lines.append((
            "TEXT",
            f"   Route Cost: {bfs.get('route_cost')}   |   Time: {bfs.get('execution_time_ms', 0):.4f} ms   |   "
            f"Nodes: {bfs.get('nodes_expanded')}   |   Score: {bfs.get('score')}",
        ))
    else:
        lines.append(("TEXT", "BFS Route: No candidate evacuation path found."))

    if astar:
        astar_p = sanitize_text(" -> ".join(astar.get("route", [])))
        lines.append(("TEXT", f"Dijkstra / A* Route (Cost Optimal): {astar_p}"))
        lines.append((
            "TEXT",
            f"   Route Cost: {astar.get('route_cost')}   |   Time: {astar.get('execution_time_ms', 0):.4f} ms   |   "
            f"Nodes: {astar.get('nodes_expanded')}   |   Score: {astar.get('score')}",
        ))
    else:
        lines.append(("TEXT", "Dijkstra Route: No candidate evacuation path found."))
    lines.append(("SPACE", ""))

    lines.append(("SECTION", "5. INCIDENT LIFECYCLE & AUDIT TRAIL"))
    for item in incident_data.get("lifecycle", []):
        lines.append(("TEXT", f"Stage: {sanitize_text(item.get('stage'))} [{sanitize_text(item.get('status')).upper()}] - Time: {sanitize_text(item.get('time'))}"))
    lines.append(("SPACE", ""))

    lines.append(("LINE", "-" * 85))
    lines.append(("NOTICE", "DISCLAIMER: SIMULATION DATA ONLY. NOT A REAL-WORLD EMERGENCY DIRECTIVE."))
    lines.append(("NOTICE", "Campus Emergency Response Agent AI Academic Project (2026). Generated via internal control center."))

    # Compile into PDF stream
    stream_parts = []
    y = 790
    for kind, text in lines:
        if kind == "HEADER":
            stream_parts.append(f"BT /F2 14 Tf 45 {y} Td ({text}) Tj ET\n")
            y -= 18
        elif kind == "SUBHEADER":
            stream_parts.append(f"BT /F1 9 Tf 45 {y} Td ({text}) Tj ET\n")
            y -= 16
        elif kind == "SECTION":
            stream_parts.append(f"BT /F2 11 Tf 45 {y} Td ({text}) Tj ET\n")
            y -= 14
        elif kind == "BULLET":
            stream_parts.append(f"BT /F1 9 Tf 55 {y} Td ({text}) Tj ET\n")
            y -= 12
        elif kind == "NOTICE":
            stream_parts.append(f"BT /F2 8 Tf 45 {y} Td ({text}) Tj ET\n")
            y -= 11
        elif kind == "LINE":
            stream_parts.append(f"BT /F1 8 Tf 45 {y} Td ({text}) Tj ET\n")
            y -= 14
        elif kind == "SPACE":
            y -= 6
        else:
            stream_parts.append(f"BT /F1 9.5 Tf 45 {y} Td ({text}) Tj ET\n")
            y -= 13

    content_bytes = "".join(stream_parts).encode("latin1")

    # Construct minimal valid PDF 1.4
    objs = [
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n",
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n",
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 4 0 R /Resources << /Font << /F1 5 0 R /F2 6 0 R >> >> >>\nendobj\n",
        f"4 0 obj\n<< /Length {len(content_bytes)} >>\nstream\n".encode("latin1") + content_bytes + b"\nendstream\nendobj\n",
        b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n",
        b"6 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>\nendobj\n",
    ]

    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for obj in objs:
        offsets.append(len(out))
        out.extend(obj)
    startxref = len(out)
    out.extend(f"xref\n0 {len(objs)+1}\n0000000000 65535 f \n".encode("latin1"))
    for off in offsets:
        out.extend(f"{off:010d} 00000 n \n".encode("latin1"))
    out.extend(f"trailer\n<< /Size {len(objs)+1} /Root 1 0 R >>\nstartxref\n{startxref}\n%%EOF\n".encode("latin1"))

    return bytes(out)
