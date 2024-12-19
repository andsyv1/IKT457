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
    "Board Size": ["27x27"] * 24,
    "Clauses": [1, 10, 50, 100, 500, 1000, 5000, 10000] * 3,
    "Accuracy": [
        51.20, 52.35, 50.75, 50.55, 49.25, 48.85, 51.45, 47.90,  # End of Game
        46.10, 51.20, 51.55, 51.20, 51.80, 48.80, 50.65, 50.40,  # Two Moves Before End
        49.40, 50.25, 51.50, 49.75, 51.55, 49.90, 50.60, 50.75   # Five Moves Before End
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
plt.title("Accuracy Distribution by Scenario and Board Size (27x27)")
plt.show()

sns.lmplot(data=df, x="Clauses", y="Accuracy", hue="Scenario", col="Board Size", ci=None, height=4, aspect=1)
plt.show()
