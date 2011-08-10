# Simple quality filtering module for FASTQ files
# SeqRecord shows per letter annotation, in the letter_annotation dictionary
# as list, tuple, or string

from Bio import SeqIO
count = 0
for rec in SeqIO.parse("SRR020192.fastq", "fastq"):
    count += 1
print "%i reads" % count

# Simple filtering for a minimum PHRED quality of 20:

from Bio import SeqIO
good_reads = (rec for rec in \
                SeqIO.parse("SRR020192.fastq", "fastq") \
                if min(rec.letter_annotations["phred_quality"]) >= 20)
count = SeqIO.write(good_reads, "good_quality.fastq", "fastq")
print "Saved %i reads" % count                
    
