import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import f_oneway

data = {
    "Scenario": (
        ["End of Game"] * 8 +
        ["Two Moves Before End"] * 8 +
        ["Five Moves Before End"] * 8
    ),
    "Board Size": ["9x9"] * 24,
    "Clauses": [1, 10, 50, 100, 500, 1000, 5000, 10000] * 3,
    "Accuracy": [
        51.15, 54.10, 54.55, 52.35, 47.95, 53.85, 52.75, 43.70,  # End of Game
        53.85, 51.75, 53.40, 52.20, 47.35, 52.75, 53.25, 52.40,  # Two Moves Before End
        53.90, 53.25, 50.05, 52.10, 53.70, 52.15, 46.95, 53.45   # Five Moves Before End
    ]
}

df = pd.DataFrame(data)

print(df.groupby(["Scenario", "Board Size", "Clauses"])["Accuracy"].describe())

anova_result = f_oneway(
    df[df["Scenario"] == "End of Game"]["Accuracy"],
    df[df["Scenario"] == "Two Moves Before End"]["Accuracy"],
    df[df["Scenario"] == "Five Moves Before End"]["Accuracy"]
)
print("ANOVA Result:", anova_result)

plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x="Scenario", y="Accuracy", hue="Board Size")
plt.title("Accuracy Distribution by Scenario and Board Size (9x9)")
plt.show()

sns.lmplot(data=df, x="Clauses", y="Accuracy", hue="Scenario", col="Board Size", ci=None, height=4, aspect=1)
plt.show()
