import pandas as pd
import ast
import matplotlib.pyplot as plt

def main(resources_dir):
    df_logs = pd.read_csv(f"{resources_dir}/openstack/log-templates/OpenStack.log_structured.csv")

    print(df_logs.columns)
    print(df_logs.shape)

    fault_traceids = ["544fd51c-4edc-4780-baae-ba1d80a0acfc", "ae651dff-c7ad-43d6-ac96-bbcd820ccca8", "a445709b-6ad0-40ec-8860-bec60b6ca0c2", "1643649d-2f42-4303-bfcd-7798baec19f9"]

    df_logs["Instance"] = df_logs["Content"].str.extract(r'instance:\s*([a-z0-9-]*)')
    df_logs["Severity"] = df_logs["Instance"].apply(lambda t: 1 if t in fault_traceids else 0)

    print(df_logs)

    grouped = df_logs.groupby("Instance")["EventId"].apply(list)

    print(grouped)

    df_logs['Count'] = 1
    event_matrix = df_logs.pivot_table(index="Instance", columns="EventId", values="Count", aggfunc="sum").fillna(0).astype(int)

    severity_by_instance = df_logs.groupby("Instance")["Severity"].max()
    event_matrix["Severity"] = severity_by_instance

    print(event_matrix)

    # event_matrix.columns = [f"E{i+1}" for i in range(event_matrix.shape[1] - 1)] + ["Severity"]
    event_matrix = event_matrix.reset_index()
    event_matrix.rename(columns={"Instance": "Sequence"}, inplace=True)
    event_matrix["Sequence"] = [f"S{i+1}" for i in range(event_matrix.shape[0])]

    severity_counts = event_matrix["Severity"].value_counts()
    print(severity_counts)

    ax = severity_counts.plot(kind='bar', color=['green', 'red'])
    ax.set_xlabel("Severity Level")
    ax.set_ylabel("Number of Sequences")
    plt.title("Distribution of Sequences by Severity Level in OpenStack Logs")
    plt.savefig(f"{resources_dir}/images/severity_counts_openstack.png", dpi=300, bbox_inches="tight")

    event_matrix.to_csv(f"{resources_dir}/openstack/log-structured/OpenStack.log_sequences.csv", index=False)

if __name__ == "__main__":
    from pathlib import Path
    RESOURCES_DIR = Path(__file__).resolve().parents[2] / "resources"
    main(RESOURCES_DIR)
    plt.show()