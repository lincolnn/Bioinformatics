# This is an extension of the 16_1_6 module
# GATGACGGTGT is an adaptor sequence in FASTQ format
# Look for the sequence anywhere in the reads 

from Bio import SeqIO

def trim_adaptors(records, adaptor, min_len):
    """Trims perfect adaptor sequences.

    This is a generator function, the records argument should
    be a list or iterator returning SeqRecord objects.
    """

    len_adaptor = len(adaptor) # cache for later
    for record in records:
        len_record = len(record) # cache this for later
        if len(record) < min_len:
            # add minimum length
            continue            
        index = record.seq.find(adaptor)
        if index == -1:
            # adaptor not found, so this won't trim
            yield record
        else:
            # trim off the adaptor
            yield record[index+len_adaptor:]

original_reads = SeqIO.parse("SRR020192.fastq", "fastq")
trimmed_reads = trim_adaptors(original_reads, "GATGACGGTGT", 100)
count = SeqIO.write(trimmed_reads, "trimmed.fastq", "fastq")
print "Saved %i reads" % count                        

