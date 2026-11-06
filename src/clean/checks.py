"""Data-quality checks. Each returns the offending rows; empty means it passed."""

import pandas as pd


def find_lookahead(features: pd.DataFrame) -> pd.DataFrame:
    """Rows using a figure before it was public (needs month, published_date)."""
    return features[features["published_date"] > features["month"]]


def find_missing_delistings(
    securities: pd.DataFrame, prices: pd.DataFrame
) -> pd.DataFrame:
    """Delisted stocks with no return recorded in their final month."""
    delisted = securities[securities["delisted_date"].notna()]
    with_returns = prices[prices["total_return"].notna()]
    last_return = with_returns.groupby("security_id")["date"].max().rename("last_return")
    merged = delisted.merge(last_return, on="security_id", how="left")
    has_final = merged["last_return"].dt.to_period("M") >= merged[
        "delisted_date"
    ].dt.to_period("M")
    return merged[~has_final]


def find_split_artifacts(
    prices: pd.DataFrame, actions: pd.DataFrame, tolerance: float = 0.1
) -> pd.DataFrame:
    """Months where a return looks like an unadjusted split.

    A 2-for-1 split on an unadjusted series shows a return near -50%.
    """
    splits = actions[actions["action_type"] == "split"]
    merged = prices.merge(splits, on=["security_id", "date"])
    raw_move = 1 / merged["value"] - 1
    return merged[(merged["total_return"] - raw_move).abs() <= tolerance]
