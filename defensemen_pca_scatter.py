# defensemen_pca_scatter.py
# Quinn Hughes Trade Analysis - Dimitri Christakis, December 2025
#
# Applies PCA to NHL defenseman data using both raw and relative stats.
# Builds three composite scores: Possession, Offensive Quality, Defensive Quality.
# Merging raw and relative removes team context - a great player on a weak team
# like Hughes on Vancouver is not penalized for it.
# Needs: Final_Super_Database.csv (raw) and Final_Super_Database_Cleaned.csv (relative)
# Output: defensemen_pca_comparison.png

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

try:
    from adjustText import adjust_text
except ImportError:
    def adjust_text(*args, **kwargs):
        pass


# --- config ---

# primary subject, shown as a large red star
HIGHLIGHT_MAIN = ["Quinn Hughes"]

# secondary reference players, shown as orange stars
HIGHLIGHT_SECONDARY = ["Evan Bouchard", "Kirill Kaprizov", "Zeev Buium"]

# full comparison pool
COMPARISON_PLAYERS = [
    "Cale Makar", "Josh Morrissey", "Adam Fox", "Roman Josi",
    "Rasmus Dahlin", "Lane Hutson", "Zach Werenski",
    "Evan Bouchard", "Miro Heiskanen", "Jakob Chychrun",
    "Charlie McAvoy", "Jaccob Slavin", "Victor Hedman",
    "Erik Karlsson", "Devon Toews", "Zeev Buium",
    "Nick Seeler", "Chris Tanev", "Gustav Forsling",
    "Jonas Brodin", "Brock Faber", "Kirill Kaprizov",
]

# raw and relative stats both included so each feature pair captures
# volume (raw) and on/off-ice impact (relative)
PCA_FEATURES = {
    "Possession Score": [
        "CF_raw", "CF_rel", "CF%_raw", "CF%_rel", "FF%_raw", "FF%_rel",
        "SF_raw", "SF_rel", "SF%_raw", "SF%_rel", "SCF_raw", "SCF_rel",
        "SCF%_raw", "SCF%_rel", "LDCF_raw", "LDCF_rel", "LDCF%_raw", "LDCF%_rel",
    ],
    "Offensive Quality Score": [
        "xGF_raw", "xGF_rel", "xGF%_raw", "xGF%_rel", "HDCF_raw", "HDCF_rel",
        "HDCF%_raw", "HDCF%_rel", "HDGF_raw", "HDGF_rel", "HDGF%_raw", "HDGF%_rel",
        "MDCF%_raw", "MDCF%_rel", "GF%_raw", "GF%_rel",
    ],
    "Defensive Quality Score": [
        "xGA_raw", "xGA_rel", "HDCA_raw", "HDCA_rel", "SCA_raw", "SCA_rel",
        "SA_raw", "SA_rel", "GA_raw", "GA_rel", "MDCA_raw", "MDCA_rel",
        "HDSA_raw", "HDSA_rel",
    ],
}


# load and merge the two data files
try:
    df_raw = pd.read_csv("Final_Super_Database.csv")
    df_rel = pd.read_csv("Final_Super_Database_Cleaned.csv")
except FileNotFoundError as e:
    raise FileNotFoundError(
        f"{e}. Download defenseman stats from Natural Stat Trick. "
        "One file for raw counts, one for relative (on-ice vs off-ice)."
    )

# drop relative rows with extreme values - those are tiny sample sizes
if "CF" in df_rel.columns:
    valid_mask = df_rel["CF"].notna() & (abs(df_rel["CF"]) <= 25.0)
    df_rel = df_rel[valid_mask].copy()

df = pd.merge(df_raw, df_rel, on="Player", suffixes=("_raw", "_rel"))
print(f"Merged data: {len(df)} players.")


# run PCA for each feature group
# standardize, take first eigenvector, flip sign so higher always = better
# defensive score is anchored to xGA specifically since lower allowed = better
for score_name, feature_list in PCA_FEATURES.items():
    valid_features = [f for f in feature_list if f in df.columns]
    if not valid_features:
        print(f"Warning: no valid features for {score_name}, skipping.")
        continue

    data_subset = df[valid_features].fillna(df[valid_features].mean())
    std_data = (data_subset - data_subset.mean()) / data_subset.std(ddof=1)

    cov_matrix = np.cov(std_data.fillna(0).T)
    eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)

    sorted_indices = np.argsort(eigenvalues)[::-1]
    first_eigenvector = eigenvectors[:, sorted_indices][:, 0]
    pca_scores = std_data.dot(first_eigenvector)

    correlation = np.corrcoef(pca_scores, std_data.mean(axis=1))[0, 1]
    if score_name == "Defensive Quality Score":
        if "xGA_raw" in std_data.columns:
            target_corr = np.corrcoef(pca_scores, std_data["xGA_raw"])[0, 1]
            if target_corr > 0:
                pca_scores = -pca_scores
        elif correlation > 0:
            pca_scores = -pca_scores
    else:
        if correlation < 0:
            pca_scores = -pca_scores

    df[score_name] = pca_scores

print("PCA scores calculated.")


# filter to comparison pool and split into three layers for scatter styling
players_rest = [p for p in COMPARISON_PLAYERS
                if p not in HIGHLIGHT_MAIN and p not in HIGHLIGHT_SECONDARY]

all_players = HIGHLIGHT_MAIN + HIGHLIGHT_SECONDARY + players_rest
df_filtered = df[df["Player"].isin(all_players)].copy()

score_cols = list(PCA_FEATURES.keys())
plot_df = df_filtered.melt(
    id_vars=["Player"],
    value_vars=score_cols,
    var_name="PCA Category",
    value_name="Score",
)

x_mapping = {name: i for i, name in enumerate(score_cols)}
plot_df["X_coord"] = plot_df["PCA Category"].map(x_mapping)

data_main = plot_df[plot_df["Player"].isin(HIGHLIGHT_MAIN)]
data_sec  = plot_df[plot_df["Player"].isin(HIGHLIGHT_SECONDARY)]
data_rest = plot_df[plot_df["Player"].isin(players_rest)]


# plot - three layers so hughes sits on top
plt.figure(figsize=(16, 9))

plt.scatter(data_rest["X_coord"], data_rest["Score"],
            s=120, c="blue", alpha=0.5, label="Comparison")

plt.scatter(data_sec["X_coord"], data_sec["Score"],
            s=350, c="orange", marker="*", edgecolors="black",
            alpha=1.0, label="Reference Players")

plt.scatter(data_main["X_coord"], data_main["Score"],
            s=900, c="red", marker="*", edgecolors="black",
            alpha=1.0, label="Quinn Hughes")

# arrow annotations pointing to hughes on each dimension
for _, row in data_main.iterrows():
    x_offset = -0.8 if row["PCA Category"] == "Defensive Quality Score" else 0.3
    y_offset = 0.5
    plt.annotate(
        "Quinn Hughes",
        xy=(row["X_coord"], row["Score"]),
        xytext=(row["X_coord"] + x_offset, row["Score"] + y_offset),
        arrowprops=dict(facecolor="black", shrink=0.05, width=2, headwidth=10),
        fontsize=14, weight="bold", color="darkred",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", alpha=0.8),
    )

# labels for comparison and secondary players
texts = []
for _, row in data_rest.iterrows():
    texts.append(plt.text(row["X_coord"], row["Score"], row["Player"],
                          fontsize=9, alpha=0.8))
for _, row in data_sec.iterrows():
    texts.append(plt.text(row["X_coord"], row["Score"], row["Player"],
                          fontsize=11, weight="bold", color="chocolate"))

try:
    adjust_text(texts,
                arrowprops=dict(arrowstyle="-", color="gray",
                                lw=0.5, shrinkA=5, shrinkB=5),
                expand_points=(1.2, 1.2))
except Exception:
    print("Note: adjustText optimization skipped.")

plt.xticks(list(x_mapping.values()), list(x_mapping.keys()), fontsize=12)
plt.axhline(0, linestyle="--", color="grey", linewidth=0.8)
plt.title("Defensemen PCA Comparison (Dual Input: Raw + Relative)", fontsize=16)
plt.ylabel("Standardized Score (Z-Score)", fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.legend()
plt.tight_layout()

plt.savefig("defensemen_pca_comparison.png", dpi=150)
print("Saved: defensemen_pca_comparison.png")
plt.show()
