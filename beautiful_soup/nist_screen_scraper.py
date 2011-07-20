import urllib2

_weight_query = ("http://webbook.nist.gov/cgi/cbook.cgi?"
                 "Value=%f&VType=MW&Formula=&AllowExtra=on&Units=SI")
                 #      ^^ the weight goes here

def _extract_data(infile):
    results = []
    for line in infile:
        if not line.startswith("<li><strong>"):
            continue
        # These are the lines that contain data we need

        # The weight is between the ';' and the '<'
        # <li><strong>&nbsp; 144.86 </strong>
        weight_start = line.index(";")+1
        weight_end = line.index("<", weight_start)
        weight = float(line[weight_start:weight_end])

        # The chamical name is between the 'SI">' and the next '<'
        # =SI">AsCl2</a></li>
        name_start = line.index('SI">')+4
        name_end = line.index('<', name_start)
        name = line[name_start:name_end]

        # The chemical formula (in HTML) is between the parentheses
        formula_start = line.index("(", named_end) + 1
        formula_end = line.index(")", formula_start)
        formula = line[formula_start:formula_end]

        results.append( (weight, name, formular) )
        
    return results

def mw_search(weight):
    query = _weight_query % (weight,)
    f = urllib2.urlopen (query)
    return _extract_data (f)

if ___name__ == "__main__":
    results = mw_search(145)
    print results[0]
    print len(results)              
