# Optimal Resource-Time Allocator

This project implements a decision-support system for selecting the best set of movies or series episodes within a fixed time budget.

The current repository is positioned as a CLI-focused milestone:

- backend optimization logic is implemented
- command-line workflow is ready for analysis and demos
- advanced reporting and deeper analysis can be added in the next phase

It follows the DAA synopsis by comparing:

- Dynamic Programming using the 0/1 Knapsack approach
- A Greedy baseline using rating-to-duration ratio
- A fatigue penalty that reduces satisfaction after 180 minutes

## Project Structure

- `main.py` - CLI entry point
- `allocator/models.py` - data models
- `allocator/io_utils.py` - CSV loading helpers
- `allocator/optimizer.py` - DP and Greedy algorithms
- `allocator/visualization.py` - Matplotlib plots
- `data/sample_content.csv` - sample dataset
- `tests/test_optimizer.py` - unit tests

## Assumptions

- Content is atomic: a movie or episode is either fully selected or skipped
- Rating is used as the satisfaction score
- Time budget is provided in minutes
- Fatigue starts after 180 minutes
- The fatigue-aware scoring assumes content is watched in the same order it is selected by the algorithm

## Setup

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
python main.py --file data/sample_content.csv --time 240 --plot
```

## Input Format

CSV columns:

```text
Series_Name,Duration_min,IMDb_Rating
```

## Example Output

The program prints:

- selected titles for Dynamic Programming
- selected titles for Greedy
- total time used
- raw and fatigue-adjusted satisfaction

If `--plot` is enabled, it also saves a comparison chart in the `outputs/` directory.
