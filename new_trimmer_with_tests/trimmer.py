import argparse


def gc_content(nt_sequence):
    return (nt_sequence.count("G") + nt_sequence.count("C")) / len(nt_sequence) * 100


def fastq_reader(opened_file):
    fastq_read = list()
    for line in opened_file:
        fastq_read.append(line.strip())
        if len(fastq_read) == 4:
            yield fastq_read
            fastq_read.clear()


def fastq_read_check(fastq_read, min_length, gc_min, gc_max):
    return len(fastq_read[1]) >= min_length and gc_min <= gc_content(fastq_read[1]) <= gc_max


def trimmer(fastq_file, output_base_name, min_length, gc_min, gc_max, keep_filtered):
    with open(fastq_file, "r") as reads_input, open("{}_passed.fastq".format(output_base_name),
                                                    'w') as passed_output:

        if keep_filtered:
            failed_output = open("{}_failed.fastq".format(output_base_name), "w")

        reads_total = 0
        passed_counter = 0
        failed_counter = 0

        for fq_read in fastq_reader(reads_input):
            reads_total += 1
            if fastq_read_check(fq_read, min_length, gc_min, gc_max):
                passed_output.write("\n".join(fq_read))
                passed_output.write("\n")
                passed_counter += 1
            elif keep_filtered:
                failed_output.write("\n".join(fq_read))
                failed_output.write("\n")
                failed_counter += 1
        if keep_filtered:
            failed_output.close()
        print("Total reads processed: {}".format(reads_total))
        print("Reads passed: {} ({}%)".format(passed_counter, passed_counter / reads_total * 100))
        print("Reads failed: {} ({}%)".format(failed_counter, failed_counter / reads_total * 100))


if __name__ == '__main__':

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
             "If not value specified, all reads will be selected."
             "Example: python3 trimmer.py --gc_bounds 45 --gc_bounds 50 my_reads.fastq"
    )
    parser.add_argument(
        "--output_base_name",
        type=str,
        help="Common prefix for output files"
    )
    args = parser.parse_args()

    if not args.output_base_name:
        args.output_base_name = args.fastq_file[:-6]

    if args.gc_bounds:
        gc_min = args.gc_bounds[0]
        if len(args.gc_bounds) == 2:
            gc_max = args.gc_bounds[1]
        else:
            gc_max = 100
    else:
        gc_min, gc_max = 0, 100

    trimmer(fastq_file=args.fastq_file, output_base_name=args.output_base_name, min_length=args.min_length,
            gc_min=gc_min, gc_max=gc_max, keep_filtered=args.keep_filtered)
