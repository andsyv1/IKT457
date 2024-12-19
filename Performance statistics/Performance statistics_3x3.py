import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import f_oneway

data = {
    "Scenario": [
        "End of Game"] * 8 + 
        ["Two Moves Before End"] * 8 + 
        ["Five Moves Before End"] * 8,
    "Board Size": ["3x3"] * 24,
    "Clauses": [1, 10, 50, 100, 500, 1000, 5000, 10000] * 3,
    "Accuracy": [
        66.60, 67.50, 66.20, 67.10, 66.70, 67.60, 65.80, 67.75,  # End of Game
        66.25, 64.70, 67.55, 67.65, 66.55, 65.55, 65.65, 66.60,  # Two Moves Before End
        65.90, 67.30, 67.75, 66.80, 67.45, 66.40, 65.55, 65.30   # Five Moves Before End
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
plt.title("Accuracy Distribution by Scenario and Board Size")
plt.show()

sns.lmplot(data=df, x="Clauses", y="Accuracy", hue="Scenario", col="Board Size", ci=None, height=4, aspect=1)
plt.show()