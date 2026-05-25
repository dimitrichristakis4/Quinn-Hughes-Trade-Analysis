---
aliases:
  - "Quinn Hughes Article — Multi-Season PCA Development Code"
  - "Quinn Hughes Multi Season Pca Code"
  - "quinn-hughes-multi-season-pca-code"
title: Quinn Hughes Article — Multi-Season PCA Development Code
tags: [Quinn-Hughes, PCA, Python, hockey, analytics, development-history]
project: Quinn Hughes Trade Analysis
status: complete
created: 2026-04-22
updated: 2026-04-22
---

## What this is

Development code for the multi-season PCA analysis of Quinn Hughes, created while drafting the QSAN article. Covers season configuration, data loading, metric normalization, ranking logic, and bar chart visualization. Extends the single-season approach in `quinn-hughes-article-summary.md`.

Source: `_Hockey Analytics Article Ideas .txt`

---

## Season Configuration

```python
SEASON_CONFIG = [
    {
        'season': 2025, 
        'file_name': '24-25.csv',
        'final_four': [
            "Florida Panthers", "Edmonton Oilers", 
            "Dallas Stars", "Carolina Hurricanes"
        ]
    },
    # Additional seasons structured identically
]

LOWER_IS_BETTER_METRICS = [
    'L', 'OTL', 'CA', 'FA', 'SA', 'GA', 'xGA',
    # Other defensive/negative metrics
]
```

---

## Core Pipeline

```python
# Multi-season data loading + normalization to rate metrics
def load_season(config):
    df = pd.read_csv(config['file_name'])
    # Normalize counting stats to per-game or per-60 rates
    # Tag final_four teams for visualization highlighting
    df['In_Final_Four'] = df['Team'].isin(config['final_four'])
    return df

# Ranking function — handles "lower is better" inversion
def rank_teams(df, metrics, lower_is_better):
    for col in metrics:
        if col in lower_is_better:
            df[f'{col}_rank'] = df[col].rank(ascending=True)  # lower = better rank
        else:
            df[f'{col}_rank'] = df[col].rank(ascending=False)
    return df

# Team_ID column: stable identifier across season joins
df['Team_ID'] = df['Team'].str.strip().str.upper()

# Top-10 filtering for visualization
top10 = df.nlargest(10, 'PCA_Component_1')
```

---

## Visualization

```python
# Bar chart generation for Quinn Hughes article
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(
    top10['Team'], 
    top10['PCA_Component_1'],
    color=top10['In_Final_Four'].map({True: '#1f77b4', False: '#aec7e8'})
)
ax.set_xlabel('PCA Component 1 (Offensive Load)')
ax.set_title('Top 10 Teams — Offensive Possession Quality (2024-25)')
plt.tight_layout()
plt.savefig('top10_offensive.png', dpi=150)
```

---

## Notes

- PCA approach mirrors the single-season analysis in `quinn-hughes-article-summary.md` but extends across multiple seasons to show Quinn's development arc
- `Team_ID` column added to handle team name inconsistencies across CSV files from different seasons
- `lower_is_better` inversion ensures defensive metrics don't penalize good teams in the PCA component loading
- Final Four highlighting shows whether the analysis correctly identifies elite teams

See: [[quinn-hughes-article-summary]] for the completed article and single-season findings.


---
## Wiki page
[[quinn-hughes-trade-analysis|Quinn Hughes Trade Analysis]]
