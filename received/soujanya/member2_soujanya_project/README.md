# Member 2 – Actions and Decision Rules
## Emergency Response Decision Agent

This folder is the complete standalone contribution for **Member 2 (Soujanya)**.
It contains the action catalogue, transparent IF–THEN decision rules, a runnable
example, and unit tests.

## 1. What this module does

The agent receives a normalized emergency-state dictionary and recommends
actions such as:
- avoid a known fire-affected area;
- avoid blocked corridor connections;
- reduce exposure to crowded locations;
- avoid security-restricted locations;
- notify campus security or the medical team (simulated);
- consider alternative available exits;
- report when no exit is available.

**Important:** this module does not calculate or guarantee an evacuation route.
Member 4's BFS/A* route planner must determine whether a route actually exists.
Crowded locations should normally add a route cost/penalty rather than being
automatically treated as blocked. Blocked edges and restricted locations are
hard constraints.

## 2. Files

| File | Purpose |
|---|---|
| `actions.py` | Defines action descriptions and `get_possible_actions(state)` |
| `decision_rules.py` | Applies IF–THEN rules and returns structured recommendations |
| `main.py` | Runs a standalone sample |
| `tests/test_member2.py` | Unit tests for common emergency cases |
| `docs/member2_report_section.md` | Report-ready theory, rules, and implementation explanation |

## 3. Run in VS Code / terminal

1. Extract the ZIP file.
2. Open the extracted `member2_soujanya_project` folder in VS Code.
3. Open Terminal → New Terminal.
4. Run:

```bash
python main.py
```

5. Run the tests:

```bash
python -m unittest discover -s tests -v
```

Python 3.9 or later is recommended. No external package is required.

## 4. Input format shared with the team

```python
emergency_data = {
    "emergency_type": "fire",
    "emergency_location": "A",
    "current_location": "A",
    "blocked_edges": [("A", "B")],
    "crowded_locations": ["G1"],
    "restricted_locations": [],
    "available_exits": ["G1", "G2"],
    "power_failure": False
}
```

Use only the agreed campus IDs:
A, B, L, C, M, P, G1, G2.
Emergency types:
`fire`, `medical`, `blocked_corridor`, `heavy_crowd`,
`security_restriction`, `power_failure`.

## 5. Integration with other members

Member 1 should pass the validated state returned by `create_state(data)`.
Member 2 calls:

```python
from actions import get_possible_actions
from decision_rules import apply_rules

possible_actions = get_possible_actions(state)
decision = apply_rules(state)
```

`decision` contains:
- `actions`: machine-readable action IDs;
- `recommendations`: human-readable action descriptions;
- `matched_rules`: rule IDs that fired;
- `status`: whether an exit was supplied in the input.

Member 4 should use the same `blocked_edges`, `restricted_locations`,
`crowded_locations`, and `available_exits` when running BFS/A*. If the route
planner cannot reach any available exit, it must return a no-safe-route result
even if `available_exits` is non-empty.

## 6. Safety and project scope

This is an educational campus simulation, not a real emergency-management,
dispatch, or evacuation system. Do not use it as operational safety advice.
Real emergencies must be handled by campus authorities and emergency services.
The priority examples are illustrative; real response priorities depend on
trained emergency protocols and the circumstances.
