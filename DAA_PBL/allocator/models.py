from dataclasses import dataclass


@dataclass(frozen=True)
class ContentItem:
    name: str
    duration: int
    rating: float


@dataclass
class SelectionResult:
    method: str
    selected_items: list[ContentItem]
    total_duration: int
    raw_satisfaction: float
    adjusted_satisfaction: float

    @property
    def title_list(self) -> list[str]:
        return [item.name for item in self.selected_items]
