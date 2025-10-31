import pandas as pd
import ast
import matplotlib.pyplot as plt

df_logs = pd.read_csv("../../resources/openstack/log-templates/OpenStack.log_structured.csv")

print(df_logs.columns)
print(df_logs.shape)

df_logs["TraceId"] = df_logs["ADDR"].apply(lambda x: str(x).split(" ")[0])

print(df_logs)

grouped = df_logs.groupby("TraceId")["EventId"].apply(list)

print(grouped)

df_logs['Count'] = 1
event_matrix = df_logs.pivot_table(index="TraceId", columns="EventId", values="Count", aggfunc="sum").fillna(0).astype(int)

severity_order = {"INFO": 0, "ERROR": 1}
df_logs["Severity"] = df_logs["Severity"].map(severity_order)
severity_by_window = (
    df_logs.groupby("TraceId")["Severity"].max()
)
reverse_map = {v: k for k, v in severity_order.items()}
severity_by_window_str = severity_by_window.map(reverse_map)

event_matrix = event_matrix.merge(
    severity_by_window.rename("Severity"), on="TraceId", how="left"
)

print(event_matrix)

df_template = df_logs
count = 0
for event,severity in zip(df_template["EventId"], df_template["Severity"]):
    if severity == 1:
        if event in event_matrix.columns:
            event_matrix = event_matrix.drop(event, axis=1)
            count += 1

print(f"Dropped {count} ERROR events from the event matrix.")

# event_matrix.columns = [f"E{i+1}" for i in range(event_matrix.shape[1] - 1)] + ["Severity"]
event_matrix = event_matrix.reset_index()
event_matrix.rename(columns={"TraceId": "Sequence"}, inplace=True)
event_matrix["Sequence"] = [f"S{i+1}" for i in range(event_matrix.shape[0])]

severity_counts = event_matrix["Severity"].value_counts()
print(severity_counts)

ax = severity_counts.plot(kind='bar', color=['green', 'red'])
ax.set_xlabel("Severity Level")
ax.set_ylabel("Number of Sequences")
plt.title("Distribution of Sequences by Severity Level")
plt.savefig("../../resources/images/severity_counts_openstack.png", dpi=300, bbox_inches="tight")

event_matrix.to_csv("../../resources/openstack/log-structured/OpenStack.log_sequences.csv", index=False)

plt.show()