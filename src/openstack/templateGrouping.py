import pandas as pd

# Words that should trigger a WARNING level
FAILURE_WORDS = {"exception"}

# Load your structured OpenStack logs
df = pd.read_csv("../../resources/openstack/log-templates/OpenStack.log_structured.csv")

# Default severity
df["Severity"] = "INFO"

# 🔹 1. Mark lines containing warning words
mask_warning_words = df["EventTemplate"].str.contains('|'.join(FAILURE_WORDS), case=False, na=False)

mask_http_4xx = df["EventTemplate"].str.contains(r"\bstatus[:=]\s*4\d{2}\b", case=False, na=False)
mask_http_5xx = df["EventTemplate"].str.contains(r"\bstatus[:=]\s*5\d{2}\b", case=False, na=False)

df.loc[mask_warning_words, "Severity"] = "ERROR"

df.to_csv("../../resources/openstack/log-templates/OpenStack.log_structured.csv", index=False)