from SPARQLWrapper import SPARQLWrapper, JSON

def runway_queries(id, sparql):
    # print(type(id))
    # print(id)
    final_result = dict()

    # Set the SPARQL query
    sparql.setQuery("""
PREFIX v: <http://myairports.com/vocab#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://myairports.com/data/>

SELECT * WHERE {
    ?runway rdf:type :Runway;
    OPTIONAL{?runway rdfs:label ?label}
    OPTIONAL{?runway v:partOf ?airport .
    ?airport rdfs:label ?airport_label}
    OPTIONAL{?runway v:length ?length_ft}
    OPTIONAL{?runway v:width ?width_ft}
    OPTIONAL{?runway v:surface ?surface}
    OPTIONAL{?runway v:isLighted ?isLighted}
    OPTIONAL{?runway v:isClosed ?isClosed}
    OPTIONAL{?runway v:leID ?leID}
    FILTER(?runway = :""" + id + """ )
} limit 100
    """)

    # Set the output format to JSON
    sparql.setReturnFormat(JSON)

    # Execute the query
    results = sparql.query().convert()

    # print(type(results))


    if (len(results["results"]["bindings"]) == 0):
        return {"message": "No results found for runways."}

    result = results["results"]["bindings"][0]

    for key in result.keys():
        final_result[key] = result[key]["value"]
    
    return(final_result)