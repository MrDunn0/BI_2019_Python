        Description

This is a simple copy of Trimmomatiс for trimming and filtering fastq reads.

         Requirements

Python 3
        
        Arguments

--CROP - the number of bases to keep, from the start of the read
--HEADCROP - the number of bases to remove from the start of the read
--LEADING - Quality threshold for bases at the beginning of a read. 
--TRAILING - Quality threshold for bases at the end of a read
--SLIDINGWINDOW <window_size> <required_quality>
        window_size - number of bases to average across 
        required_quality - average quality required
        
        Warning: In the current implementation, the SLIDINGWINDOW evaluates new N nucleotides each time.

--min_length Minimal length of reads to be selected. If not specified, then reads of any length will pass the filter.

--gc_bounds 
The range of quantitative content of GC. First and second values are min and max respectively.If the only one value is specified, then reads with greater or equal value will be selected.

--keep_filtered(flag) - Reads that do not pass the filter will be written to a separate file.

--output_base_name - common prefix for passed and failed reads.

        Usage

python3 trimmer.py --HEADCROP 20 --LEADING 30 --TRAILING 30 --SLIDINGWINDOW 5 30 --min_length 100 --gc_bounds 40 50 --output_base_name any_prefix --keep_filtered my_reads.fastq



        




         
