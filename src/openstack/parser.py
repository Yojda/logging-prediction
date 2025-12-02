from logparser.Drain import LogParser
import pandas as pd

def main(resources_dir):
    input_dir = f'{resources_dir}/openstack/log'  # The input directory of log file
    output_dir = f'{resources_dir}/openstack/log-templates'  # The output directory of parsing results
    log_format = '<FileName> <Date> <Timestamp> <PID> <Level> <Component> \[<ADDR>\] <Content>' # Define log format to split message fields
    # Regular expression list for optional preprocessing (default: [])
    regex = [
    ]
    st = 0.2  # Similarity threshold
    depth = 6  # Depth of all leaf nodes

    parser = LogParser(log_format, indir=input_dir, outdir=output_dir,  depth=depth, st=st, rex=regex)
    parser.parse('OpenStack_log_others.log')

    parser = LogParser(log_format, indir=input_dir, outdir=output_dir,  depth=2, st=0.75, rex=regex)
    parser.parse('OpenStack_log_requests.log')

    df_requests = pd.read_csv(f'{output_dir}/OpenStack_log_requests.log_structured.csv')
    df_requests["EventId"] = "request-" + df_requests["EventId"].astype(str)
    df_others = pd.read_csv(f'{output_dir}/OpenStack_log_others.log_structured.csv')
    df_others["EventId"] = "other-" + df_others["EventId"].astype(str)

    df_combined = pd.concat([df_requests, df_others], ignore_index=True)
    df_combined.to_csv(f'{output_dir}/OpenStack.log_structured.csv', index=False)

if __name__ == "__main__":
    from pathlib import Path
    RESOURCES_DIR = Path(__file__).resolve().parents[2] / "resources"
    main(RESOURCES_DIR)