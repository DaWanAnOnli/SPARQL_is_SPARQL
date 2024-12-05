from SPARQLWrapper import SPARQLWrapper, JSON

def navaid_queries(id, sparql):
    # print(type(id))
    # print(id)
    final_result = dict()

    # Set the SPARQL query
    sparql.setQuery("""
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX v: <http://myairports.com/vocab#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX c: <http://example.org/countries/> 
PREFIX : <http://myairports.com/data/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

select * where {
	?navaid rdf:type :navaid.
    optional{?navaid rdfs:label ?name.}
    optional{?navaid rdf:type ?type.}
    optional{?navaid v:ident ?ident.}
    optional{?navaid v:usage_type ?usage_type.}
    optional{?navaid v:power_type ?power.}
        optional{?navaid v:icao_code ?airport_id.
        	?airport rdf:type :airport;
            		 v:ident ?airport_id;
                     rdfs:label ?airport_label.}
    optional{?navaid v:magnetic_var ?magnetic_variation_deg.}
    optional{?navaid v:country ?iso_country.}
    optional{?navaid geo:long ?longitude_deg.}
    optional{?navaid geo:alt ?elevation_ft.}
    optional{?navaid geo:lat ?latitude_deg.}
    optional{?navaid v:frequency ?frequency_khz.}
                    
    FILTER(?navaid = :""" + id + """ && ?type != :navaid)
} limit 100

    
    """)

    # Set the output format to JSON
    sparql.setReturnFormat(JSON)

    # Execute the query
    results = sparql.query().convert()

    # print(type(results))


    if (len(results["results"]["bindings"]) == 0):
        return {"message": "No results found for navaids."}

    result = results["results"]["bindings"][0]

    for key in result.keys():
        final_result[key] = result[key]["value"]
    
    return(final_result)













    



