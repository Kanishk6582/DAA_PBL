import unittest

from allocator.models import ContentItem
from allocator.optimizer import (
    FatigueConfig,
    compute_adjusted_satisfaction,
    dynamic_programming_selection,
    greedy_selection,
)


class OptimizerTests(unittest.TestCase):
    def test_dynamic_programming_finds_optimal_combination_without_fatigue(self) -> None:
        items = [
            ContentItem("A", 10, 60),
            ContentItem("B", 20, 100),
            ContentItem("C", 30, 120),
        ]
        fatigue = FatigueConfig(threshold_minutes=1000, penalty_factor=1.0)

        result = dynamic_programming_selection(items, 50, fatigue)

        self.assertEqual(result.total_duration, 50)
        self.assertEqual(result.raw_satisfaction, 220)
        self.assertEqual(result.title_list, ["B", "C"])

    def test_greedy_can_miss_the_optimal_solution(self) -> None:
        items = [
            ContentItem("A", 10, 60),
            ContentItem("B", 20, 100),
            ContentItem("C", 30, 120),
        ]
        fatigue = FatigueConfig(threshold_minutes=1000, penalty_factor=1.0)

        greedy = greedy_selection(items, 50, fatigue)
        dp = dynamic_programming_selection(items, 50, fatigue)

        self.assertEqual(greedy.raw_satisfaction, 160)
        self.assertEqual(dp.raw_satisfaction, 220)

    def test_fatigue_penalty_reduces_total_satisfaction_after_threshold(self) -> None:
        items = [
            ContentItem("Episode 1", 100, 9.0),
            ContentItem("Episode 2", 100, 9.0),
        ]
        fatigue = FatigueConfig(threshold_minutes=180, penalty_factor=0.5)

        adjusted = compute_adjusted_satisfaction(items, fatigue)

        self.assertEqual(adjusted, 17.1)


if __name__ == "__main__":
    unittest.main()
