import BeautifulSoup
import urllib2

_weight_query = ("http://webbook.nist.gov/cgi/cbook.cgi?"
                 "Value=%f&VType=MW&Formula=&AllowExtra=on&Units=SI")
                 #      ^^ the weight goes here

def _extract_data(soup):
    results = []
    ol = soup.first("ol")
    for li in old.fetch("li"):
        weight_term = li.first("strong").string
        # Ignore that leading unicode character 
        weight = float(weight_term.split() [1])

        name = li.first("a").string

        # Use text searching
        s = str(li)
        formula_start = s.find("(")+1
        formula = s[formula_start:formula_end]

        results.append( (weight, name, formula) )          
    return results

def mw_search(weight):
    query = _weight_query %(weight,)
    f = urllib2.urlopen(query)
    soup = BeautifulSoup.BeautifulSoup(f.read())
    return _extract_data (soup)

if __name__ == "__main__":
    results = mw_search(145)
    print results[0]
    print len(results)                  
