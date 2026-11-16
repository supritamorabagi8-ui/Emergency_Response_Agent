
"""
Emergency Response Agent - Campus Graph
Weighted undirected campus network.
"""

LOCATIONS = {
    "A": "Academic Block A",
    "B": "Academic Block B",
    "L": "Library",
    "C": "Canteen",
    "M": "Medical Centre",
    "P": "Parking Area",
    "G1": "Main Gate",
    "G2": "Gate 2",
}

CAMPUS_GRAPH = {
    "A": {"B": 4, "L": 3},
    "B": {"A": 4, "L": 2, "C": 5},
    "L": {"A": 3, "B": 2, "C": 2, "M": 3},
    "C": {"B": 5, "L": 2, "M": 4, "P": 3},
    "M": {"L": 3, "C": 4, "P": 2},
    "P": {"C": 3, "M": 2, "G1": 4, "G2": 5},
    "G1": {"P": 4},
    "G2": {"P": 5},
}

EMERGENCY_EXITS = ["G1", "G2"]

START_LOCATIONS = ["A", "B", "L", "C", "M", "P"]


def validate_campus_graph():
    """Check that all graph nodes and edges are valid."""

    if set(CAMPUS_GRAPH) != set(LOCATIONS):
        raise ValueError("Campus graph and location definitions do not match.")

    for node, neighbors in CAMPUS_GRAPH.items():
        for neighbor, weight in neighbors.items():

            if neighbor not in CAMPUS_GRAPH:
                raise ValueError(f"Unknown connected node: {neighbor}")

            if weight <= 0:
                raise ValueError(f"Invalid corridor weight: {node} -> {neighbor}")

            if CAMPUS_GRAPH[neighbor].get(node) != weight:
                raise ValueError(
                    f"Undirected connection mismatch: {node} -> {neighbor}"
                )

    for exit_node in EMERGENCY_EXITS:
        if exit_node not in CAMPUS_GRAPH:
            raise ValueError(f"Invalid emergency exit: {exit_node}")

    return True


validate_campus_graph()
