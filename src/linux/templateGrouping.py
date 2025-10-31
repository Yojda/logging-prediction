import pandas as pd

FAILURE_WORDS = {"failure", "failed", "crash"}
WARNING_WORDS = {"warning", "couldn't", "timed out", "critical"}

df = pd.read_csv("../../resources/linux/log-templates/Linux.log_structured.csv")

df["Severity"] = "INFO"
df.loc[df["EventTemplate"].str.contains('|'.join(FAILURE_WORDS), case=False, na=False), "Severity"] = "FAILURE"

df.to_csv("../../resources/linux/log-templates/Linux.log_structured.csv")

