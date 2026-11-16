"""
Original Procedural Emergency Siren Engine & Alert Sound Controller.
Generates an authentic dual-tone emergency siren in pure Python (zero external dependencies).
Handles browser autoplay policies, rerun debouncing, volume control, and stop/acknowledge triggers.
"""

import base64
import datetime
import io
import math
import struct
import wave
import streamlit as st
import streamlit.components.v1 as components

from ui.state_manager import acknowledge_current_alert, log_audit_event, stop_siren
from ui.theme import render_html


@st.cache_data(show_spinner=False)
def generate_siren_wav_base64(duration_seconds: float = 2.4, sample_rate: int = 22050) -> str:
    """
    Generate an authentic, procedural wailing emergency siren audio in WAV format.
    Completely original, royalty-free, and requires zero external files or network access.
    """
    num_samples = int(duration_seconds * sample_rate)
    buffer = io.BytesIO()

    with wave.open(buffer, "wb") as wf:
        wf.setnchannels(1)  # Mono channel
        wf.setsampwidth(2)  # 16-bit PCM
        wf.setframerate(sample_rate)

        frames = bytearray()
        phase = 0.0

        for i in range(num_samples):
            t = i / sample_rate
            # 1.25 Hz frequency sweep cycling smoothly between 750 Hz and 1250 Hz
            instant_freq = 950.0 + 300.0 * math.sin(2.0 * math.pi * 1.25 * t)
            phase += 2.0 * math.pi * instant_freq / sample_rate

            # Primary oscillation with harmonic undertone
            sample_val = 0.85 * math.sin(phase) + 0.15 * math.sin(2.0 * phase)
            scaled = int(26000.0 * sample_val)
            clamped = max(-32768, min(32767, scaled))
            frames.extend(struct.pack("<h", clamped))

        wf.writeframes(frames)

    wav_bytes = buffer.getvalue()
    b64_str = base64.b64encode(wav_bytes).decode("ascii")
    return f"data:audio/wav;base64,{b64_str}"


def trigger_test_alert():
    """Trigger a simulated emergency alert for testing the siren and visual warnings."""
    now_str = datetime.datetime.now().strftime("%H:%M:%S")
    test_id = f"ALERT-TEST-{datetime.datetime.now().strftime('%M%S')}"

    st.session_state.active_alert = {
        "alert_id": test_id,
        "incident_id": "DRILL-001",
        "type": "General Alarm Drill",
        "location": "Academic Block A",
        "severity": "Critical",
        "timestamp": now_str,
        "route_found": True,
        "acknowledged": False,
    }
    st.session_state.siren_active = st.session_state.sound_enabled
    st.session_state.alert_history.insert(0, st.session_state.active_alert.copy())
    log_audit_event("TEST_ALERT_TRIGGERED", "Operator initiated test emergency drill.")


def render_audio_controller():
    """
    Renders the active alert banner, siren controls, and audio player.
    Guarantees audio does not repeatedly loop on unrelated Streamlit reruns.
    """
    active_alert = st.session_state.get("active_alert")
    siren_active = st.session_state.get("siren_active", False)
    sound_enabled = st.session_state.get("sound_enabled", True)
    volume = st.session_state.get("sound_volume", 0.8)

    # 1. Render active emergency banner if alert exists and is unacknowledged
    if active_alert and not active_alert.get("acknowledged", False):
        alert_type = active_alert.get("type", "Emergency")
        loc = active_alert.get("location", "Campus")
        severity = active_alert.get("severity", "Critical")

        render_html(
            f"""
            <div class="alert-banner-active">
                <div>
                    <div class="alert-banner-title">
                        🚨 {severity.upper()} EMERGENCY ALERT: {alert_type.upper()}
                    </div>
                    <div style="font-size:14px; color:#FFFFFF; margin-top:6px;">
                        <strong style="color:#FFFFFF;">Location:</strong> {loc} &nbsp;|&nbsp;
                        <strong style="color:#FFFFFF;">Alert ID:</strong> {active_alert.get('alert_id')} &nbsp;|&nbsp;
                        <strong style="color:#FFFFFF;">Timestamp:</strong> {active_alert.get('timestamp')} &nbsp;|&nbsp;
                        <strong style="color:#FFFFFF;">Status:</strong> Active Alarm • Awaiting Operator Acknowledgment
                    </div>
                </div>
            </div>
            """
        )

        # Quick action buttons for the active alert
        col1, col2, col3 = st.columns([2, 2, 4])
        with col1:
            if st.button("🔕 STOP SIREN", key="btn_stop_siren", width="stretch"):
                stop_siren()
                st.rerun()
        with col2:
            if st.button("✅ ACKNOWLEDGE ALERT", key="btn_ack_alert", width="stretch"):
                acknowledge_current_alert()
                st.rerun()
        with col3:
            st.caption("Acknowledge to record operator response timestamp and silence alarms.")

    # 2. Audio playback with rerun debouncing
    should_play = False
    if siren_active and sound_enabled and active_alert:
        current_id = active_alert.get("alert_id")
        last_played = st.session_state.get("last_played_alert_id")

        if current_id != last_played:
            should_play = True
            st.session_state.last_played_alert_id = current_id

    if should_play:
        siren_uri = generate_siren_wav_base64()
        # Invisible HTML5 audio player that plays once for this alert
        audio_html = f"""
        <audio id="siren_player" autoplay>
            <source src="{siren_uri}" type="audio/wav">
        </audio>
        <script>
            var audio = document.getElementById("siren_player");
            if (audio) {{
                audio.volume = {volume};
                audio.play().catch(function(e) {{
                    console.log("Audio autoplay restricted until user interaction:", e);
                }});
            }}
        </script>
        """
        components.html(audio_html, height=0, width=0)
