from SPARQLWrapper import SPARQLWrapper, JSON

# GraphDB SPARQL endpoint
# punya joel
sparql = SPARQLWrapper("http://34.50.87.161:7200/repositories/airports")

# punya adrial
# sparql = SPARQLWrapper("http://DESKTOP-CMK0990:7200/repositories/airport")
final_result=dict()
# Set the SPARQL query
id = "Dubai_Emirate"
print(type(id))
sparql.setQuery("""
select * where {
    ?s ?p ?o .
} limit 100
""")


# Set the output format to JSON
sparql.setReturnFormat(JSON)

# Execute the query
results = sparql.query().convert()

print(type(results))


if (len(results["results"]["bindings"]) == 0):
    raise ValueError

result = results["results"]["bindings"][0]

for key in result.keys():
    final_result[key] = result[key]["value"]

print(final_result)





