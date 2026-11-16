# Member 3 – Performance & Environment Types
## Emergency Response Decision Agent

This is the complete standalone project contribution for **Member 3 (Hanne)**.

## Included files

- `performance.py`: performance score and aggregate metrics.
- `experiments.py`: campus graph, transparent BFS/A* benchmark implementations, and six scenarios.
- `main.py`: runs experiments and exports measured results to CSV.
- `tests/test_member3.py`: unit tests.
- `docs/member3_report_section.md`: report-ready theory, metrics, methodology, limitations, and viva questions.

## Run

Python 3.9+ recommended. No third-party packages required.

```bash
python main.py
```

Run unit tests:

```bash
python -m unittest discover -s tests -v
```

The script prints actual route, nodes expanded, execution time, route cost and
score measured on your computer. It also creates `experiment_results.csv`.
Execution time varies by machine; do not copy sample timing values from another
computer into your report.

## Shared campus graph

A = Academic Block A; B = Academic Block B; L = Library; C = Canteen;
M = Medical Centre; P = Parking Area; G1 = Main Gate; G2 = Gate 2.

Connections:
A: B,L
B: A,C,P
L: A,C,M
C: B,L,P
M: L,P
P: B,C,M,G1,G2
G1: P
G2: P

## Experiments

1. Normal campus.
2. Fire with corridor A-B blocked.
3. Main Gate crowd penalty.
4. Security restriction at B.
5. Partial observability: crowd status at G2 is unknown.
6. Dynamic environment: P-G1 closes during the updated scenario.

BFS and A* code here is a small benchmark implementation so Member 3 can run
experiments independently. In the final integrated project, coordinate with
Member 4 and use the same BFS/A* implementation and return format to avoid
duplicate algorithm versions.

## Metrics

- Goal achievement / success rate
- Route validity
- Route cost
- Nodes expanded
- Execution time in milliseconds
- Illustrative composite score

The score weights are configurable examples for the academic simulation, not
validated emergency-safety weights. The partial-observability scenario labels
unknown information; it does not pretend to know the hidden crowd condition.
