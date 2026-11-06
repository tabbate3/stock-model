from datetime import date

import pytest

from src.sampling.windows import add_months, month_index, sample_windows

HISTORY = {
    "long_lived": (date(1950, 1, 1), date(2025, 12, 1)),
    "failed_early": (date(1995, 1, 1), date(2001, 6, 1)),
    "too_short": (date(2004, 1, 1), date(2004, 6, 1)),
}


def sample(**overrides):
    settings = dict(
        n_windows=2000,
        train_start=date(1990, 1, 1),
        test_start=date(2010, 1, 1),
        horizon_months=36,
        min_months=24,
        max_months=120,
    )
    return sample_windows(HISTORY, **(settings | overrides))


def test_inputs_and_outcomes_finish_before_test_period():
    assert all(w.outcome_end < date(2010, 1, 1) for w in sample())


def test_a_long_horizon_still_finishes_before_test_period():
    windows = sample(horizon_months=120)
    assert all(w.outcome_end < date(2010, 1, 1) for w in windows)


def test_windows_stay_inside_training_era_and_stock_history():
    for w in sample():
        first, last = HISTORY[w.security_id]
        assert w.start >= max(first, date(1990, 1, 1))
        assert w.end <= last


def test_lengths_vary_within_limits():
    lengths = [month_index(w.end) - month_index(w.start) + 1 for w in sample()]
    assert min(lengths) >= 24
    assert max(lengths) <= 120
    assert len(set(lengths)) > 10


def test_failed_stocks_are_sampled_and_short_histories_are_skipped():
    drawn = {w.security_id for w in sample()}
    assert drawn == {"long_lived", "failed_early"}


def test_same_seed_gives_same_windows():
    assert sample(seed=7) == sample(seed=7)


def test_no_eligible_stock_raises():
    with pytest.raises(ValueError):
        sample(test_start=date(1991, 1, 1))


def test_add_months_crosses_years():
    assert add_months(date(2019, 11, 1), 3) == date(2020, 2, 1)
    assert add_months(date(2020, 1, 1), -1) == date(2019, 12, 1)
