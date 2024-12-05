from SPARQLWrapper import SPARQLWrapper, JSON

def search_queries(id, sparql):
    print(type(id))
    print(id)
    final_result = dict()

    # Set the SPARQL query
    sparql.setQuery('''
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX : <http://myairports.com/data/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX v: <http://myairports.com/data/>

    SELECT * WHERE {{
        {
            ?airport rdf:type :airport;
                    rdfs:label ?airport_label .
            FILTER(CONTAINS(LCASE(?airport_label), "''' + id + '''"))
        }
        UNION
        { 
            ?region rdf:type :region;
                    rdfs:label ?region_label .
            BIND(
                IF(
                    CONTAINS(LCASE(?region_label), "unassigned"),
            		SUBSTR(STR(?region), 28),
                    ?region_label
                ) AS ?region_label_result
            )
            FILTER(CONTAINS(LCASE(?region_label_result), "''' + id + '''"))

    }
        UNION
        {
            ?navaid rdf:type :navaid;
                    rdfs:label ?navaid_label .
            FILTER(CONTAINS(LCASE(?navaid_label), "''' + id + '''"))
        }
        UNION
        {
            ?runway rdf:type :Runway;
                    rdfs:label ?runway_label .
            FILTER(CONTAINS(LCASE(?runway_label), "''' + id + '''"))
        }
        UNION
        {
            ?country rdf:type v:country;
                    rdfs:label ?country_label .
            ?code v:isoHasLabel ?label2 .
            FILTER(?country = ?code) .
            FILTER(CONTAINS(LCASE(?country_label), "''' + id + '''"))
        }
    }}
    ''')

    # Set the output format to JSON
    sparql.setReturnFormat(JSON)

    # Execute the query
    results = sparql.query().convert()

    # print(type(results))

    if len(results["results"]["bindings"]) == 0:
        return {"message": "No results found for the given search keyword."}

    # Initialize lists for results
    airports = []
    airport_labels = []
    regions = []
    region_labels = []
    navaids = []
    navaid_labels = []
    runways = []
    runway_labels = []
    countries = []
    country_labels = []

    # Process each result row
    for result in results["results"]["bindings"]:
        if "airport" in result:
            airports.append(result["airport"]["value"])
            airport_labels.append(result["airport_label"]["value"])
        if "region" in result:
            regions.append(result["region"]["value"])
            region_labels.append(result["region_label_result"]["value"])
        if "navaid" in result:
            navaids.append(result["navaid"]["value"])
            navaid_labels.append(result["navaid_label"]["value"])
        if "runway" in result:
            runways.append(result["runway"]["value"])
            runway_labels.append(result["runway_label"]["value"])
        if "country" in result:
            # iso_country = result["country"]["value"]
            countries.append(result["country"]["value"])
            country_labels.append(result["country_label"]["value"])
        if "label2" in result:
            if result["country_label"]["value"] != result["label2"]["value"]:
                countries.append(result["code"]["value"])
                country_labels.append(result["label2"]["value"])

    # Populate the final result dictionary
    final_result["airports"] = airports
    final_result["airport_labels"] = airport_labels
    final_result["regions"] = regions
    final_result["region_labels"] = region_labels
    final_result["navaids"] = navaids
    final_result["navaid_labels"] = navaid_labels
    final_result["runways"] = runways
    final_result["runway_labels"] = runway_labels
    final_result["countries"] = countries
    final_result["country_labels"] = country_labels

    return final_result
