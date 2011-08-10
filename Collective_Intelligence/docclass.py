# Document Filtering 
# Adapt to bioinformatics research from PubMed
# @ Lincoln Nguyen

from pysqlite2 import dbapi2 as sqlite

import re
import math

def sampletrain(cl):
    cl.train('Nobody owns the water.','good')
    cl.train('the quick rabbit jumps fences','good')
    cl.train('buy pharmaceuticals now','bad')
    cl.train('make quick money at the online casino','bad')
    cl.train('the quick brown fox jumps','good')
    
def getwords(doc):
  splitter=re.compile('\\W*')
  print doc
  # Split the words by non-alpha characters
  words=[s.lower() for s in splitter.split(doc) 
          if len(s)>2 and len(s)<20]
  
  # Return the unique set of words only
  return dict([(w,1) for w in words])
  
class classifier:

    def __init__(self,getfeatures,filename=None):
        
    # Counts of feature/category combinators in dictionary
        self.fc = {}
        # Counts of documents in each category
        self.cc = {}
        self.getfeatures = getfeatures

    # This function increases the count of a feature/category pair
    def incf(self, f, cat):
        count = self.fcount(f, cat)
        if count == 0:
            self.con.execute("insert into fc values ('%s', '%s', 1)" % (f, cat))

        else:
            self.con.execute(
                "update fc set count = %d where feature = '%s' and category = '%s'" % (count + 1, f, cat))

    # The number of times a feature has appeared in a category
    def fcount(self, f, cat):
        res = self.con.execute(
            'select count from fc where feature = "%s" and category = "%s"'
            %(f, cat)).fetchone()
        if res == None: return 0
        else: return float(res[0])

    # This function increases the count of a category
    def incc(self, cat):
        count = self.catcount(cat)
        if count == 0:
            self.con.execute("insert into cc values ('%s', 1)" % (cat))
        else:
            self.con.execute("update cc set count = %d where category = '%s;" % (count + 1, cat))

    # The number of items in a category
    def catcount(self, cat):
        res = self.con.execute('select count from cc where category = "%s"' % (cat)).fetchone()
        if res == None: return 0
        else: return float(res[0])
                                                                                              

    # The list of all categories
    def categories(self):
        cur = self.con.execute('select category from cc');
        return [d[0] for d in cur]

    # The total number of items
    def totalcount(self):
        res = self.con.execute('selecct sum(count) from cc').fetchone();
        if res == None : return 0
        return res[0]                                                              




    # This function takes an item(doc) and a classification. 
    # It uses getfeatures to break the item into separate features. 
    # It calls incf to increase the counts for this classification for every feature. 
    # Lastly, it increases the total count fo this classification
    def train(self, item, cat):
        features = self.getfeatures(item)
        # Increment the count for every feature with this category
        for f in features:
            self.incf(f, cat)

        # Increment the count for this category
        self.incc(cat)       
        self.con.commit     

    def fprob(self, f, cat):
        if self.catcount(cat) == 0: return 0
        # The total # of times this feature appeared in this
        # category divided by the total number of items in this category
        return self.fcount(f,cat)/self.catcount(cat)

    def weightedprob(self, f, cat, prf, weight = 1.0, ap = 0.5):
        # Calculate current probability
        basicprob = prf(f, cat)     # Probability of features given the category

        # Count the number of times this feature has appeared in all categories
        totals = sum([self.fcount(f,c) for c in self.categories()])

        # Calculate the weighted average
        bp = ((weight * ap) + (totals * basicprob)) / (weight + totals)
        return bp  

class naivebayes(classifier):  # subclass of classifier class above
    def __init__(self,getfeatures):
        classifier.__init__(self,getfeatures)   # Set up thresholds and add new instance var to classifier
        self.thresholds = {}
        
    def docprob(self, item, cat):
        features = self.getfeatures(item)    # get a dictionary from the getwords f

        # Multiply the probabilities of all the features together
        p = 1
        for f in features: p*= self.weightedprob(f, cat, self.fprob) #self used to connect method
        return p                             

    def prob(self, item, cat):
        catprob = self.catcount(cat) / self.totalcount() # probability of category
        docprob = self.docprob(item, cat) # probability of document
        return docprob * catprob      

    # Simple methods to set and get the values returning 1.0 as default
    def setthreshold(self, cat, t):
        self.thresholds[cat] = t
    
    def getthreshold(self,cat):
        if cat not in self.thresholds: return 1.0
        return self.thresholds[cat]

    def classify(self, item, default = None):
        probs = {}
        # Find the category with the highest probability
        max = 0.0
        for cat in self.categories():    # for loop category in     
            probs[cat] = self.prob(item, cat)
            if probs[cat] >max:
                max = probs[cat]
                best = cat    

        # Make sure the probability exceeds threshold*next best
        for cat in probs:
          if cat==best: continue
          if probs[cat]*self.getthreshold(best)>probs[best]: return default
        return best

## Fisher method

class fisherclassifier(classifier):

    def setdb(self, dbfile):
        self.con = sqlite.connect(dbfile) # function inside the dbapi
        self.con.execute('create table if not exists fc(feature, category, count)')
        self.con.execute('create table if not exists cc(category, count)')
        
    def cprob(self, f, cat):
        # The frequency fo this feature in this category
        clf = self.fprob(f, cat)
        if clf == 0: return 0

        # Frequency of this feature in all categories
        freqsum = sum([self.fprob(f, c) for c in self.categories()])

        # The probability is the frequency in this category divided by 
        # the overall frequency
        p = clf/ (freqsum)

        return p
            
    def fisherprob(self, item, cat):
        # Multiply all the probabilties together
        p = 1
        features = self.getfeatures(item)
        for f in features:
            p *= (self.weightedprob(f, cat, self.cprob))

        # Take the natural log and multiply by -2
        fscore = -2 * math.log(p)

        # Use the inverse chi2 function to get a probability
        return self.invchi2(fscore, len(features) * 2)                                 

    def invchi2(self, chi, df):
        m = chi / 2.0
        sum = term = math.exp(-m)
        for i in range(1, df//2):
            term *= m / i
            sum += term
        return min(sum, 1.0)   

    # Init method with another variable to store cutoffs
    def __init__(self, getfeatures):
        classifier.__init__(self, getfeatures)
        self.minimums = {}                   

    # Methods for getting and setting these cutoff values with a default val = 0
    def setminimum(self, cat, min):
        self.minimums[cat] = min

    def getminimum(self, cat):
        if cat not in self.minimums: return 0
        return self.minimums[cat]

    # Method to calculate the probs for each category and determine best result
    # that exceeds the minimum
    def classify(self, item, default=None):
        # Loop through looking for the best result
        best = default
        max = 0.0
        for c in self.categories():
          p = self.fisherprob(item, c)
          # Make sure it exceeds its minimum
          if p > self.getminimum(c) and p > max:
            best = c
            max = p
        return best                                                           
