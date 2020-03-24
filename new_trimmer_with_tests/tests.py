import unittest
import trimmer


class TestTrimmer(unittest.TestCase):

    def setUp(self):
        self.trimmer = trimmer

    def test_gc_content(self):
        self.assertEqual(self.trimmer.gc_content("AGCT"), 50)
        self.assertEqual(self.trimmer.gc_content("AATT"), 0)
        self.assertEqual(self.trimmer.gc_content("GGGCCC"), 100)

    def test_fastq_read_check(self):
        self.assertEqual(self.trimmer.fastq_read_check(
            ["Read123", "AAGGCCTT", "+", "ADGDFHFSH"], 8, 0, 50), True)
        self.assertEqual(self.trimmer.fastq_read_check(
            ["Read123", "AAGGCCTT", "+", "ADGDFHFSH"], 8, 0, 49), False)
        self.assertEqual(self.trimmer.fastq_read_check(
            ["Read123", "AAGGCCTT", "+", "ADGDFHFSH"], 9, 0, 50), False)

    def test_fastq_reader(self):
        parser_reads = list()
        test_reads = list()
        with open("test_reads.fastq", "r") as test_file:
            for line in test_file:
                test_reads.append(line.strip())
        with open("test_reads.fastq", "r") as test_file:
            for read in self.trimmer.fastq_reader(test_file):
                parser_reads.extend(read)
        self.assertEqual(parser_reads, test_reads)

    def test_trimmer(self):
        trimmer.trimmer(fastq_file="test_reads.fastq", output_base_name="test", min_length=7, gc_min=45, gc_max=50,
                        keep_filtered=True)
        with open("test_reads.fastq", "r") as trimmer_input, open("test_passed.fastq", "r") as passed, open(
                "test_failed.fastq", "r") as failed:
            input_reads = [line.strip() for line in trimmer_input]
            passed_reads = [line.strip() for line in passed]
            failed_reads = [line.strip() for line in failed]

            self.assertEqual(len(input_reads), len(passed_reads) + len(failed_reads))
            self.assertEqual(len(passed_reads) // 4, 3)


if __name__ == "__main__":
    unittest.main()
