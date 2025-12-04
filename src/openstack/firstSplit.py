import pandas as pd

def main(resources_dir):
    lines = []

    with open(f"{resources_dir}/openstack/log/openstack_abnormal.log", "r", encoding="utf-8", errors="ignore") as f:
        lines += f.readlines()

    with open(f"{resources_dir}/openstack/log/openstack_normal1.log", "r", encoding="utf-8", errors="ignore") as f:
        lines += f.readlines()

    with open(f"{resources_dir}/openstack/log/openstack_normal2.log", "r", encoding="utf-8", errors="ignore") as f:
        lines += f.readlines()

    df = pd.DataFrame(lines, columns=["Message"])
    print(df.head())

    print(df.columns)

    df["is_http"] = df["Message"].str.contains(r'HTTP/1.1', case=False, na=False)
    df["status_code"] = df["Message"].str.extract(r'status[:=]\s*(\d{3})')
    df["status_code"] = pd.to_numeric(df["status_code"], errors="coerce")

    df_requests = df[df["is_http"]].copy()
    print(len(df_requests))
    df_others = df[~df["is_http"]].copy()
    print(len(df_others))

    # Drop helper columns (just in case)
    df_requests = df_requests.drop(columns=["is_http", "status_code", "RequestResult"], errors="ignore")
    df_others = df_others.drop(columns=["is_http", "status_code", "Category"], errors="ignore")

    # Remove possible embedded newlines from the log messages
    df_requests["Message"] = df_requests["Message"].str.strip()
    df_others["Message"] = df_others["Message"].str.strip()

    # Save manually joined logs — ensures no extra \n
    with open(f"{resources_dir}/openstack/log/OpenStack_log_requests.log", "w", encoding="utf-8") as f:
        f.write("\n".join(df_requests["Message"].tolist()))

    with open(f"{resources_dir}/openstack/log/OpenStack_log_others.log", "w", encoding="utf-8") as f:
        f.write("\n".join(df_others["Message"].tolist()))

if __name__ == "__main__":
    from pathlib import Path
    RESOURCES_DIR = Path(__file__).resolve().parents[2] / "resources"
    main(RESOURCES_DIR)