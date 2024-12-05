from SPARQLWrapper import SPARQLWrapper, JSON

def airport_queries(id, sparql):
    # print(type(id))
    # print(id)
    final_result = dict()

    # Set the SPARQL query
    sparql.setQuery("""
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX v: <http://myairports.com/vocab#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://myairports.com/data/>

select distinct * where {
    :""" + id + """ rdf:type ?type .
    

    
    optional{:""" + id + """ rdfs:label ?name;}
    optional{:""" + id + """ v:ident ?ident;}
    optional{:""" + id + """ v:iata_code ?iata_code;}
    optional{:""" + id + """ v:gps_code ?gps_code;}
    optional{:""" + id + """ v:local_code ?local_code;}
    optional{:""" + id + """ v:scheduled_service ?scheduled_service;}
    optional{:""" + id + """ v:municipality ?municipality .
    		 ?municipality rdfs:label ?municipality_label .}
    optional{:""" + id + """ v:region ?iso_region .
    		 ?iso_region rdfs:label ?region_label .}
    optional{:""" + id + """ v:country ?iso_country .
    		 ?iso_country rdfs:label ?country_label . }
    optional{:""" + id + """ v:continent ?continent;}
    optional{:""" + id + """ geo:lat ?latitude_deg;}
    optional{:""" + id + """ geo:long ?longitude_deg;}
    optional{:""" + id + """ geo:alt ?elevation_ft .}
        
    
    filter(
    ?type != :airport
    )
   
    
}
    """)

    # Set the output format to JSON
    sparql.setReturnFormat(JSON)

    # Execute the query
    results = sparql.query().convert()

    # print(type(results))


    if (len(results["results"]["bindings"]) == 0):
        return {"message": "No results found for airports."}

    result = results["results"]["bindings"][0]

    for key in result.keys():
        final_result[key] = result[key]["value"]



###############################################################

    sparql.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX v: <http://myairports.com/vocab#>
    PREFIX : <http://myairports.com/data/>

    select distinct * where {
        ?runway v:partOf :""" + id + """;
        rdfs:label ?runway_label .
        
        }  order by ?runway_label
    """)

    # Set the output format to JSON
    sparql.setReturnFormat(JSON)

    # Execute the query
    results = sparql.query().convert()


    runways = []
    runway_labels = []

    for result in results["results"]["bindings"]:
        runways.append(result["runway"]["value"])
        runway_labels.append(result["runway_label"]["value"])
    
    final_result["runways"] = runways
    final_result["runway_labels"] = runway_labels

    ##############################################################

    sparql.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX v: <http://myairports.com/vocab#>
    PREFIX : <http://myairports.com/data/>

    select distinct ?navaid ?navaid_label ?navaid_ident where {
        :""" + id + """ v:ident ?airport_ident .
        ?navaid v:icao_code ?airport_ident;
                rdfs:label ?navaid_label;
                v:ident ?navaid_ident .
    }  order by ?navaid_label
    """)

    # Set the output format to JSON
    sparql.setReturnFormat(JSON)

    # Execute the query
    results = sparql.query().convert()

    navaids = []
    navaid_labels = []
    navaid_idents = []

    for result in results["results"]["bindings"]:
        navaids.append(result["navaid"]["value"])
        navaid_labels.append(result["navaid_label"]["value"])
        navaid_idents.append(result["navaid_ident"]["value"])

    final_result["navaids"] = navaids
    final_result["navaid_labels"] = navaid_labels
    final_result["navaid_idents"] = navaid_idents

    return final_result


def get_all_airports(sparql):
    """
    Fetches all airports with their corresponding country names.

    Args:
        sparql: The SPARQLWrapper object for querying the dataset.

    Returns:
        A dictionary with:
        - airports: A list of dictionaries containing airport details:
            - id: Airport ID
            - label: Airport name
            - country: Country name
    """
    final_result = {"airports": []}

    # Set the SPARQL query
    sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX va: <http://myairports.com/vocab#>

        SELECT DISTINCT ?airportId ?airport ?label1 WHERE {
            ?airportId rdfs:label ?airport .
            ?airportId va:country ?isoCode .
            ?isoCode rdfs:label ?label1 .
        }
    """)

    sparql.setReturnFormat(JSON)

    # Execute the query
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        airport_id = result["airportId"]["value"]
        airport_label = result["airport"]["value"]
        country_name = result["label1"]["value"]

        final_result["airports"].append({
            "id": airport_id.split("/")[-1],  # Extract only the last part of the URI
            "label": airport_label,
            "country": country_name,
        })

    return final_result













    



