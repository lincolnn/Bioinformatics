# @date: 7/2/11
# @author: Lincoln Nguyen 
# This script produces randomised genomes. Use this product as a sample set for statistical analysis. 
# Uses big for loop and writes out the records one by one

import random
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO

# SeqIO is an object, read the file and put into a string
original_rec = SeqIO.read("NC_005816.gb","genbank")

handle = open("shuffled.fasta", "w")
for i in range(30):     
    nuc_list = list(original_rec.seq)       #return a list when looping through 
    random.shuffle(nuc_list)    
    # Construct a new SeqRecord with a new Seq object using this shuffled list (nuc_list).  
    shuffled_rec = SeqRecord(Seq("".join(nuc_list), original_rec.seq.alphabet),  
                            id = "Shuffled%i" % (i + 1), 
                            description = "Based on %s" % original_rec.id)
    handle.write(shuffled_rec.format("fasta"))
handle.close()     
