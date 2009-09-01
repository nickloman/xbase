#!/usr/bin/python

"""
trim_reads.py

Usage: trim_reads.py <fastq_file> <trim length>

I.e. trim_reads.py in.fq 30 would trim each base to 30 characters. Output is to stdout.
"""

if __name__ == '__main__':
    import sys
    from Bio import SeqIO

    try:
        FILE_NAME = sys.argv[1]
        TRIM_LENGTH = int(sys.argv[2])
    except IndexError:
        print "Usage: trim_reads.py <fastq_file> <trim length>"
        raise SystemExit

    for rec in SeqIO.parse(open(FILE_NAME), "fastq"):
	    rec = rec[0:TRIM_LENGTH]
	    SeqIO.write([rec], sys.stdout, "fastq")

