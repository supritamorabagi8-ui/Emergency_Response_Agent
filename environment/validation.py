# ==========================================
# Emergency Response Agent
# Input Validation
# ==========================================

from environment.campus_graph import LOCATIONS


def validate_location(location):
    """Check whether a location exists in the campus."""

    return location in LOCATIONS


def validate_emergency_type(emergency_type):
    """Check whether the emergency type is valid."""

    valid_types = ["fire", "medical", "security", "other"]

    return emergency_type.lower() in valid_types


def validate_emergency_input(start, emergency_type):

    if not validate_location(start):
        return False, "Invalid starting location."

    if not validate_emergency_type(emergency_type):
        return False, "Invalid emergency type."

    return True, "Input is valid."