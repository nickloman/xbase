from Bio import SeqIO
import sys
import cProfile

def go():
	SeqIO.write(
		SeqIO.parse(open(sys.argv[1]), "fastq-illumina"),
		sys.stdout,
		"fastq"
	)


# cProfile.run('go()')
go()

