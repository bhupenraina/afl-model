# AFL Match Prediction Model

Predicting AFL match margins using gradient boosted decision trees (XGBoost), trained on advanced player and team statistics from the Fryzigg dataset (2019–2025).

> **Status**: v1 model built using rolling team form data. Team ELO ratings and other features yet to be added.

## Approach

The model predicts the home team's margin of victory where a positive value means a home win, negative means an away win. This is a regression problem where rather than classifying win/loss, predicting the margin captures both the match result and size of victory.

### Data Pipeline

1. **Collection** — Player-level match stats pulled from Fryzigg via the `fitzRoy` R package (~65,000 rows across 2019–2025)
2. **Processing** — Player stats aggregated to team level per match, then structured into home/away format with one row per match
3. **Feature Engineering** — Rolling 5-game averages for 46 team statistics (contested possessions, clearances, inside 50s, pressure acts, metres gained, etc.), lagged by one game to prevent data leakage.

### Model

- **Algorithm**: XGBoost Regressor (`n_estimators=100`, `max_depth=4`, `learning_rate=0.1`)
- **Target variable**: Home team margin (home score − away score)
- **Features**: 92 rolling average stats (46 home + 46 away)

### Validation

Walk-forward (expanding window) validation — the model only ever predicts forward in time, mirroring real-world usage. Standard k-fold cross-validation is inappropriate here because it would allow the model to train on future data.

| Year | MAE | RMSE | Tip Accuracy |
|------|-----|------|-------------|
| 2021 | 30.89 | 38.41 | 53.1% |
| 2022 | 28.84 | 35.96 | 59.4% |
| 2023 | 30.47 | 38.92 | 58.3% |
| 2024 | 30.38 | 38.06 | 59.3% |
| **2025 (holdout)** | **29.36** | **37.23** | **66.7%** |

## Project Structure
```
afl-model/
├── R/
│   └── data_pull.R              # Fryzigg data collection via fitzRoy
├── src/
│   ├── processing/
│   │   └── clean.py             # Aggregate player stats to team/match level
│   ├── features/
│   │   └── form.py              # Rolling 5-game averages with leakage prevention
│   └── model/
│       └── train.py             # XGBoost training with walk-forward validation
├── data/
│   ├── raw/                     # Raw Fryzigg CSVs (gitignored)
│   └── cleaned/                 # Processed datasets (gitignored)
└── README.md
```
## Roadmap

- [ ] ELO rating system as an additional feature
- [ ] Rest days between matches
- [ ] Hyperparameter tuning
- [ ] Win probability calibration (sigmoid on predicted margin)
- [ ] Web dashboard with live round predictions
- [ ] Benchmark against bookmaker line

## Setup

```bash
# Pull data (requires R and fitzRoy)
Rscript R/data_pull.R

# Install Python dependencies
pip install pandas numpy xgboost scikit-learn

# Run pipeline
python src/processing/clean.py
python src/features/form.py
python src/model/train.py
```