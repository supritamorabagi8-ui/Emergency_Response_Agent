
# ==========================================
# Emergency Response Agent
# Emergency State Management
# ==========================================

from environment.campus_graph import (
    START_LOCATIONS,
    EMERGENCY_EXITS
)


def create_emergency_state(
    start,
    emergency_type,
    emergency_location=None,
    blocked_edges=None,
    crowded_locations=None,
    restricted_locations=None,
    available_exits=None
):
    """
    Creates the current emergency environment state.
    """

    state = {
        "start": start,
        "emergency_type": emergency_type,
        "emergency_location": emergency_location,

        "blocked_edges": blocked_edges or [],
        "crowded_locations": crowded_locations or [],
        "restricted_locations": restricted_locations or [],

        "available_exits": (
            available_exits
            if available_exits is not None
            else EMERGENCY_EXITS.copy()
        )
    }

    return state
