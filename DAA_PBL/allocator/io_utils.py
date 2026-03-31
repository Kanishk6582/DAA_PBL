import csv
from pathlib import Path

from allocator.models import ContentItem


REQUIRED_COLUMNS = {"Series_Name", "Duration_min", "IMDb_Rating"}


def load_items_from_csv(file_path: str | Path) -> list[ContentItem]:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    with path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        if reader.fieldnames is None:
            raise ValueError("CSV file is missing headers.")

        missing = REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing:
            raise ValueError(f"CSV file is missing required columns: {sorted(missing)}")

        items: list[ContentItem] = []
        for row in reader:
            name = row["Series_Name"].strip()
            duration = int(float(row["Duration_min"]))
            rating = float(row["IMDb_Rating"])
            if duration <= 0:
                raise ValueError(f"Duration must be positive for item: {name}")
            items.append(ContentItem(name=name, duration=duration, rating=rating))

    if not items:
        raise ValueError("CSV file does not contain any content rows.")

    return items
