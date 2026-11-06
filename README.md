# stock-model
Seeing if I can make a stock prediction model testings various AI models such as neural networks and random forest based on different indicators. It will be trained on data only from US stocks right now to keep it small at the start.

The model succeeds only if it beats simple baselines and a low-cost index fund,
after costs, on periods it never saw. This is a research tool, not financial advice.

## Setup

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python -m pytest
```

On macOS or Linux, use `.venv/bin/python` instead.

## Data flow

1. **Download:** `src/ingest` saves untouched vendor data to `data/raw`.
2. **Clean:** `src/clean` assigns permanent IDs and records delistings.
3. **Calculate:** `src/features` builds indicators using only data public at that date.
4. **Sample:** `src/sampling` draws random windows from training eras only.
5. **Train:** `src/models` fits the baselines, then the neural network.
6. **Test:** `src/evaluate` predicts unseen eras and compares results.

## Status

| Phase | Work | Status |
|---|---|---|
| 1 | Data test with EODHD or Massive | Not started |
| 2 | Database with 100-500 stocks | Schema written |
| 3 | Indicators | Starter list written |
| 4 | Baselines | Not started |
| 5 | Neural network | Not started |
| 6 | Validation across eras | Not started |
| 7 | Older data and social signals | Not started |

Working so far: the window sampler and the data-quality checks.
The check that the model can't guess the year from its inputs comes in Phase 4.
