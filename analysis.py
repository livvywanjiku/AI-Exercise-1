import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# Step 1: Load the CSV
# ============================================================
df = pd.read_csv("results.csv")
print(df.head())

# ============================================================
# Basic Exploration
# ============================================================
print("\n=== BASIC EXPLORATION ===")

# How many matches?
print(f"Total matches: {df.shape[0]}")

# Earliest and latest year
print(f"Earliest date: {df['date'].min()}")
print(f"Latest date:   {df['date'].max()}")

# Unique countries
all_teams = pd.concat([df['home_team'], df['away_team']])
print(f"Unique countries: {all_teams.nunique()}")

# Most frequent home team
print("\nTop 5 home teams:")
print(df['home_team'].value_counts().head())

# ============================================================
# Goals Analysis
# ============================================================
print("\n=== GOALS ANALYSIS ===")

df['total_goals'] = df['home_score'] + df['away_score']

print(f"Average goals per match: {df['total_goals'].mean():.2f}")

max_row = df.loc[df['total_goals'].idxmax()]
print(f"Highest scoring match: {max_row['home_team']} {max_row['home_score']}-{max_row['away_score']} {max_row['away_team']} on {max_row['date']}")

print(f"Total home goals: {df['home_score'].sum()}")
print(f"Total away goals: {df['away_score'].sum()}")

print(f"Most common total goals: {df['total_goals'].mode()[0]}")

# ============================================================
# Match Results
# ============================================================
print("\n=== MATCH RESULTS ===")

def match_result(row):
    if row['home_score'] > row['away_score']:
        return 'Home Win'
    elif row['home_score'] < row['away_score']:
        return 'Away Win'
    else:
        return 'Draw'

df['result'] = df.apply(match_result, axis=1)

result_counts = df['result'].value_counts()
result_pct = df['result'].value_counts(normalize=True) * 100

print(result_counts)
print(result_pct.round(2))

home_wins = df[df['result'] == 'Home Win'].groupby('home_team').size()
away_wins = df[df['result'] == 'Away Win'].groupby('away_team').size()
total_wins = home_wins.add(away_wins, fill_value=0).sort_values(ascending=False)
print("\nTop 10 countries by total wins:")
print(total_wins.head(10))

# ============================================================
# Visualisations
# ============================================================

# Figure 1: Histogram of goals
plt.figure(figsize=(9, 5))
df['total_goals'].hist(bins=range(0, 22), color='#3498db', edgecolor='white', rwidth=0.85)
plt.title('Distribution of Total Goals Per Match', fontsize=14, fontweight='bold')
plt.xlabel('Total Goals in Match')
plt.ylabel('Number of Matches')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('fig1_goals_histogram.png', dpi=140)
plt.show()

# Figure 2: Bar chart of match outcomes
plt.figure(figsize=(7, 5))
colors = {'Home Win': '#2ecc71', 'Away Win': '#e74c3c', 'Draw': '#f39c12'}
bars = plt.bar(result_counts.index, result_counts.values,
               color=[colors[r] for r in result_counts.index], width=0.5)
for bar, val in zip(bars, result_counts.values):
    pct = val / len(df) * 100
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200,
             f'{pct:.1f}%', ha='center', fontweight='bold')
plt.title('Match Outcomes', fontsize=14, fontweight='bold')
plt.ylabel('Number of Matches')
plt.tight_layout()
plt.savefig('fig2_match_outcomes.png', dpi=140)
plt.show()

# Figure 3: Top 10 teams by total wins
top10 = total_wins.head(10)
plt.figure(figsize=(10, 6))
plt.barh(top10.index[::-1], top10.values[::-1], color='#9b59b6')
plt.title('Top 10 Countries by Total Wins (All-Time)', fontsize=14, fontweight='bold')
plt.xlabel('Total Wins')
plt.tight_layout()
plt.savefig('fig3_top10_wins.png', dpi=140)
plt.show()

print("\nDone! Charts saved as PNG files.")
