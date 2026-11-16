"""Integrated Emergency Response Agent: run experiments and save CSV results."""

import csv

from performance.experiments import run_experiments, print_results
from performance.performance import summarize_runs


def main():

    # Run all emergency scenarios using BFS and A*.
    rows, grouped = run_experiments()

    # Display experiment results.
    print_results(rows)

    # Display overall performance summary.
    summary = summarize_runs(rows)

    print("\nOVERALL PERFORMANCE SUMMARY")
    print("-" * 40)

    for key, value in summary.items():
        print(f"{key}: {value}")

    # Save results in the integration folder.
    output_file = "performance/experiment_results.csv"

    fieldnames = [
        "experiment",
        "algorithm",
        "route",
        "goal_reached",
        "route_valid",
        "unsafe_route",
        "route_cost",
        "execution_time_ms",
        "nodes_expanded",
        "score",
        "unknown_crowd_information",
        "uncertainty_note"
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:

            cleaned = dict(row)

            cleaned["route"] = (
                " -> ".join(row["route"])
                if row["route"]
                else ""
            )

            cleaned["unknown_crowd_information"] = ";".join(
                row["unknown_crowd_information"]
            )

            writer.writerow({
                key: cleaned.get(key, "")
                for key in fieldnames
            })

    print(f"\nSaved integrated experiment results to {output_file}")

    print("\nNote: Results are based on simulated campus data.")


if __name__ == "__main__":
    main()