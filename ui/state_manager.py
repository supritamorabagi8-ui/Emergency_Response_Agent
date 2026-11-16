"""
Session state manager for Emergency Response Agent AI.
Handles multi-incident tracking, audit logging, alert debouncing, and role management.
"""

import datetime
import streamlit as st


def init_session_state():
    """Initialize all persistent session state variables."""
    if "nav_page" not in st.session_state:
        st.session_state.nav_page = "1. Command Center"

    if "user_role" not in st.session_state or st.session_state.user_role not in ["Administrator", "Security Officer", "Campus Observer"]:
        st.session_state.user_role = "Administrator"

    if "sound_enabled" not in st.session_state:
        st.session_state.sound_enabled = True

    if "sound_volume" not in st.session_state:
        st.session_state.sound_volume = 0.8

    if "siren_active" not in st.session_state:
        st.session_state.siren_active = False

    if "last_played_alert_id" not in st.session_state:
        st.session_state.last_played_alert_id = None

    if "active_alert" not in st.session_state:
        st.session_state.active_alert = None

    if "alert_history" not in st.session_state:
        st.session_state.alert_history = []

    if "last_result" not in st.session_state:
        st.session_state.last_result = None

    if "incidents" not in st.session_state:
        st.session_state.incidents = {}

    if "active_incident_id" not in st.session_state:
        st.session_state.active_incident_id = None

    if "audit_logs" not in st.session_state:
        st.session_state.audit_logs = []

    if "speech_enabled" not in st.session_state:
        st.session_state.speech_enabled = True

    if "speech_lang" not in st.session_state:
        st.session_state.speech_lang = "en-US"

    if "high_contrast" not in st.session_state:
        st.session_state.high_contrast = False


def log_audit_event(event_type: str, details: str, incident_id: str = None):
    """Record an immutable event in the chronological audit log."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {
        "timestamp": now,
        "event_type": event_type,
        "incident_id": incident_id or st.session_state.get("active_incident_id", "N/A"),
        "role": st.session_state.get("user_role", "Admin"),
        "details": details,
    }
    st.session_state.audit_logs.insert(0, entry)


def register_new_incident(
    emergency_type: str,
    start: str,
    emergency_location: str,
    severity: str,
    routes: dict,
    decision: dict,
    state: dict,
):
    """Register and store an incident across the multi-incident system."""
    now = datetime.datetime.now()
    incident_num = len(st.session_state.incidents) + 1
    incident_id = f"INC-{now.strftime('%Y%m%d')}-{incident_num:03d}"
    alert_id = f"ALERT-{now.strftime('%H%M%S')}-{incident_num:02d}"

    bfs = routes.get("BFS")
    astar = routes.get("A*")
    route_found = (bfs is not None) or (astar is not None)

    incident_data = {
        "id": incident_id,
        "alert_id": alert_id,
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "type": emergency_type.title(),
        "severity": severity,
        "start": start,
        "emergency_location": emergency_location or "Unspecified",
        "route_found": route_found,
        "status": "Candidate Route Calculated" if route_found else "Analyzed (No Route)",
        "acknowledged": False,
        "acknowledged_time": None,
        "routes": routes,
        "decision": decision,
        "state": state,
        "lifecycle": [
            {"stage": "Reported", "time": now.strftime("%H:%M:%S"), "status": "done"},
            {"stage": "Validated", "time": now.strftime("%H:%M:%S"), "status": "done"},
            {"stage": "Analyzed", "time": now.strftime("%H:%M:%S"), "status": "done"},
            {
                "stage": "Candidate Route Calculated" if route_found else "Exhausted (No Route)",
                "time": now.strftime("%H:%M:%S"),
                "status": "done",
            },
            {"stage": "Alert Generated", "time": now.strftime("%H:%M:%S"), "status": "done"},
            {"stage": "Acknowledged", "time": "-", "status": "pending"},
            {"stage": "Resolved", "time": "-", "status": "pending"},
        ],
    }

    st.session_state.incidents[incident_id] = incident_data
    st.session_state.active_incident_id = incident_id

    # Configure active alert
    st.session_state.active_alert = {
        "alert_id": alert_id,
        "incident_id": incident_id,
        "type": emergency_type.title(),
        "location": emergency_location or start,
        "severity": severity,
        "timestamp": now.strftime("%H:%M:%S"),
        "route_found": route_found,
        "acknowledged": False,
    }

    # Append to alert history
    st.session_state.alert_history.insert(0, st.session_state.active_alert.copy())

    # Set siren active if sound is enabled
    st.session_state.siren_active = st.session_state.sound_enabled

    # Audit log
    log_audit_event(
        "EMERGENCY_ANALYZED",
        f"Analyzed {emergency_type.upper()} at {emergency_location or start}. Route found: {route_found}",
        incident_id,
    )

    return incident_id, alert_id


def acknowledge_current_alert():
    """Acknowledge active alert and silence the siren."""
    if st.session_state.active_alert:
        st.session_state.active_alert["acknowledged"] = True
        incident_id = st.session_state.active_alert.get("incident_id")
        if incident_id and incident_id in st.session_state.incidents:
            inc = st.session_state.incidents[incident_id]
            inc["acknowledged"] = True
            now_str = datetime.datetime.now().strftime("%H:%M:%S")
            inc["acknowledged_time"] = now_str
            for stage in inc["lifecycle"]:
                if stage["stage"] == "Acknowledged":
                    stage["status"] = "done"
                    stage["time"] = now_str

        st.session_state.siren_active = False
        log_audit_event("ALERT_ACKNOWLEDGED", "Operator acknowledged active emergency alert.")


def stop_siren():
    """Silence the siren immediately without changing acknowledgement status."""
    st.session_state.siren_active = False
    log_audit_event("SIREN_SILENCED", "Operator silenced siren sound.")


def reset_simulation():
    """Reset current active simulation state safely."""
    st.session_state.active_alert = None
    st.session_state.siren_active = False
    st.session_state.last_result = None
    st.session_state.active_incident_id = None
    log_audit_event("SIMULATION_RESET", "Operator reset active simulation state.")
