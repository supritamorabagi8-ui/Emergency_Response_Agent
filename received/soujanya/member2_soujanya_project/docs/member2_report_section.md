# Member 2 – Actions and Decision Rules

## 1. Objective

The responsibility of Member 2 is to define the actions that the Emergency
Response Decision Agent can recommend and to implement transparent decision
rules. The purpose is to convert the current emergency state into a set of
appropriate responses. The module is designed to work with the campus
environment and state representation prepared by Member 1 and the route
search algorithms implemented by Member 4.

## 2. Possible actions

An action is an operation or recommendation that an intelligent agent can
perform after receiving information from its environment. In this project,
actions are represented using short action IDs and corresponding descriptions.

| Action ID | Meaning |
|---|---|
| `avoid_danger_area` | Avoid entering a known emergency-affected area |
| `avoid_blocked_corridor` | Do not traverse a blocked edge |
| `avoid_crowded_location` | Prefer a route with less crowd exposure |
| `avoid_restricted_area` | Do not enter a restricted location |
| `select_alternative_exit` | Allow the route planner to compare available exits |
| `notify_security` | Simulated security notification |
| `notify_medical_team` | Simulated medical-team notification |
| `check_power_failure` | Re-check route options under power-failure conditions |
| `report_no_safe_route` | Report that no safe route can be recommended |

## 3. Decision rules

The system uses rule-based reasoning. Each rule follows the IF–THEN structure.

| Rule | IF condition | THEN recommendation |
|---|---|---|
| R1 | Emergency type is fire | Avoid entering the fire-affected area and notify security |
| R2 | Emergency type is medical | Notify the simulated medical team |
| R3 | A corridor is blocked | Do not use the blocked connection |
| R4 | A location is crowded | Apply a crowd penalty when evaluating routes |
| R5 | A location is security-restricted | Do not enter the restricted location and notify security |
| R6 | Power failure is reported | Re-check route options and notify security |
| R7 | More than one exit is available | Compare the available exits using route search |
| R8 | No exit is available | Report that no safe exit is available |

More than one rule may activate at the same time. For example, a fire may occur
while a corridor is blocked and the Main Gate is crowded. The agent should
therefore collect all applicable recommendations rather than stopping after
the first rule.

## 4. Rational action selection

A rational action is an action that is expected to maximize the agent's
performance measure based on the information currently available. For this
simulation, the main considerations are:

1. Do not plan through blocked corridors.
2. Do not enter restricted locations.
3. Avoid known danger locations when selecting onward movement.
4. Consider crowd exposure as an additional route cost.
5. Consider only exits marked as available.
6. If no valid route can be found, report failure instead of inventing a route.

The action module produces recommendations. The search algorithm is
responsible for verifying route connectivity and selecting a path. This
separation makes the system easier to test and explain.

## 5. Illustrative example

Input:

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

Expected action recommendations include:
- avoid entering the known fire-affected area;
- notify campus security (simulated);
- avoid the blocked A–B corridor;
- consider crowd exposure at G1;
- compare available exits G1 and G2.

The final route is not determined by this module. Member 4's route planner
must verify which exit can be reached without violating the constraints.

## 6. Implementation summary

The implementation is divided into two Python files:

- `actions.py` stores the action catalogue and implements
  `get_possible_actions(state)`.
- `decision_rules.py` evaluates the IF–THEN conditions in
  `apply_rules(state)` and returns a structured decision dictionary.

The code uses ordinary Python dictionaries and lists, so it can be integrated
with the other project modules without installing extra libraries.

## 7. Limitations

- The module operates on simulated inputs; it does not use physical sensors.
- Notifications are descriptions only; no real security or medical message is sent.
- A rule can only respond to information present in the input state.
- The module does not calculate distances or guarantee a safe route.
- If the route planner discovers that every available exit is unreachable,
  it must report no safe route even when the input lists one or more exits.
- A starting location may itself be the emergency location. The route planner
  must allow the agent to leave its starting node while preventing it from
  entering the hazard again, according to the agreed team policy.

## 8. Conclusion

Member 2's module provides a transparent action catalogue and rule-based
decision mechanism. It converts emergency conditions into understandable
recommendations and supplies the route planner with the constraints that
must be considered. This supports explainability, modular development, and
testing of the complete Emergency Response Decision Agent.

**Project disclaimer:** This is an academic simulation only. It is not a
validated real-world evacuation or emergency-response system.
