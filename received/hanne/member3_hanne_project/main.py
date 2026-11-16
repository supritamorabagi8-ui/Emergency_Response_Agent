"""Member 3 demonstration: run experiments and save measured CSV results."""
import csv
from experiments import run_experiments, print_results


def main():
    rows, _ = run_experiments()
    print_results(rows)

    output_file = "experiment_results.csv"
    fieldnames = [
        "experiment", "algorithm", "route", "goal_reached", "route_valid",
        "unsafe_route", "route_cost", "execution_time_ms", "nodes_expanded",
        "score", "unknown_crowd_information", "uncertainty_note"
    ]
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            cleaned = dict(row)
            cleaned["route"] = " -> ".join(row["route"]) if row["route"] else ""
            cleaned["unknown_crowd_information"] = ";".join(row["unknown_crowd_information"])
            writer.writerow({key: cleaned.get(key, "") for key in fieldnames})

    print(f"\nSaved measured results to {output_file}")


if __name__ == "__main__":
    main()
