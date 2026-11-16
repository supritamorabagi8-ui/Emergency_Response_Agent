"""
Multilingual Voice Announcement Engine for Emergency Response Agent AI.
Supports English and Kannada (ಕನ್ನಡ) browser-based speech announcements using the Web Speech API.
"""

import json
import streamlit as st
import streamlit.components.v1 as components


ANNOUNCEMENTS = {
    "en": {
        "fire": "Fire emergency reported near {location}. Please follow the available candidate evacuation route.",
        "medical": "Medical emergency reported at {location}. Simulated medical response teams have been notified.",
        "security": "Security restriction reported near {location}. Please avoid this area and proceed to the designated exit.",
        "other": "Emergency situation reported near {location}. Please consult the evacuation dashboard for candidate routes.",
        "drill": "This is a simulated campus emergency drill. Follow the designated candidate evacuation routes.",
        "no_route": "Warning: No safe evacuation route currently identified. Shelter in place and await further security guidance.",
    },
    "kn": {
        "fire": "{location} ಸಮೀಪ ಬೆಂಕಿ ಅವಘಡದ ಅನುಕರಣೆ ವರದಿಯಾಗಿದೆ. ದಯವಿಟ್ಟು ಲಭ್ಯವಿರುವ ನಿರ್ಗಮನ ಮಾರ್ಗವನ್ನು ಅನುಸರಿಸಿ.",
        "medical": "{location} ನಲ್ಲಿ ವೈದ್ಯಕೀಯ ತುರ್ತು ಪರಿಸ್ಥಿತಿಯ ಅನುಕರಣೆ ವರದಿಯಾಗಿದೆ. ವೈದ್ಯಕೀಯ ತಂಡಕ್ಕೆ ಸೂಚಿಸಲಾಗಿದೆ.",
        "security": "{location} ನಲ್ಲಿ ಭದ್ರತಾ ನಿರ್ಬಂಧದ ಅನುಕರಣೆ ವರದಿಯಾಗಿದೆ. ಈ ಪ್ರದೇಶವನ್ನು ತಪ್ಪಿಸಿ ನಿರ್ಗಮನದತ್ತ ಸಾಗಿ.",
        "other": "{location} ನಲ್ಲಿ ತುರ್ತು ಪರಿಸ್ಥಿತಿಯ ಅನುಕರಣೆ ವರದಿಯಾಗಿದೆ. ದಯವಿಟ್ಟು ನಿರ್ಗಮನ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್ ಪರಿಶೀಲಿಸಿ.",
        "drill": "ಇದು ಕ್ಯಾಂಪಸ್ ತುರ್ತು ಪರಿಸ್ಥಿತಿಯ ಅನುಕರಣಾ ಕವಾಯಿತು. ಸೂಚಿಸಲಾದ ನಿರ್ಗಮನ ಮಾರ್ಗವನ್ನು ಅನುಸರಿಸಿ.",
        "no_route": "ಎಚ್ಚರಿಕೆ: ಪ್ರಸ್ತುತ ಯಾವುದೇ ಸುರಕ್ಷಿತ ನಿರ್ಗಮನ ಮಾರ್ಗ ಲಭ್ಯವಿಲ್ಲ. ಇದ್ದ ಸ್ಥಳದಲ್ಲೇ ಇರಿ ಮತ್ತು ಭದ್ರತಾ ಸೂಚನೆಗಳನ್ನು ನಿರೀಕ್ಷಿಸಿ.",
    },
}


def get_announcement_text(emergency_type: str, location: str, lang: str = "en") -> str:
    """Retrieve translated announcement template and interpolate variables."""
    lang_key = "kn" if "kn" in lang.lower() else "en"
    key = emergency_type.lower() if emergency_type.lower() in ANNOUNCEMENTS[lang_key] else "other"
    template = ANNOUNCEMENTS[lang_key][key]
    return template.format(location=location or "the campus")


def render_voice_announcer(text: str, lang: str = "en-US", auto_play: bool = False):
    """
    Render a browser-native Web Speech synthesis controller.
    Runs client-side in the user's browser with zero external API calls.
    """
    speech_js = f"""
    <div style="background:#0a192f; border:1px solid #1e3a5f; border-radius:10px; padding:14px; margin-top:12px;">
        <div style="font-size:13px; font-weight:700; color:#38bdf8; margin-bottom:8px; display:flex; align-items:center; gap:8px;">
            📢 VOICE ANNOUNCEMENT SYSTEM ({'ಕನ್ನಡ' if 'kn' in lang else 'ENGLISH'})
        </div>
        <p style="font-size:14px; color:#e2e8f0; margin-bottom:12px; font-style:italic;">
            "{text}"
        </p>
        <div style="display:flex; gap:10px;">
            <button onclick="playAnnouncement()" style="background:#0284c7; color:white; border:none; border-radius:6px; padding:6px 14px; font-weight:600; cursor:pointer;">
                ▶️ Play Announcement
            </button>
            <button onclick="stopAnnouncement()" style="background:#475569; color:white; border:none; border-radius:6px; padding:6px 14px; font-weight:600; cursor:pointer;">
                ⏹️ Stop
            </button>
        </div>
    </div>

    <script>
        var currentText = {json.dumps(text)};
        var currentLang = {json.dumps(lang)};

        function playAnnouncement() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                var utterance = new SpeechSynthesisUtterance(currentText);
                utterance.lang = currentLang;
                utterance.rate = 0.95;
                window.speechSynthesis.speak(utterance);
            }} else {{
                alert("Web Speech API not supported in this browser.");
            }}
        }}

        function stopAnnouncement() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
            }}
        }}

        {'playAnnouncement();' if auto_play else ''}
    </script>
    """
    components.html(speech_js, height=130)
