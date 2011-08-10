# Normalize the data by making everything uppercase. 
# Example 16.1.3 in Biopython Tutorial

from Bio import SeqIO

records = (rec.upper() for rec in SeqIO,parse("mixed.fas", "fasta")) # Python generator expression 
count = SeqIO.write(records, "upper.fas", "fasta")
print "Converted %i records to upper case" % count
