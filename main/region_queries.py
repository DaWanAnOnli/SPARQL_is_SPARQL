from SPARQLWrapper import SPARQLWrapper, JSON

def region_queries(id, sparql):
    # print(type(id))
    # print(id)
    final_result = dict()

    # Set the SPARQL query
    sparql.setQuery("""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX v: <http://myairports.com/vocab#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX : <http://myairports.com/data/>

    SELECT ?region ?label ?hasID ?hasLocalCode ?country ?labelCountry
    WHERE {
        ?region rdf:type :region .
        OPTIONAL { ?region rdfs:label ?label . }
        OPTIONAL { ?region v:hasID ?hasID . }
        OPTIONAL { ?region v:hasLocalCode ?hasLocalCode . }
        OPTIONAL { ?region v:partOf ?country . }
        OPTIONAL {?country a v:country ;
                            rdfs:label ?labelCountry.

        }

        FILTER(isIRI(?country))
        FILTER(?region = :""" + id + """)
    }
    LIMIT 100
    """)

    # Set the output format to JSON
    sparql.setReturnFormat(JSON)

    # Execute the query
    results = sparql.query().convert()

    # print(type(results))


    if (len(results["results"]["bindings"]) == 0):
        return {"message": "No results found for regions."}

    result = results["results"]["bindings"][0]

    for key in result.keys():
        final_result[key] = result[key]["value"]
    
    return(final_result)