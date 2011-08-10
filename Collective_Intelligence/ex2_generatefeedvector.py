# This module counts the words in a feed. It gets the title, links, and entries from RSS and Atom feeds.
# From Collective Intelligence on data clustering(unsupervised learning)
# Bioinformatics Use Case: Finds groups of genes that exhibit similar behavior indicating
# they response to treatment in the same way. Use this for Pubmed library. 

import feedparser
import re

# Returns title and a dictionary of word counts for RSS feed
def getwordcounts(url):
    # Parse the feed using feedparser library and parse function
    d = feedparser.parse(url)
    wc = {}

    # Loop over all the entries, using for loop
    for e in d.entries:
        if 'summary' in e: summary = e.summary
        else: summary = e.description

        # Extract a list of words
        words = getwords(e.title + ' ' + summary)
        for word in words:
            wc.setdefault(word, 0)
            wc[word] += 1
        return d.feed.title, wc            

def getwords(html):
    # Remove the HTML tags
    txt = re.compile(r'<[^>]+>').sub('', html)

    # Split the words by all non alpha characters
    words = re.compile(r'[^A-Z^a-z]+').split(txt)

    # Convert to lowercase
    return [word.lower() for word in words if word! = ''] 

    # apcount shows number of blogs each word appears
    apcount = {}
    for feedurl in file('pubmedfeeds.txt'):           
        title, wc = getwordcounts(feedurl)
        wordcounts[title] = wc
        for word, count in wc.items():
            apcount.setdefault(word, 0)
            if count > 1:
                apcount[word] +=1

    wordlist = []
    for w,bc in apcount.items():
        frac = float(bc)/len(feedlist)
        if frac > 0.1 and frac < 0.5: wordlist.append(w)

    out = file('pubmeddata.txt', 'w')
    out.write('Blog')
    for word in wordlists: out.write('\t%s' % word)
    out.write('\n')
    for blog,wc in wordcounts.items():
        out.write(blog)                        
        for word in wordlist:
            if word in wc: out.write('\t%d' % wc[word])
            else: out.write('\t0')
        out.write('\n')            
