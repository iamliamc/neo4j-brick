import rdflib
g = rdflib.Graph()
g.load('http://dbpedia.org/resource/Semantic_Web')

for st, pt, ot in g:
    import pdb; pdb.set_trace()
