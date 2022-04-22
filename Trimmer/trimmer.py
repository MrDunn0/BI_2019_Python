import argparse


class FastqRead:
    def __init__(self, read: list):
        if len(read) != 4:
            raise ValueError("Your list should consist of 4 elements")
        self.read = read
        self.seq = read[1]
        self.encoded_quality = [i for i in read[3]]
        self.phred_quality = self.__get_quality()
        self.__length = len(self.seq)

    def __get_quality(self):
        return [ord(nt) - 33 for nt in self.encoded_quality]

    def __getitem__(self, key):
        new_read = list()
        new_read.extend([self.read[0], self.seq[key], self.read[2], self.read[3][key]])
        return FastqRead(new_read)

    def __iter__(self):
        return iter(self.seq)

    def __len__(self):
        return self.__length


def gc_content(nt_sequence):
    return (nt_sequence.count("G") + nt_sequence.count("C")) / len(nt_sequence) * 100


def fastq_reader(opened_file):
    fastq_read = list()
    for line in opened_file:
        fastq_read.append(line.strip())
        if len(fastq_read) == 4:
            yield FastqRead(fastq_read)
            fastq_read.clear()


def crop(fq_read, length):
    return fq_read[0:length] if len(fq_read) > length else None


def headcrop(fq_read, length):
    return fq_read[length:] if len(fq_read) > length else None


def sliding_window(fq_read, window_size, required_quality):
    """
    :param fq_read: Bio.SeqRecord.SeqRecord object
    :param window_size: specifies the number of bases to average across
    :param required_quality: specifies the average quality required.
    :return: Trimmed read or  "None" if window size > read length or read is trimmed completely
    Uses BIO.SeqIO
    """

    good_record = None
    windows = int(len(fq_read) // window_size) + 1
    if windows > 1:
        for window in range(1, windows + 1):
            sub_record = fq_read[0:window_size * window]
            average_quality = sum(sub_record[-window_size:].phred_quality) / window_size
            if average_quality < required_quality:
                break
            good_record = sub_record
    else:
        if sum(fq_read.phred_quality) / len(fq_read) >= required_quality:
            good_record = fq_read
    return good_record


def leading_cut(fq_read, required_quality):
    read_start = 0
    for i, quality in enumerate(fq_read.phred_quality):
        if quality >= required_quality:
            read_start = i
            break
        elif i == len(fq_read) - 1:
            return None
    return fq_read[read_start:]


def trailing_cut(fq_read, required_quality):
    read_start = 0
    for i, quality in enumerate(fq_read[::-1].phred_quality):
        if quality >= required_quality:
            read_start = i
            break
        elif i == len(fq_read) - 1:
            return None
    return fq_read[::-1][read_start:][::-1]


def apply_trimmers(fq_read, args):
    trimmers = {"CROP": (args.CROP, crop), "HEADCROP": (args.HEADCROP, headcrop),
                "LEADING": (args.LEADING, leading_cut), "TRAILING": (args.TRAILING, trailing_cut),
                "SLIDINGWINDOW": (args.SLIDINGWINDOW, sliding_window)}
    for name, trimmer in trimmers.items():
        if trimmer[0]:
            if name == "SLIDINGWINDOW":
                fq_read = sliding_window(fq_read, int(trimmer[0][0]), int(trimmer[0][1]))
            else:
                fq_read = trimmer[1](fq_read, trimmer[0])
                # print(fq_read.read)
    return fq_read


def apply_filters(fastq_read: str, min_length, gc_min, gc_max):
    return len(fastq_read) >= min_length and gc_min <= gc_content(fastq_read) <= gc_max


def parse_args():
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
        nargs="+",
        default=[0, 100],
        help="The range of quantitative content of GC. First and second values are min and max respectively."
             "If only one value is specified, then reads with greater or equal value will be selected."
             "If not value specified, all reads will be selected."
    )
    parser.add_argument(
        "--output_base_name",
        type=str,
        help="Common prefix for output files"
    )
    parser.add_argument(
        "--CROP",
        type=int,
        help="The number of bases to keep, from the start of the read"
    )
    parser.add_argument(
        "--HEADCROP",
        type=int,
        help="The number of bases to remove from the start of the read"
    )
    parser.add_argument(
        "--LEADING",
        type=int,
        help="Quality threshold for bases at the beginning of a read"
    )
    parser.add_argument(
        "--TRAILING",
        type=int,
        help="Quality threshold for bases at the end of a read"
    )
    parser.add_argument(
        "--SLIDINGWINDOW",
        type=float,
        nargs="+",
        help="--SLIDINGWINDOW <window_size> <required_quality>"
             "window_size - number of bases to average across"
             "required_quality - average quality required"
    )
    args = parser.parse_args()
    if not args.output_base_name:
        args.output_base_name = args.fastq_file[:-6]
    return args


def main(args):
    with open(args.fastq_file, "r") as reads_input, open("{}_passed.fastq".format(args.output_base_name),
                                                         'w') as passed_output:
        statistics = {"reads_total": 0, "passed_counter": 0,
                      "failed_counter": 0, "failed_on_trimming": 0, "failed_on_filters": 0}
        if args.keep_filtered:
            failed_output = open("{}_failed.fastq".format(args.output_base_name), "w")

        fastq_parser = fastq_reader(reads_input)
        for initial_read in fastq_parser:
            statistics["reads_total"] += 1
            fq_read = apply_trimmers(initial_read, args)
            if fq_read:

                if apply_filters(fq_read.seq, args.min_length, args.gc_bounds[0], args.gc_bounds[1]):
                    passed_output.write("\n".join(fq_read.read) + "\n")
                    statistics["passed_counter"] += 1
                else:
                    statistics["failed_counter"] += 1
                    statistics["failed_on_filters"] += 1

                if args.keep_filtered:
                    failed_output.write("\n".join(initial_read.read) + "\n")
            else:
                statistics["failed_counter"] += 1
                statistics["failed_on_trimming"] += 1

            if args.keep_filtered:
                failed_output.write("\n".join(initial_read.read) + "\n")

        if args.keep_filtered:
            failed_output.close()
    return statistics


if __name__ == '__main__':
    statistics = main(parse_args())

    print("Total reads processed: {}".format(statistics["reads_total"]))
    print("Reads passed: {} ({}%)".format(statistics["passed_counter"],
                                          round(statistics["passed_counter"] / statistics["reads_total"] * 100, 2)))
    print("Reads failed: {} ({}%)".format(statistics["failed_counter"],
                                          round(statistics["failed_counter"] / statistics["reads_total"] * 100, 2)))
    if statistics["failed_counter"] != 0:
        print("Filed by GC content or min length : {} ({}%)".format(statistics["failed_on_filters"], round(
            statistics["failed_on_filters"] / statistics["failed_counter"] * 100, 2)))
        print("Failed by quality or fully trimmed: {} ({}%)".format(statistics["failed_on_trimming"], round(
            statistics["failed_on_trimming"] / statistics["failed_counter"] * 100, 2)))
