"""Guided Practice — A video game sales analysis report.

Scenario: `vgsales.csv` holds 16,598 video games with sales figures
(in millions of copies) for North America, Europe, Japan, and the rest
of the world — scraped from vgchartz.com around 2016.

Download the dataset (one CSV file) from Kaggle:
  https://www.kaggle.com/datasets/gregorut/videogamesales
Put `vgsales.csv` in this folder before running.

The file is realistically imperfect: 271 games have no release year and
58 have no publisher recorded.

This script walks the full analysis pipeline:
  1. Load & inspect   — read_csv, head(), info()
  2. Clean            — handle missing years
  3. Analyze          — groupby answers: top genre? Japan vs America taste?
  4. Visualize        — bar chart + line chart
  5. Export           — summary table to CSV

Run it from this folder so the CSV path resolves:
  python game_sales_example.py

Outputs: sales_by_genre.png, sales_by_year.png, genre_summary.csv
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---------------------------------------------------------------
# Step 1 — Load & inspect
# ---------------------------------------------------------------
try:
    df = pd.read_csv("vgsales.csv")
except FileNotFoundError:
    raise SystemExit(
        "[Error] vgsales.csv not found.\n"
        "Download it from https://www.kaggle.com/datasets/gregorut/videogamesales"
        " and put it in this folder."
    )

print("=== First 5 rows ===")
print(df.head())

print("\n=== Structure ===")
df.info()   # Note: Year and Publisher have fewer non-null values!


# ---------------------------------------------------------------
# Step 2 — Clean
# ---------------------------------------------------------------
missing_year = df["Year"].isna().sum()
print(f"\nGames with no release year: {missing_year}")

# A missing Year means "we don't know when it came out" — not "year zero".
# fillna(0) would invent games from the year 0; dropping is honest. Sales
# columns are complete, so we keep the full `df` for sales questions and
# use `released` only when the question involves the year.
released = df.dropna(subset=["Year"]).copy()
released["Year"] = released["Year"].astype(int)   # 2006.0 → 2006
print(f"Rows kept for year-based analysis: {len(released)} of {len(df)}")


# ---------------------------------------------------------------
# Step 3 — Analyze with groupby
# ---------------------------------------------------------------
print("\n=== Best-selling game ever ===")
top = df.loc[df["Global_Sales"].idxmax()]
print(f"{top['Name']} ({top['Platform']}) — {top['Global_Sales']} million copies")

print("\n=== Global sales by genre (millions) ===")
sales_by_genre = df.groupby("Genre")["Global_Sales"].sum()
sales_by_genre = sales_by_genre.sort_values(ascending=False)
print(sales_by_genre.round(1))

print("\n=== Do Japan and North America like the same games? ===")
taste = df.groupby("Genre")[["NA_Sales", "JP_Sales"]].sum().round(1)
print(f"NA favorite: {taste['NA_Sales'].idxmax()} "
      f"({taste['NA_Sales'].max()} M)")
print(f"JP favorite: {taste['JP_Sales'].idxmax()} "
      f"({taste['JP_Sales'].max()} M)")

print("\n=== Million-sellers vs the rest ===")
# np.where = a vectorized if/else: one label per row, no loop needed
df["tier"] = np.where(df["Global_Sales"] >= 1.0, "million-seller", "niche")
print(df["tier"].value_counts())


# ---------------------------------------------------------------
# Step 4 — Visualize
# ---------------------------------------------------------------
# Chart 1: total global sales per genre (bar)
plt.figure(figsize=(9, 5))           # Start a fresh canvas for each chart
sales_by_genre.plot(kind="bar", color="steelblue")
plt.title("Global Video Game Sales by Genre, 1980–2016")
plt.xlabel("Genre")
plt.ylabel("Sales (millions of copies)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("sales_by_genre.png", dpi=150)
plt.show()

# Chart 2: industry size over time (line) — year questions use `released`
plt.figure(figsize=(9, 5))
yearly = released.groupby("Year")["Global_Sales"].sum()
yearly.plot(kind="line", marker=".")
plt.title("Global Video Game Sales per Year")
plt.xlabel("Year")
plt.ylabel("Sales (millions of copies)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("sales_by_year.png", dpi=150)
plt.show()


# ---------------------------------------------------------------
# Step 5 — Export a summary report to CSV
# ---------------------------------------------------------------
summary = pd.DataFrame({
    "titles": df.groupby("Genre")["Name"].count(),
    "global_sales_m": df.groupby("Genre")["Global_Sales"].sum().round(1),
    "na_sales_m": df.groupby("Genre")["NA_Sales"].sum().round(1),
    "jp_sales_m": df.groupby("Genre")["JP_Sales"].sum().round(1),
})
summary = summary.sort_values("global_sales_m", ascending=False)

summary.to_csv("genre_summary.csv")
print("\nSaved: sales_by_genre.png, sales_by_year.png, genre_summary.csv")
