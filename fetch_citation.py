import random

#get a list of lines from txt
def read_file(fname):
    with open(fname) as infile:
        citation_list = [line.rstrip("\n") for line in infile]
    return citation_list
#pick a quote randomly in the list
def pick_citation(citation_list):
    i = random.randint(0,len(citation_list)-1)
    citation = citation_list[i]
    return citation
#return quote from txt
def fetch_citation():
    citation_list = read_file("assets/citations.txt")
    citation = pick_citation(citation_list)
    return citation
