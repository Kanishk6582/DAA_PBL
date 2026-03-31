import argparse
from pathlib import Path

from allocator.io_utils import load_items_from_csv
from allocator.optimizer import (
    FatigueConfig,
    benchmark_across_budgets,
    dynamic_programming_selection,
    greedy_selection,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Optimal Resource-Time Allocator using DP and Greedy."
    )
    parser.add_argument(
        "--file",
        default="data/sample_content.csv",
        help="Path to the input CSV file.",
    )
    parser.add_argument(
        "--time",
        type=int,
        default=240,
        help="Available watch time in minutes.",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=180,
        help="Fatigue threshold in minutes.",
    )
    parser.add_argument(
        "--penalty",
        type=float,
        default=0.85,
        help="Penalty multiplier after the fatigue threshold.",
    )
    parser.add_argument(
        "--plot",
        action="store_true",
        help="Generate a satisfaction comparison plot.",
    )
    return parser


def print_result(label: str, result) -> None:
    print(f"\n{label}")
    print("-" * len(label))
    print(f"Method: {result.method}")
    print(f"Selected items: {', '.join(result.title_list) if result.title_list else 'None'}")
    print(f"Total duration: {result.total_duration} minutes")
    print(f"Raw satisfaction: {result.raw_satisfaction:.2f}")
    print(f"Adjusted satisfaction: {result.adjusted_satisfaction:.2f}")


def main() -> None:
    args = build_parser().parse_args()

    items = load_items_from_csv(args.file)
    fatigue = FatigueConfig(
        threshold_minutes=args.threshold,
        penalty_factor=args.penalty,
    )

    dp_result = dynamic_programming_selection(items, args.time, fatigue)
    greedy_result = greedy_selection(items, args.time, fatigue)

    print_result("Dynamic Programming Result", dp_result)
    print_result("Greedy Result", greedy_result)

    if args.plot:
        from allocator.visualization import save_comparison_plot

        rows = benchmark_across_budgets(
            items=items,
            start=max(30, min(item.duration for item in items)),
            stop=args.time,
            step=max(15, args.time // 8),
            fatigue=fatigue,
        )
        output_path = save_comparison_plot(
            rows,
            Path("outputs") / "comparison_plot.png",
        )
        print(f"\nPlot saved to: {output_path}")


if __name__ == "__main__":
    main()
