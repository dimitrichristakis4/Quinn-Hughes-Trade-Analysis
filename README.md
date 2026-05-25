# Quinn Hughes Trade Analysis: PCA Model

> [December 2025] Two-stage PCA model asking whether Quinn Hughes makes Minnesota a Stanley Cup contender. Benchmarks the Wild against previous Conference Finals teams, then ranks Hughes against elite NHL defensemen across possession, offense, and defense.

**By Dimitri Christakis**

*Analysis written and completed in December 2025 following the Quinn Hughes trade to the Minnesota Wild. Posted to GitHub in May 2026.*

**The question:** Does acquiring Quinn Hughes turn the Minnesota Wild into a legitimate Stanley Cup contender?

To answer it, this project uses PCA to build composite scores for every Conference Finals team from 2022 to 2025, maps exactly where Minnesota sits relative to those contenders, then runs the same model on individual defensemen to evaluate whether Hughes fills the gaps.

Full article: *"Analytical Review: Can Quinn Hughes Elevate the Minnesota Wild to Contender Status?"*

---

## Methodology

The analysis runs in two stages.

**Stage 1: Team-level PCA (`team_contender_pca_analysis.py`)**

NHL team data from the 2022 to 2025 Conference Finals seasons is reduced into four composite scores using PCA. Minnesota Wild 2025-26 is included as the focus team and projected to 82-game pace for comparison. PCA is computed across the full database so scores are standardized relative to the entire league.

| Composite Score | Features used |
|----------------|--------------|
| Possession | `LDGF%, CF, CF%, SCF%, SCSF%, SCF, LDCF, LDCF%, LDSF, SF, FF%` |
| Offensive Quality | `HDCF%, xGF%, HDCF, SCGF%, HDGF%, MDCF%, xGF, GF%, HDGF` |
| Defensive Quality | `HDCA, LDGA, SA, SCA, xGA, HDSA, GA, MDSA, MDCA, SCGA` |
| Goaltending / Luck | `LDSSV%, PDO, SV%` |

The Florida Panthers (2024, 2025) serve as the gold standard. They rated elite across all four dimensions and won back-to-back Cups.

**Stage 2: Defensemen PCA (`defensemen_pca_scatter.py`)**

The same PCA approach applied to individual defensemen using both raw and relative stats merged together. Balancing the two removes team context from the equation. A great player on a weak team like Hughes on Vancouver is not penalized, and an elite player on a powerhouse team is not artificially inflated.

Three composite scores are built (no Goaltending dimension for individual players):

| Composite Score | Features used (raw + relative for each) |
|----------------|----------------------------------------|
| Possession | `CF, CF%, FF%, SF, SF%, SCF, SCF%, LDCF, LDCF%` |
| Offensive Quality | `xGF, xGF%, HDCF, HDCF%, HDGF, HDGF%, MDCF%, GF%` |
| Defensive Quality | `xGA, HDCA, SCA, SA, GA, MDCA, HDSA` |

---

## Key Findings

- Minnesota pre-trade had elite goaltending (Wallstedt .937 SV%, Gustavsson .912 SV%) but was below average in possession and offensive quality
- Hughes ranks elite in Possession and Offensive Quality among all defensemen in the comparison pool
- His defensive score is just above average, which is exactly what Minnesota needs since their goaltending covers the rest
- **The formula: Elite Offense + Average Defense + Elite Goaltending = Stanley Cup Winning Potential**
- Post-trade, Minnesota and Colorado rate 1a/1b in the Western Conference

---

## Outputs

**Section 1: Minnesota vs. historical contenders**

![Historical Team Comparison](outputs/team_comparison_historical.png)

Minnesota sits well below average in possession and offensive quality. Elite goaltending is their only dimension that matches contender-level teams.

---

**Section 2: Minnesota vs. current rivals (82-game pace)**

![Rivals Comparison](outputs/team_comparison_rivals_82game.png)

Carolina, Washington, and Colorado are operating at a much higher statistical level. Without a major move, Minnesota was a bubble team, good enough to make the playoffs but not good enough to survive a seven-game series against the top seeds.

---

**Section 3: Defensemen PCA comparison**

![Defensemen PCA](outputs/defensemen_pca_comparison.png)

Hughes stands out in both Possession and Offensive Quality. Evan Bouchard rates highly in Possession due to his possession-as-defense effect. Zeev Buium, the player Hughes directly replaces, is still developing. The gap between them is not marginal.

---

## Data Sources

- Team stats: [Natural Stat Trick](https://www.naturalstattrick.com/) — 2022 to 2025 Conference Finals teams, with Minnesota Wild 2025-26 projected to 82-game pace
- Defenseman stats: [Natural Stat Trick](https://www.naturalstattrick.com/) — raw and relative (on-ice vs off-ice splits)

---

## Files

```
├── team_contender_pca_analysis.py   # Stage 1: team PCA (adjust COMPARISON_TEAMS for historical vs rivals view)
├── defensemen_pca_scatter.py        # Stage 2: defensemen PCA scatter
├── outputs/
│   ├── team_comparison_historical.png
│   ├── team_comparison_rivals_82game.png
│   └── defensemen_pca_comparison.png
```

## Dependencies

```
pip install pandas numpy matplotlib adjustText
```
