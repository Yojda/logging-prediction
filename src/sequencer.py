import pandas as pd
import ast
import matplotlib.pyplot as plt

df_logs = pd.read_csv("../resources/linux/log-templates/Linux.log_structured.csv")

print(df_logs.columns)
print(df_logs.shape)

df_logs["Time"] = pd.to_datetime(df_logs["Time"], format="%H:%M:%S")

df_logs["window"] = (df_logs["Time"].dt.hour * 3600 + df_logs["Time"].dt.minute * 60 + df_logs["Time"].dt.second) // 15  # 10-seconds windows
grouped = df_logs.groupby("window")["EventId"].apply(list)


df_logs['Count'] = 1
event_matrix = df_logs.pivot_table(index="window", columns="EventId", values="Count", aggfunc="sum").fillna(0)

severity_order = {"INFO": 1, "WARNING": 2, "FAILURE": 3}
df_logs["SeverityLevel"] = df_logs["Severity"].map(severity_order)
severity_by_window = (
    df_logs.groupby("window")["SeverityLevel"].max()
)
reverse_map = {v: k for k, v in severity_order.items()}
severity_by_window = severity_by_window.map(reverse_map)

event_matrix = event_matrix.merge(
    severity_by_window.rename("Severity"), on="window", how="left"
)


# event_matrix.columns = [f"E{i+1}" for i in range(event_matrix.shape[1])]
event_matrix = event_matrix.reset_index()
event_matrix.rename(columns={"window": "Sequence"}, inplace=True)
event_matrix["Sequence"] = [f"S{i+1}" for i in range(event_matrix.shape[0])]

severity_counts = event_matrix["Severity"].value_counts()
print(severity_counts)

ax = severity_counts.plot(kind='bar', color=['green', 'red'])
ax.set_xlabel("Severity Level")
ax.set_ylabel("Number of Sequences")
plt.title("Distribution of Sequences by Severity Level")
plt.savefig("../resources/images/severity_counts.png", dpi=300, bbox_inches="tight")

event_matrix.to_csv("../resources/linux/log-structured/Linux.log_sequences.csv", index=False)

plt.show()