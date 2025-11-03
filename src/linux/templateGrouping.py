import pandas as pd

def main(resources_dir):
    FAILURE_WORDS = {"failure", "failed", "crash", "abnormally"}

    df = pd.read_csv(f"{resources_dir}/linux/log-templates/Linux.log_structured.csv")

    df["Severity"] = "INFO"
    df.loc[df["EventTemplate"].str.contains('|'.join(FAILURE_WORDS), case=False, na=False), "Severity"] = "FAILURE"

    df.to_csv(f"{resources_dir}/linux/log-templates/Linux.log_structured.csv")

