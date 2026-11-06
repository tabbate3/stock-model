"""Draw random stock windows without leaking the future into training."""

from dataclasses import dataclass
from datetime import date

import numpy as np


@dataclass(frozen=True)
class Window:
    security_id: str
    start: date  # First month of inputs.
    end: date  # Last month of inputs; the prediction is made here.
    outcome_end: date  # Last month of the return being predicted.


def month_index(month: date) -> int:
    return month.year * 12 + month.month - 1


def add_months(month: date, months: int) -> date:
    """Move a first-of-month date by a number of months."""
    index = month_index(month) + months
    return date(index // 12, index % 12 + 1, 1)


def sample_windows(
    months_by_security: dict[str, tuple[date, date]],
    n_windows: int,
    train_start: date,
    test_start: date,
    horizon_months: int,
    min_months: int,
    max_months: int,
    seed: int = 0,
) -> list[Window]:
    """Sample windows whose inputs and outcome all finish before test_start.

    months_by_security maps each stock to its first and last months of data.
    The stock is drawn first and evenly, so long-lived companies don't dominate.
    """
    if min_months > max_months:
        raise ValueError("min_months must not exceed max_months")

    rng = np.random.default_rng(seed)
    # outcome_end must stay before test_start, which limits the latest prediction month.
    last_allowed = add_months(test_start, -horizon_months - 1)

    eligible = []
    for security_id, (first, last) in sorted(months_by_security.items()):
        earliest = max(first, train_start)
        latest = min(last, last_allowed)
        if month_index(latest) - month_index(earliest) + 1 >= min_months:
            eligible.append((security_id, earliest, latest))

    if not eligible:
        raise ValueError("No stock has enough history before test_start")

    windows = []
    for _ in range(n_windows):
        security_id, earliest, latest = eligible[rng.integers(len(eligible))]
        available = month_index(latest) - month_index(earliest) + 1
        length = int(rng.integers(min_months, min(max_months, available) + 1))
        offset = int(rng.integers(0, available - length + 1))
        start = add_months(earliest, offset)
        end = add_months(start, length - 1)
        windows.append(Window(security_id, start, end, add_months(end, horizon_months)))
    return windows
