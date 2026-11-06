# Decisions

## Made

| Decision | Why |
|---|---|
| Start with US stocks | Best data and a practical scope |
| Use one row per stock per month | Easy to sample, and monthly data reaches furthest back |
| Predict return relative to the market | Reduces the model's ability to profit from recognizing an era |
| Train on random stocks, dates and lengths | Gives more variety, and suits variable-length sequence models |
| Split by time before sampling | Random splits would leak the future into training |
| Keep delisted stocks with final returns | Otherwise the model learns that companies never fail |
| Feed returns and ratios, not raw prices | Raw prices aren't comparable across stocks or eras |
| Build baselines before the neural network | Complexity has to earn its place |
| Keep social attention as a later add-on | The data only covers the 2010s onward |

## Open

| Decision | How it gets settled |
|---|---|
| Data vendor | Phase 1 sample test |
| Budget | Decides how far back the data can go |
| Main time horizon | Proposed: prioritize 2-5 years, with 10 years as secondary |
