import unittest
from os import remove
import trimmer


class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class TestTrimmer(unittest.TestCase):

    def setUp(self):
        self.trimmer = trimmer
        self.test_read1 = self.trimmer.FastqRead(["SHUE228PPSH322", "ATGCATGCAT", "+", "IIIIIHHHHH"])
        self.test_read2 = self.trimmer.FastqRead(["SHUE228PPSH322", "ATGCATGCAT", "+", "HHHHHI!!!!"])
        self.test_read3 = self.trimmer.FastqRead(["SHUE228PPSH322", "ATGCATGCATGCATGC", "+", "05:???::005:HHHH"])
        self.args1 = Namespace(CROP=None, HEADCROP=None, LEADING=None, TRAILING=None, SLIDINGWINDOW=None,
                               fastq_file="test_reads.fastq", output_base_name="test", min_length=7, gc_bounds=[45, 50],
                               keep_filtered=True)
        self.args2 = Namespace(CROP=12, HEADCROP=2, LEADING=26, TRAILING=30, SLIDINGWINDOW=[50, 30],
                         fastq_file="test_reads.fastq", output_base_name="test", min_length=7, gc_bounds=[45, 50],
                         keep_filtered=True)

    def test_gc_content(self):
        self.assertEqual(self.trimmer.gc_content("AGCT"), 50)
        self.assertEqual(self.trimmer.gc_content("AATT"), 0)
        self.assertEqual(self.trimmer.gc_content("GGGCCC"), 100)

    def test_apply_filters(self):
        self.assertEqual(self.trimmer.apply_filters(
            "AAGGCCTT", 8, 0, 50), True)
        self.assertEqual(self.trimmer.apply_filters(
            "AAGGCCTT", 8, 0, 49), False)
        self.assertEqual(self.trimmer.apply_filters(
            "AAGGCCTT", 9, 0, 50), False)

    def test_fastq_reader(self):
        parser_reads = list()
        test_reads = list()
        with open("test_reads.fastq", "r") as test_file:
            for line in test_file:
                test_reads.append(line.strip())
        with open("test_reads.fastq", "r") as test_file:
            for read in self.trimmer.fastq_reader(test_file):
                parser_reads.extend(read.read)
        self.assertEqual(parser_reads, test_reads)

    def test_trimmer(self):
        trimmer.main(self.args1)
        with open("test_reads.fastq", "r") as trimmer_input, open("test_passed.fastq", "r") as passed, open(
                "test_failed.fastq", "r") as failed:
            input_reads = [line.strip() for line in trimmer_input]
            passed_reads = [line.strip() for line in passed]
            failed_reads = [line.strip() for line in failed]
            remove("test_passed.fastq")
            remove("test_failed.fastq")
            self.assertEqual(len(input_reads), len(passed_reads) + len(failed_reads))
            self.assertEqual(len(passed_reads) // 4, 3)

    def test_crop(self):
        self.assertEqual(self.trimmer.crop(self.test_read1, 5).read, ["SHUE228PPSH322", "ATGCA", "+", "IIIII"])
        self.assertEqual(self.trimmer.crop(self.test_read1, 10), None)

    def test_headcrop(self):
        self.assertEqual(self.trimmer.headcrop(self.test_read1, 5).read, ["SHUE228PPSH322", "TGCAT", "+", "HHHHH"])
        self.assertEqual(self.trimmer.headcrop(self.test_read1, 10), None)

    def test_leading_cut(self):
        self.assertEqual(self.trimmer.leading_cut(self.test_read2, 40).read, ["SHUE228PPSH322", "TGCAT", "+", "I!!!!"])
        self.assertEqual(self.trimmer.leading_cut(self.test_read2, 41), None)

    def test_trailing_cut(self):
        self.assertEqual(self.trimmer.trailing_cut(self.test_read2, 40).read, ["SHUE228PPSH322", "ATGCAT", "+", "HHHHHI"])
        self.assertEqual(self.trimmer.trailing_cut(self.test_read2, 41), None)

    def test_sliding_window(self):
        self.assertEqual(self.trimmer.sliding_window(self.test_read3, 4, 20).read, ["SHUE228PPSH322", "ATGCATGC", "+", "05:???::"])
        self.assertEqual(self.trimmer.sliding_window(self.test_read1, 4, 20).read, self.test_read1.read)
        self.assertEqual(self.trimmer.sliding_window(self.test_read3, 4, 30), None)

    def test_FastqRead(self):
        self.assertEqual(self.test_read1[::-1].read, ["SHUE228PPSH322", "TACGTACGTA", "+", "HHHHHIIIII"])
        self.assertEqual(self.test_read1.phred_quality, [40, 40, 40, 40, 40, 39, 39, 39, 39, 39])
        self.assertEqual(len(self.test_read1), 10)

    def test_apply_trimmers(self):
        self.assertEqual(self.trimmer.apply_trimmers(self.test_read3, self.args2).read, ["SHUE228PPSH322", "CAT", "+", "???"] )
        self.assertEqual(self.trimmer.apply_trimmers(self.test_read3, self.args1).read, self.test_read3.read)


if __name__ == "__main__":
    unittest.main()
