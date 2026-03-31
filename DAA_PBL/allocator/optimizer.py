from dataclasses import dataclass

from allocator.models import ContentItem, SelectionResult


@dataclass(frozen=True)
class FatigueConfig:
    threshold_minutes: int = 180
    penalty_factor: float = 0.85


def adjusted_rating_for_append(
    current_minutes: int,
    item: ContentItem,
    fatigue: FatigueConfig,
) -> float:
    threshold = fatigue.threshold_minutes
    penalty = fatigue.penalty_factor

    if current_minutes >= threshold:
        return item.rating * penalty

    minutes_before_penalty = max(0, threshold - current_minutes)
    unpenalized_minutes = min(item.duration, minutes_before_penalty)
    penalized_minutes = item.duration - unpenalized_minutes
    multiplier = (unpenalized_minutes + penalized_minutes * penalty) / item.duration
    return item.rating * multiplier


def compute_adjusted_satisfaction(
    items: list[ContentItem],
    fatigue: FatigueConfig,
) -> float:
    total = 0.0
    elapsed = 0
    for item in items:
        total += adjusted_rating_for_append(elapsed, item, fatigue)
        elapsed += item.duration
    return round(total, 4)


def compute_raw_satisfaction(items: list[ContentItem]) -> float:
    return round(sum(item.rating for item in items), 4)


def _build_result(
    method: str,
    selected_items: list[ContentItem],
    fatigue: FatigueConfig,
) -> SelectionResult:
    total_duration = sum(item.duration for item in selected_items)
    return SelectionResult(
        method=method,
        selected_items=selected_items,
        total_duration=total_duration,
        raw_satisfaction=compute_raw_satisfaction(selected_items),
        adjusted_satisfaction=compute_adjusted_satisfaction(selected_items, fatigue),
    )


def dynamic_programming_selection(
    items: list[ContentItem],
    time_budget: int,
    fatigue: FatigueConfig | None = None,
) -> SelectionResult:
    if time_budget < 0:
        raise ValueError("Time budget must be non-negative.")

    fatigue = fatigue or FatigueConfig()
    dp = [0.0] * (time_budget + 1)
    chosen: list[list[ContentItem]] = [[] for _ in range(time_budget + 1)]

    for item in items:
        for minutes in range(time_budget, item.duration - 1, -1):
            previous_selection = chosen[minutes - item.duration]
            current_time = sum(selected.duration for selected in previous_selection)
            candidate_value = dp[minutes - item.duration] + adjusted_rating_for_append(
                current_time, item, fatigue
            )
            if candidate_value > dp[minutes]:
                dp[minutes] = candidate_value
                chosen[minutes] = previous_selection + [item]

    best_time = max(range(time_budget + 1), key=dp.__getitem__)
    return _build_result("Dynamic Programming", chosen[best_time], fatigue)


def greedy_selection(
    items: list[ContentItem],
    time_budget: int,
    fatigue: FatigueConfig | None = None,
) -> SelectionResult:
    if time_budget < 0:
        raise ValueError("Time budget must be non-negative.")

    fatigue = fatigue or FatigueConfig()
    ranked_items = sorted(items, key=lambda item: item.rating / item.duration, reverse=True)

    selected_items: list[ContentItem] = []
    total_duration = 0
    for item in ranked_items:
        if total_duration + item.duration <= time_budget:
            selected_items.append(item)
            total_duration += item.duration

    return _build_result("Greedy", selected_items, fatigue)


def benchmark_across_budgets(
    items: list[ContentItem],
    start: int,
    stop: int,
    step: int,
    fatigue: FatigueConfig | None = None,
) -> list[dict[str, float]]:
    if step <= 0:
        raise ValueError("Step must be positive.")
    if start > stop:
        raise ValueError("Start budget must be less than or equal to stop budget.")

    fatigue = fatigue or FatigueConfig()
    rows: list[dict[str, float]] = []
    for budget in range(start, stop + 1, step):
        dp_result = dynamic_programming_selection(items, budget, fatigue)
        greedy_result = greedy_selection(items, budget, fatigue)
        rows.append(
            {
                "budget": budget,
                "dp": dp_result.adjusted_satisfaction,
                "greedy": greedy_result.adjusted_satisfaction,
            }
        )
    return rows
