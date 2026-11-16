"""
Reports & Documentation View for Emergency Operations Command Center.
Allows exporting incident summaries, downloading benchmark CSVs, and generating official PDF dossiers.
"""

import os
import pandas as pd
import streamlit as st

from ui.pdf_export import generate_pdf_report
from ui.theme import render_disclaimer, render_html, render_page_header


def render_reports_view():
    """Render the Emergency Reports & Documentation Page."""
    render_page_header(
        "📄 Emergency Incident Reports & Audit Export",
        "Generate Formatted Official Incident Dossiers, Download CSV Data, and Maintain Response Archives",
        badge_text="DOCUMENTATION ARCHIVE",
    )

    incidents = st.session_state.get("incidents", {})

    st.markdown("### 🖨️ Generate Official PDF Incident Report")
    if incidents:
        sel_id = st.selectbox("Select Incident Dossier to Export", list(incidents.keys()))
        inc = incidents[sel_id]

        render_html(
            f"""
            <div class="glass-card" style="border-left: 4px solid #8B5CF6;">
                <h4 style="color:#FFFFFF; margin:0 0 6px 0;">Dossier: {inc['id']} — {inc['type']} Emergency</h4>
                <div style="font-size:13px; color:#FFFFFF;">
                    Location: <strong style="color:#FFFFFF;">{inc['emergency_location']}</strong> &nbsp;|&nbsp; 
                    Severity: <strong style="color:#FFFFFF;">{inc['severity']}</strong> &nbsp;|&nbsp; 
                    Timestamp: <span style="color:#FFFFFF;">{inc['timestamp']}</span>
                </div>
            </div>
            """
        )

        pdf_bytes = generate_pdf_report(inc)
        st.download_button(
            label=f"⬇️ DOWNLOAD OFFICIAL PDF DOSSIER ({inc['id']})",
            data=pdf_bytes,
            file_name=f"Incident_Report_{inc['id']}.pdf",
            mime="application/pdf",
            width="stretch",
        )
    else:
        st.info("No active incidents currently logged. Trigger an incident in 'Emergency Analysis' to generate a PDF report.")

    render_html("<hr style='border-color:#3A2854; margin:22px 0;'>")
    st.markdown("### 📊 Export Benchmark Experiment CSV")

    csv_path = "performance/experiment_results.csv"
    if os.path.exists(csv_path):
        df_bench = pd.read_csv(csv_path)
        csv_bytes = df_bench.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ DOWNLOAD 12-RUN BENCHMARK EXPERIMENT RESULTS (CSV)",
            data=csv_bytes,
            file_name="campus_benchmark_experiments.csv",
            mime="text/csv",
            width="stretch",
        )
    else:
        st.warning("Benchmark CSV file not found.")

    render_html("<hr style='border-color:#3A2854; margin:22px 0;'>")
    st.markdown("### 📜 System Event Audit Ledger (CSV)")
    audit_logs = st.session_state.get("audit_logs", [])
    if audit_logs:
        df_audit = pd.DataFrame(audit_logs)
        st.dataframe(df_audit, use_container_width=True)
        csv_audit = df_audit.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ DOWNLOAD SYSTEM AUDIT LOG (CSV)",
            data=csv_audit,
            file_name="system_audit_logs.csv",
            mime="text/csv",
            width="stretch",
        )
    else:
        st.info("Audit log is currently empty.")

    render_disclaimer()
