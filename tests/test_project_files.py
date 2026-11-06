from pathlib import Path

import duckdb
import yaml

ROOT = Path(__file__).parent.parent


def load(name):
    return yaml.safe_load((ROOT / "config" / name).read_text())


def test_schema_creates_every_table():
    connection = duckdb.connect()
    connection.execute((ROOT / "db" / "schema.sql").read_text())
    tables = {row[0] for row in connection.execute("SHOW TABLES").fetchall()}
    assert tables == {
        "securities",
        "ticker_history",
        "prices",
        "corporate_actions",
        "fundamentals",
        "macro",
        "features",
    }


def test_feature_names_are_unique():
    groups = load("features.yaml").values()
    names = [feature["name"] for group in groups for feature in group]
    assert len(names) == len(set(names))


def test_test_periods_start_after_training_starts():
    for split in load("splits.yaml")["walk_forward"]:
        assert split["train_start"] < split["test_start"] < split["test_end"]
