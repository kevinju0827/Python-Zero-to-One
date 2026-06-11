# M15 Data Analysis & Visualization

![Module 15 of 16](https://img.shields.io/badge/Module-15_of_16-6366f1?style=flat-square)
![Intermediate](https://img.shields.io/badge/Difficulty-Intermediate-facc15?style=flat-square)
![2 hours](https://img.shields.io/badge/Time-2_hours-60a5fa?style=flat-square)
![Prerequisites: M10 — Data Formats](https://img.shields.io/badge/Prerequisites-M10:_Data_Formats-94a3b8?style=flat-square)

**Topics covered:** `pandas` · DataFrame · `read_csv()` · selecting & filtering · `numpy` & vectorization · missing data (`NaN`) · `groupby()` · `matplotlib` · `df.plot()` · chart labels · `savefig()` · CSV export

## The Why?

In M14 you built a dashboard that displayed sales numbers — but every number on that screen came pre-computed from a fixed JSON file. Someone, somewhere, had to *calculate* "total revenue by category" before your GUI could display it. This module is about being that someone.

Think about how you would answer this question with the tools you have so far: *"Across 16,598 rows of video game sales, what is the total sales per genre?"* With M10's `csv` module, that is a loop, a dictionary of running totals, type conversions, and careful handling of empty cells — 20 lines, easy to get wrong. With **pandas**, it is one line:

```python
df.groupby("Genre")["Global_Sales"].sum()
```

pandas is a spreadsheet you control with code. Everything Excel does — filter, sort, sum, pivot table — pandas does faster, on files too big for Excel to open, and *repeatably*: new data arrives, you re-run the script, done. **matplotlib** then turns those numbers into charts. Together they are the standard toolkit for data analysis in Python — used everywhere from scientific research to business reporting, and one of the main reasons people learn Python at all.

---

## The Dataset

This module uses **[Video Game Sales](https://www.kaggle.com/datasets/gregorut/videogamesales)** from Kaggle — 16,598 games with sales figures (in millions of copies) for North America, Europe, Japan, and the rest of the world, scraped from vgchartz.com around 2016.

**Download it before starting** (free Kaggle account required):

1. Open <https://www.kaggle.com/datasets/gregorut/videogamesales>
2. Click **Download**, unzip, and put `vgsales.csv` **in this folder**.

[Kaggle](https://www.kaggle.com/datasets) hosts thousands of free datasets like this — after this module, go find one about something *you* care about.

---

## Core Concepts

### Installation

Two packages: pandas for analysis, matplotlib for charts.

```bash
pip install pandas matplotlib
```

Run `pip show numpy` afterwards — pip quietly installed a third package you never asked for. **NumPy** is the numerical engine pandas is built on; more on it shortly.

---

### The DataFrame — A Spreadsheet in Code

pandas has one central object: the **DataFrame**. Picture an Excel worksheet — rows, named columns, one data type per column. `pd.read_csv()` loads an entire CSV file into one:

```python
import pandas as pd

df = pd.read_csv("vgsales.csv")   # df is the conventional variable name
print(df.head())                  # First 5 rows — always look first
```

```
   Rank                      Name Platform  ...  JP_Sales Other_Sales Global_Sales
0     1                Wii Sports      Wii  ...      3.77        8.46        82.74
1     2         Super Mario Bros.      NES  ...      6.81        0.77        40.24
2     3            Mario Kart Wii      Wii  ...      3.79        3.31        35.82
3     4         Wii Sports Resort      Wii  ...      3.28        2.96        33.00
4     5  Pokemon Red/Pokemon Blue       GB  ...     10.22        1.00        31.37
```

Compare this with M10: no `open()`, no loop, no manual `float()` conversion. pandas read the file, split the columns, and guessed each column's type in one call. (16,598 rows loaded instantly — try scrolling that in Excel.)

Two more inspection tools you should run on *every* new dataset before analyzing anything:

```python
df.info()    # Column types + how many non-empty values per column
df.shape     # (rows, columns) — here: (16598, 11)
```

```
RangeIndex: 16598 entries, 0 to 16597
 #   Column        Non-Null Count  Dtype
---  ------        --------------  -----
 0   Rank          16598 non-null  int64
 1   Name          16598 non-null  str
 2   Platform      16598 non-null  str
 3   Year          16327 non-null  float64
 4   Genre         16598 non-null  str
 5   Publisher     16540 non-null  str
 6   NA_Sales      16598 non-null  float64
 ...
 10  Global_Sales  16598 non-null  float64
```

Read that output like a detective. Numbers came in as `float64`/`int64` (real numbers, ready for math), text as `str` (older pandas versions print `object` — same meaning). And two lines are quietly alarming: `Year` has only **16327 non-null** values and `Publisher` only **16540** — hundreds of cells are empty. More on that below.

(Also notice `Year` is `float64`, not `int64`. A whole-number column with even one `NaN` gets stored as floats — that is why you will see `2006.0` instead of `2006`. The dtype itself is telling you data is missing.)

---

### Selecting Columns, Filtering Rows

Grab one column with the same square-bracket syntax as a dictionary (M04):

```python
df["Global_Sales"]          # One column — a pandas "Series"
df["Global_Sales"].sum()    # Columns have built-in math: .sum() .mean() .max() .min()
```

Filtering rows reuses the comparison operators from M03 — with a twist. Comparing a whole column produces a column of `True`/`False`, and putting that back into `df[...]` keeps only the `True` rows:

```python
hits = df[df["Global_Sales"] > 10]              # Only games that sold 10M+ copies
nintendo = df[df["Publisher"] == "Nintendo"]    # Only Nintendo games
```

Read `df[df["Publisher"] == "Nintendo"]` inside-out: *"compare every row's publisher to Nintendo, then keep the rows where that was True."* This pattern is called a **boolean mask** and you will use it constantly.

Combine conditions with `&` (and) / `|` (or) — **not** Python's `and`/`or`, and each condition needs its own parentheses:

```python
modern_hits = df[(df["Year"] >= 2010) & (df["Global_Sales"] > 10)]
```

---

### NumPy — The Engine Under pandas

Something strange just happened in the last section, and it deserves a name. `df["Global_Sales"] > 10` compared **16,598 numbers in one expression** — no `for` loop. Where did the loop go?

Into **NumPy**. It is the package pip installed alongside pandas, and it does one thing exceptionally well: the **array**, a sequence of numbers that supports math on the *whole thing at once*:

```python
import numpy as np

prices = np.array([100, 250, 80])     # Looks like a list (M04)...
print(prices * 1.05)                  # ...but math hits every element at once
```

```
[105.  262.5  84. ]
```

Try `[100, 250, 80] * 1.05` with a plain list — `TypeError`. A list would need a `for` loop (M05); an array does it in one expression, running in compiled C far faster than Python can loop. This style is called **vectorization**: *describe the math once, apply it to everything.*

Here is the secret: **every pandas column is a NumPy array wearing a label.** (Peek behind the curtain: `df["Global_Sales"].to_numpy()`.) Each time you wrote column math or a boolean mask, NumPy was doing the work — which is why 16,598 rows feel instant, and why experienced users almost never loop over a DataFrame row by row.

You will mostly use NumPy *through* pandas, but two pieces are worth knowing by name:

- **`np.nan`** — the `NaN` marker for missing data (next section) is literally this NumPy object.
- **`np.where(condition, A, B)`** — a vectorized if/else: one verdict per row, no loop:

```python
df["tier"] = np.where(df["Global_Sales"] >= 1.0, "million-seller", "niche")
print(df["tier"].value_counts())
```

```
tier
niche             14517
million-seller     2081
```

Read it like M03: *"for every row — if global sales ≥ 1.0 million, label it million-seller, else niche."* One line classified the entire industry (and revealed it: only 1 game in 8 ever breaks a million copies).

> pandas for tables, NumPy for raw number-crunching. When you later meet scientific computing, image processing (a digital photo is just a NumPy array of pixels), or machine learning, NumPy is the common language under all of them.

---

### Missing Data — `NaN` Is Normal

Real-world data is dirty. Sensors go offline, people skip form fields, web scrapers miss pages. pandas marks every empty cell as `NaN` ("Not a Number"), and your first job with any dataset is to find them and decide what to do:

```python
df["Year"].isna().sum()   # How many missing? → 271
```

Two standard responses:

```python
df.dropna(subset=["Year"])     # Drop rows where the year is missing
df.fillna(0)                   # Or: replace every NaN with a value
```

**Which one is correct depends on the meaning of the data, not the code.** Here, a missing `Year` means "nobody recorded when this game came out" — the game still exists and its sales still count. `fillna(0)` would invent games released in the year 0 and wreck every timeline. Dropping those rows *from year-based questions only* is honest; inventing values is not. Always ask: *what does "missing" mean here?*

> This is M08's defensive mindset applied to data: the failure case (`NaN`) is not an error to silence — it is information to handle deliberately.

---

### Sorting and Quick Statistics

```python
df.sort_values("Global_Sales", ascending=False)   # Best sellers first
df["Platform"].value_counts()                     # Count games per platform
df["Global_Sales"].describe()                     # count/mean/min/max/quartiles in one shot
```

`describe()` is the 10-second health check: the mean game sold 0.54 million copies but the max is 82.74 — a few giant hits dominate thousands of tiny titles. If you saw a max of 8 *billion*, you would have a data entry problem, not a hit. Always sanity-check before you trust.

---

### `groupby()` — The Pivot Table of Code

The single most important tool in this module. `groupby()` implements **split → apply → combine**:

```
                  split by Genre            apply .sum()           combine
all 16,598 rows ─┬─ 3,316 Action rows   ──→  Action total     ─┐
                 ├─ 2,346 Sports rows   ──→  Sports total     ─┤──→  one small
                 ├─ 1,488 RPG rows      ──→  RPG total        ─┤     result table
                 └─ ... (12 genres)     ──→  ...              ─┘
```

```python
df.groupby("Genre")["Global_Sales"].sum()
```

Read it left to right: *"split `df` into one group per `Genre`, take each group's `Global_Sales` column, sum it."* The result (sorted, in millions):

```
Genre
Action          1751.2
Sports          1330.9
Shooter         1037.4
Role-Playing     927.4
Platform         831.4
...
Strategy         175.1
```

If you have used Excel's pivot table, this is the same idea — but written down, version-controlled, and re-runnable. Swap `.sum()` for `.mean()`, `.max()`, or `.count()`, or group by `Platform` instead of `Genre`, and you have answered a different question in one edit. That is the workflow of data analysis: **every question becomes one groupby line.**

---

### Charts in One Line — `df.plot()`

matplotlib is Python's standard charting library. pandas integrates with it directly: any DataFrame or Series has a `.plot()` method.

```python
import matplotlib.pyplot as plt

totals = df.groupby("Genre")["Global_Sales"].sum()
totals.plot(kind="bar")    # Draw it
plt.show()                 # ...then actually open the window
```

Two things beginners hit immediately:

1. **"Why is there no window?"** — `.plot()` only *prepares* the chart. Nothing appears until `plt.show()`. (Same idea as M12's `commit()`: do the work, then make it real.)
2. **One chart per canvas.** Drawing a second chart without `plt.figure()` first stacks it *on top of* the previous one. Start every new chart with `plt.figure()`.

The `kind` parameter picks the chart type, and choosing the right one is part of the skill:

| `kind=` | Shape | Use when asking... |
|---------|-------|--------------------|
| `"bar"` | Bars | Which category is biggest? |
| `"line"` | Lines | How does it change over time? |
| `"pie"` | Pie | What share of the whole? (Use sparingly) |

---

### Finishing a Chart — Labels and Saving

A chart without a title and axis labels is a guess, not a report. Note the first line: we draw the chart *again* — the `plt.show()` you called in the last section handed the canvas to the window and **cleared it**, so labels added now would land on a fresh, empty canvas:

```python
totals.plot(kind="bar")                       # Draw again — show() cleared the canvas
plt.title("Global Video Game Sales by Genre")
plt.xlabel("Genre")
plt.ylabel("Sales (millions of copies)")
plt.tight_layout()                            # Stop labels from being cut off
plt.savefig("sales.png", dpi=150)             # Save BEFORE plt.show()
plt.show()
```

> **Order matters, twice:** labels and `savefig()` only apply to a canvas that still has the chart on it. Draw → label → `savefig()` → `show()`, always in that order — call `show()` too early and you will label (or save) a blank image.

---

### Exporting Results

Analysis nobody can open is analysis nobody uses. Hand your results back in a format everyone reads:

```python
totals.to_csv("genre_totals.csv")
```

This closes the loop with M10: pandas reads *and* writes the CSV format you already know — except now a 12-row summary comes out instead of 16,598 raw rows. The file opens directly in Excel, Google Sheets, or any text editor.

---

## Going Further

<details>
<summary>Reading Straight from a Database (M12 Tie-In)</summary>

pandas can skip CSV entirely and query SQLite directly — your M12 expense tracker is one line away from analysis:

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect("expenses.db")
df = pd.read_sql("SELECT * FROM expenses", conn)
df.groupby("category")["amount"].sum().plot(kind="bar")
```

</details>

<details>
<summary>Chinese Labels in Charts — Fixing the Empty Boxes</summary>

matplotlib's default font cannot display Chinese (or Japanese/Korean). The first time you put a Chinese label in a chart title, every character renders as an empty box: □□. The fix is two settings, placed once right after the import:

```python
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = [
    "Microsoft JhengHei",   # Windows
    "PingFang TC",          # macOS
    "Noto Sans CJK TC",     # Linux
]
plt.rcParams["axes.unicode_minus"] = False   # Keeps the minus sign from breaking too
```

matplotlib walks the list and uses the first font installed on your machine, so the same script works on every OS. This module's dataset uses English labels, but the moment you chart real Taiwan open data you will meet this — remember it exists.

</details>

<details>
<summary>Real Open Data — Encoding Survival Guide</summary>

[Taiwan Open Data](https://data.gov.tw/) CSVs come in mixed encodings. If `read_csv` raises `UnicodeDecodeError` or shows garbled Chinese:

```python
df = pd.read_csv("file.csv", encoding="utf-8-sig")   # Try first (handles the BOM)
df = pd.read_csv("file.csv", encoding="big5")        # Older government files
```

This is the same encoding story from M09's file I/O — it never goes away; you just learn the two magic words.

</details>

<details>
<summary>pivot_table — Two-Dimensional groupby</summary>

`groupby` answers "per genre". What about "per genre *per platform*" as a grid?

```python
pd.pivot_table(df, values="Global_Sales", index="Genre",
               columns="Platform", aggfunc="sum")
```

Rows = genres, columns = platforms, cells = total sales. This *is* Excel's pivot table, by the same name.

</details>

<details>
<summary>Joining Two Tables with merge()</summary>

Real analysis often spans tables — sales in one file, product info in another. `pd.merge(sales, products, on="product_id")` lines them up by a shared key, exactly like SQL's `JOIN`.

</details>

<details>
<summary>More Chart Types</summary>

```python
df.plot(kind="scatter", x="NA_Sales", y="JP_Sales")    # Are two columns related?
df["Year"].plot(kind="hist", bins=30)                  # Distribution shape
```

When you outgrow matplotlib's defaults, look at **seaborn** (prettier statistical charts) and **plotly** (interactive, zoomable charts in the browser).

</details>

<details>
<summary>Where Analysts Actually Work — Jupyter</summary>

Data people rarely run analysis as plain scripts. **Jupyter notebooks** (`pip install notebook`) mix code, output, and charts in one document, one runnable cell at a time — built for the "ask, look, ask again" rhythm of analysis. PyCharm and VS Code both render `.ipynb` files. The pandas you learned here is identical there.

</details>

---

## Guided Practice

**Scenario:** you have downloaded `vgsales.csv` ([Kaggle link](https://www.kaggle.com/datasets/gregorut/videogamesales) — see *The Dataset* above) into this folder: 16,598 games, sales per region in millions of copies. You will produce a small **industry report**: the best-selling game ever, which genres dominate, whether Japan and North America like the same games, two charts, and a summary CSV.

The finished script is `game_sales_example.py`. Build it step by step:

### Step 1 — Load and inspect

Create `game_sales_example.py` in this folder. Start with the imports and a first look at the data:

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv("vgsales.csv")
print(df.head())
df.info()
```

Run it. In the `info()` output, find the problems before reading on: which two columns have fewer than 16,598 non-null values? And why is `Year` a `float64`?

### Step 2 — Clean

Count the damage, then decide what to do about it:

```python
missing_year = df["Year"].isna().sum()
print(f"Games with no release year: {missing_year}")     # → 271

released = df.dropna(subset=["Year"]).copy()
released["Year"] = released["Year"].astype(int)          # 2006.0 → 2006
print(f"Rows kept for year-based analysis: {len(released)} of {len(df)}")
```

Note the design decision: we keep **two** DataFrames. `released` (16,327 rows) for any question involving the year, the full `df` (16,598 rows) for everything else — the sales columns have no gaps, so dropping those rows would throw away good data. And we did *not* use `fillna(0)`: a missing year is unknown, not the year zero.

### Step 3 — Answer questions with groupby

```python
print("\n=== Best-selling game ever ===")
top = df.loc[df["Global_Sales"].idxmax()]
print(f"{top['Name']} ({top['Platform']}) — {top['Global_Sales']} million copies")

print("\n=== Global sales by genre (millions) ===")
sales_by_genre = df.groupby("Genre")["Global_Sales"].sum()
sales_by_genre = sales_by_genre.sort_values(ascending=False)
print(sales_by_genre.round(1))

print("\n=== Do Japan and North America like the same games? ===")
taste = df.groupby("Genre")[["NA_Sales", "JP_Sales"]].sum().round(1)
print(f"NA favorite: {taste['NA_Sales'].idxmax()} ({taste['NA_Sales'].max()} M)")
print(f"JP favorite: {taste['JP_Sales'].idxmax()} ({taste['JP_Sales'].max()} M)")

print("\n=== Million-sellers vs the rest ===")
df["tier"] = np.where(df["Global_Sales"] >= 1.0, "million-seller", "niche")
print(df["tier"].value_counts())
```

Expected results: the best seller is **Wii Sports (82.74 M)**, Action is the biggest genre worldwide (1751.2 M)... and the two markets genuinely disagree — North America's favorite is **Action (877.8 M)** while Japan's is **Role-Playing (352.3 M)**. A cultural difference you just *measured*. The `np.where` line splits the industry in one expression: **2,081 million-sellers vs 14,517 niche titles** — only about 1 game in 8 ever breaks a million copies. Notice what happened: four real questions, one line each.

### Step 4 — Bar chart: sales by genre

```python
plt.figure(figsize=(9, 5))
sales_by_genre.plot(kind="bar", color="steelblue")
plt.title("Global Video Game Sales by Genre, 1980–2016")
plt.xlabel("Genre")
plt.ylabel("Sales (millions of copies)")
plt.xticks(rotation=45, ha="right")     # 12 genre names need a tilt to fit
plt.tight_layout()
plt.savefig("sales_by_genre.png", dpi=150)
plt.show()
```

The staircase from Action down to Strategy should match your Step 3 numbers — but now visible at a glance.

### Step 5 — Line chart: the industry over time

Year questions use `released`, the cleaned DataFrame from Step 2:

```python
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
```

You should see the industry climb for decades to a dramatic peak in **2008 (≈679 M copies)**, then fall off a cliff. Is that the game industry dying — or a dataset scraped in 2016 that never saw the years after it was collected? (Check: which years could a 2016 snapshot possibly cover completely?) A chart can mislead as easily as it can inform; *knowing where the data came from* is part of reading it. Trends like this are invisible in a table and obvious in a line chart — that is the entire point of visualization.

### Step 6 — Export the summary

Build a small summary table (one row per genre) and write it back out as CSV — full circle to where the data came in:

```python
summary = pd.DataFrame({
    "titles": df.groupby("Genre")["Name"].count(),
    "global_sales_m": df.groupby("Genre")["Global_Sales"].sum().round(1),
    "na_sales_m": df.groupby("Genre")["NA_Sales"].sum().round(1),
    "jp_sales_m": df.groupby("Genre")["JP_Sales"].sum().round(1),
})
summary = summary.sort_values("global_sales_m", ascending=False)
summary.to_csv("genre_summary.csv")
print("Saved: genre_summary.csv")
```

Open `genre_summary.csv` (Excel and Google Sheets both read it directly) and check it against your Step 3 console output. You have just shipped a complete pipeline: 16,598 raw rows in → cleaned → analyzed → charted → a 12-row report out.

---

## Checkpoints

* [ ] **Platform Wars**
  Group by `Platform` instead of `Genre` and chart the **top 10** platforms by total global sales as a bar chart *(hint: `.head(10)` works on a sorted Series)*.
  Then compare with `df["Platform"].value_counts()` — the platform with the *most games* is not the one with the *most sales*. Why might that be?

* [ ] **The Nintendo Question**
  Using boolean masks: how many games did Nintendo publish, and what fraction of *all* global sales do they represent?
  Then combine two masks: of games released **after 2005** that sold **over 10 M copies**, how many are Nintendo's?
  *(Hint: combine conditions with `&` — parentheses around each.)*

* [ ] **Analyze Your Own Data**
  Point this module's pipeline at data of your own choosing — either `M10DataFormat/daily_sales.csv` (revenue per product: quantity × unit price, then `groupby("product_name")`), your M12 expense tracker via `pd.read_sql` (see Going Further), or best of all: browse [Kaggle Datasets](https://www.kaggle.com/datasets) for a topic you actually care about — movies, music, sports, anime — and download one.
  Deliver one chart (PNG) and one summary CSV. For an extra challenge, use a CSV from [data.gov.tw](https://data.gov.tw/) and survive its encoding.
