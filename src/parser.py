from logparser.Drain import LogParser

input_dir = '../resources/linux/log' # The input directory of log file
output_dir = '../resources/linux/log-templates'  # The output directory of parsing results
log_file = 'Linux.log'  # The input log file name
log_format = '<Month> <Day> <Time> <Machine> <Service>(\[<PID>\])?: <Content>' # Define log format to split message fields
# Regular expression list for optional preprocessing (default: [])
regex = [
]
st = 0.5  # Similarity threshold
depth = 4  # Depth of all leaf nodes

parser = LogParser(log_format, indir=input_dir, outdir=output_dir,  depth=depth, st=st, rex=regex)
parser.parse(log_file)