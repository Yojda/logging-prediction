import linux
import openstack
import pandas as pd
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]  # up from src/
RESOURCES_DIR = PROJECT_ROOT / "resources"

def run_pipeline(dataset, skipPipeline) -> pd.DataFrame:
    if dataset == "OpenStack":
        pipeline = [openstack.firstSplit, openstack.parser, openstack.templateGrouping, openstack.tracer]
        path = "./resources/openstack/log-structured/OpenStack.log_sequences.csv"
    elif dataset == "Linux":
        pipeline = [linux.parser, linux.templateGrouping, linux.tracer]
        path = "./resources/linux/log-structured/Linux.log_sequences.csv"
    else:
        raise ValueError(f"Unsupported dataset {dataset}, please choose either 'OpenStack' or 'Linux'.")

    if skipPipeline:
        return pd.read_csv(path)

    for step in pipeline:
        step.main(RESOURCES_DIR)

    print(os.getcwd())
    return pd.read_csv(path)
