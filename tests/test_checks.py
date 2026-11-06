import pandas as pd

from src.clean.checks import (
    find_lookahead,
    find_missing_delistings,
    find_split_artifacts,
)


def dates(*values):
    return pd.to_datetime(list(values))


def test_lookahead_flags_figures_used_before_publication():
    features = pd.DataFrame(
        {
            "security_id": ["safe", "leaky"],
            "month": dates("2020-03-01", "2020-03-01"),
            "published_date": dates("2020-02-10", "2020-03-15"),
        }
    )
    assert find_lookahead(features)["security_id"].tolist() == ["leaky"]


def test_missing_delisting_return_is_flagged():
    securities = pd.DataFrame(
        {
            "security_id": ["complete", "missing", "active"],
            "delisted_date": dates("2008-09-15", "2001-12-02", None),
        }
    )
    prices = pd.DataFrame(
        {
            "security_id": ["complete", "missing", "active"],
            "date": dates("2008-09-01", "2001-10-01", "2025-12-01"),
            "total_return": [-0.9, 0.1, 0.02],
        }
    )
    result = find_missing_delistings(securities, prices)
    assert result["security_id"].tolist() == ["missing"]


def test_delisted_stock_with_no_prices_is_flagged():
    securities = pd.DataFrame(
        {"security_id": ["empty"], "delisted_date": dates("2001-12-02")}
    )
    prices = pd.DataFrame(
        {
            "security_id": pd.Series(dtype=str),
            "date": pd.Series(dtype="datetime64[ns]"),
            "total_return": pd.Series(dtype=float),
        }
    )
    assert len(find_missing_delistings(securities, prices)) == 1


def test_split_artifact_is_flagged_but_adjusted_return_is_not():
    prices = pd.DataFrame(
        {
            "security_id": ["unadjusted", "adjusted"],
            "date": dates("2020-08-01", "2020-08-01"),
            "total_return": [-0.51, 0.03],
        }
    )
    actions = pd.DataFrame(
        {
            "security_id": ["unadjusted", "adjusted"],
            "date": dates("2020-08-01", "2020-08-01"),
            "action_type": ["split", "split"],
            "value": [2.0, 2.0],
        }
    )
    result = find_split_artifacts(prices, actions)
    assert result["security_id"].tolist() == ["unadjusted"]
