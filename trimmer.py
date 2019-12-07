import argparse

parser = argparse.ArgumentParser(description="Trimmer for fastq reads")
parser.add_argument(
    "fastq_file",
    type=str,
    help="Path to unzipped fastq-file."
    )
parser.add_argument(
    "--min_length",
    type=int,
    default=0,
    help="Minimal length of reads to be selected. If not specified, then reads of any length will pass the filter."
    )
parser.add_argument(
    "--keep_filtered",
    action="store_true",
    help="Reads that do not pass the filter will be written to a separate file."
    )
parser.add_argument(
    "--gc_bounds",
    type=float,
    action="append",
    help="The range of quantitative content of GC. First and second values are min and max respectively."
         "If only one value is specified, then reads with greater or equal value will be selected."
         "If not value specified, all reads will be selected.\n Example: \n python3 trimmer.py --gc_bounds 45 --gc_bounds 50 my_reads.fastq"
    )
parser.add_argument(
    "--output_base_name",
    type=str,
    help="Common prefix for output files"
    )
args = parser.parse_args()

if not args.output_base_name:
    args.output_base_name = args.fastq_file[-6]

if args.gc_bounds:
    gc_min = args.gc_bounds[0]
    if len(args.gc_bounds) == 2:
        gc_max = args.gc_bounds[1]
    else:
        gc_max = 100
else:
    gc_min, gc_max = 0, 100


def gc_content(read):
    return (read.count("G") + read.count("C")) / len(read) * 100


with open(args.fastq_file, "r") as reads_input, open("{}_passed.fastq".format(args.output_base_name), 'a') as passed_output:
    if args.keep_filtered:
        failed_output = open("{}_failed.fastq".format(args.output_base_name), "a")

    temp_read = list()
    for line in reads_input:
        temp_read.append(line.strip())
        if len(temp_read) == 4:
            if len(temp_read[1]) >= args.min_length and gc_min <= gc_content(temp_read[1]) <= gc_max:
                passed_output.write("\n".join(temp_read))
                passed_output.write("\n")
            elif args.keep_filtered:
                failed_output.write("\n".join(temp_read))
                failed_output.write("\n")
            temp_read.clear()
if args.keep_filtered:
    failed_output.close()
