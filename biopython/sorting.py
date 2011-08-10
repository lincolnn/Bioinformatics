# Sort a sequence file by length

from Bio import SeqIO

# Get the lengths and ids and sort each on length
# Scan through files using Bio.SeqIO.pase() in for loop
# recording identifiers and their lengths in list of tuples
# Then sort the list to get them in length order
len_and_ids = sorted((len(rec), rec.id) for rec in \
                    SeqIO.parse("ls_orchid.fasta","fasta"))

ids = reversed([id for (length, id) in len_and_ids])

# Discard the lengths
del len_and_ids # Use this to free memory

record_index = SeqIO.index("ls_orchid.fasta", "fasta")
records = (record_index[id] for id in ids)

# Write into fasta file
SeqIO.write(records, "sorted.fasta", "fasta")

# Output to a file type other than FASTA
handle = open("sorted.fasta", "w")

for id in ids:
    handle.write(record_index.get_raw(id))
handle.close()                        
