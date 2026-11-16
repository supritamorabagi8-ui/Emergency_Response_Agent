# Member 3 – Performance Measure and Environment Types

## 1. Introduction

The responsibility of Member 3 is to define how the Emergency Response
Decision Agent is evaluated and to explain how different environment
properties affect its decisions. An agent is rational when it selects an
action expected to perform well according to its performance measure, using
the percepts available to it. Rationality does not mean that the agent always
knows the true state or always achieves a perfect result.

## 2. Performance measure

A performance measure specifies how success is evaluated. In this project,
the following metrics are used:

| Metric | Meaning | Desired behaviour |
|---|---|---|
| Goal achievement | Whether a valid available exit is reached in the simulation | High |
| Route validity | Whether the route avoids blocked edges and restricted locations | 100% valid routes |
| Route cost | Sum of edge costs, including crowd penalties | Lower, subject to constraints |
| Nodes expanded | Number of graph nodes explored by the search | Lower for comparable problems |
| Execution time | Time taken by the search, measured in milliseconds | Lower |
| Composite score | Illustrative score combining selected metrics | Higher |

Safety constraints must take precedence over a short route. A shorter route is
not better if it crosses a blocked corridor or restricted area.

## 3. Illustrative scoring model

The project uses a configurable educational score:

- 50 points for reaching an available goal exit;
- 25 points for a valid route;
- up to 15 points for a low route cost;
- up to 10 points for quick execution;
- a large penalty for an unsafe route.

The exact weights are project assumptions used to demonstrate a performance
measure. They are not clinically or operationally validated safety values.
The score is capped between 0 and 100. An unsafe route should never be
presented as acceptable merely because its total score is high.

## 4. Rationality

A rational agent chooses the action that maximizes expected performance based
on its current percepts, available actions, knowledge and performance measure.

For this campus simulation, rational decisions should:
1. avoid known blocked corridor edges;
2. avoid known restricted locations;
3. avoid re-entering a known emergency area;
4. consider crowd exposure as a soft route cost;
5. consider only exits reported as available;
6. report failure if no valid route can be found.

If crowd status at Gate 2 is unknown, the agent cannot claim that Gate 2 is
uncrowded. It should request an update or mark the decision as uncertain.

## 5. Nature of the environment

### Fully observable

The agent receives all relevant information needed for the simulation:
emergency location, blocked corridors, crowd levels, restricted locations and
available exit status.

### Partially observable

Some relevant information is missing. For example, the crowd status at G2
may be unknown. The agent should preserve that uncertainty rather than
silently assuming the location is safe.

### Static

The environment does not change while the agent is deciding. The same
corridors, hazards and crowd levels remain in place for the duration of a run.

### Dynamic

The environment can change during operation. For example, a connection
between Parking Area P and Main Gate G1 may become unavailable. The agent
must update its state and search again.

| Environment property | Simulation example |
|---|---|
| Fully observable | All exit and crowd information is supplied |
| Partially observable | Crowd status at G2 is unknown |
| Static | No graph or hazard changes during one run |
| Dynamic | P-G1 closes and the route is recalculated |

## 6. Experimental methodology

The project runs six scenarios:

| Experiment | Conditions | What it demonstrates |
|---|---|---|
| E1 | Normal campus | Baseline route search |
| E2 | Fire in A; A-B blocked | Blocked corridor handling |
| E3 | G1 crowded | Crowd penalty can change route choice |
| E4 | B restricted | Restricted location avoidance |
| E5 | G2 crowd status unknown | Partial observability and uncertainty |
| E6 | P-G1 closes | Dynamic environment and replanning |

BFS and A* are run against the same graph scenarios. The program records
route, goal achievement, route validity, route cost, nodes expanded and
execution time. Actual timing values are generated on the computer running
the experiment and should be recorded from the program output.

## 7. BFS and A* comparison

BFS explores the graph level by level and finds a path with the fewest edges
when all edges have equal cost. A* uses a cost function `f(n) = g(n) + h(n)`,
where `g(n)` is the cost so far and `h(n)` estimates the remaining cost.

The standalone benchmark uses a conservative `h(n)=0`, which is admissible
but makes A* behave like uniform-cost search. This avoids claiming an
unverified heuristic advantage on the small agreed campus graph. Member 4's
integrated A* may use a stronger heuristic only if it is proven not to
overestimate the remaining route cost.

BFS optimizes hop count. A* in the integrated system may optimize weighted
route cost, including crowd penalties. Comparisons must state which objective
is being optimized.

## 8. Results table template

Run `python main.py`. The program prints measured results and writes
`experiment_results.csv`.

| Scenario | Algorithm | Route | Nodes expanded | Execution time (ms) | Route cost | Score |
|---|---|---|---:|---:|---:|---:|
| E1 Normal | BFS | Record output | Record output | Record output | Record output | Record output |
| E1 Normal | A* | Record output | Record output | Record output | Record output | Record output |
| E2 Fire + blocked | BFS | Record output | Record output | Record output | Record output | Record output |
| E2 Fire + blocked | A* | Record output | Record output | Record output | Record output | Record output |

Do not invent results. Run the code and paste your actual output into the
final report. Execution time can vary between computers and repeated runs.

## 9. Conclusion

Performance measures make it possible to evaluate whether the agent's
decisions satisfy the project goals. Environment comparisons demonstrate that
the same agent may behave differently when information is incomplete or
conditions change. The experiments provide measurable evidence through
success, route validity, route cost, nodes expanded and execution time.

## 10. Viva questions and answers

**Q1. What is a performance measure?**  
It is the criterion used to evaluate how successfully an agent performs.

**Q2. What makes an action rational?**  
It is the action expected to maximize the performance measure using the
available percepts and knowledge.

**Q3. Does rationality mean always being correct?**  
No. A rational agent makes the best decision it can with the information
available, even when information is incomplete.

**Q4. What is a fully observable environment?**  
An environment in which the agent receives all relevant information.

**Q5. What is a partially observable environment?**  
An environment in which some relevant information is missing or uncertain.

**Q6. What is a static environment?**  
An environment that does not change while the agent is deciding.

**Q7. What is a dynamic environment?**  
An environment that may change while the agent is operating.

**Q8. Why measure nodes expanded?**  
It indicates how much of the search space an algorithm explores.

**Q9. Why measure execution time?**  
It measures how long the algorithm takes to produce a result on the tested
computer and input.

**Q10. What is the difference between BFS and A*?**  
BFS explores level by level and finds a minimum-edge path in an unweighted
graph. A* uses path cost plus a heuristic estimate to guide search.

**Q11. Why should an unsafe route receive a penalty?**  
Because safety constraints are more important than route length or speed.

**Q12. How does the project demonstrate a dynamic environment?**  
It changes a corridor or exit condition and runs the route search again.

## 11. Limitations and responsible use

This is an academic simulation using a small synthetic campus graph. The
performance weights, crowd penalties and example scenarios are assumptions
for teaching and testing. They are not validated for real evacuation
decisions. Real emergencies must be handled by campus authorities and
emergency services.
