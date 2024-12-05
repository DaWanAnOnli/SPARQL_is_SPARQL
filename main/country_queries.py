from django.shortcuts import render
import requests
from SPARQLWrapper import SPARQLWrapper, JSON
from SPARQLWrapper import SPARQLWrapper, JSON

def get_flag(iso_country, wikidata_sparql):
    # Define the SPARQL endpoint for Wikidata

    # SPARQL query to get the flag image URL for Brunei using its ISO 2-digit code
    query = '''
    SELECT ?flag
    WHERE {
      ?country wdt:P31 wd:Q6256;  # Instance of country (Q6256)
               wdt:P297 "''' + iso_country + '''";  # ISO 2-digit code for the country
               wdt:P41 ?flag.  # Flag image (P41)
    }
    '''

    # Send the query to Wikidata's SPARQL endpoint
    response = requests.get(wikidata_sparql, params={'query': query, 'format': 'json'})

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()  # Parse the response as JSON
        if data['results']['bindings']:
            flag_url = data['results']['bindings'][0]['flag']['value']
        else:
            flag_url = None
    else:
        flag_url = None

    return flag_url

def cotw_queries(country_code, sparql):
    final_result = dict()

    # SPARQL query to retrieve country data
    sparql.setQuery(f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX c: <http://example.org/countries/>
    PREFIX v: <http://myairports.com/data/>
    PREFIX va: <http://myairports.com/vocab#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    select * where {{
        ?code v:isoHasLabel ?label2 .

        ?country v:isPartOfRegion ?type .

        OPTIONAL {{?country v:isPartOfRegion ?Region . }} 
        OPTIONAL {{?country v:hasPopulation ?Population . }} 
        OPTIONAL {{?country v:hasAreaInSquareMiles ?AreaInSquareMiles . }}
        OPTIONAL {{?country v:hasPopulationDensityPerSquareMiles ?PopulationDensityPerSquareMiles . }}
        OPTIONAL {{?country v:hasCoastlineRatio ?CoastlineRatio . }}
        OPTIONAL {{?country v:hasNetMigration ?NetMigration . }}
        OPTIONAL {{?country v:hasInfantMortality ?InfantMortality . }}
        OPTIONAL {{?country v:hasGDPInUSD ?GDPInUSD . }}
        OPTIONAL {{?country v:hasLiteracyRate ?LiteracyRate . }}
        OPTIONAL {{?country v:hasPhones ?Phones . }}
        OPTIONAL {{?country v:arablePercentage ?arablePercentage . }}
        OPTIONAL {{?country v:cropsPercentage ?cropsPercentage . }}
        OPTIONAL {{?country v:othersPercentage ?othersPercentage . }}
        OPTIONAL {{?country v:hasClimate ?Climate . }}
        OPTIONAL {{?country v:hasBirthrate ?Birthrate . }}
        OPTIONAL {{?country v:hasDeathrate ?Deathrate . }}
        OPTIONAL {{?country v:hasAgricultureRatio ?AgricultureRatio . }}
        OPTIONAL {{?country v:hasIndustryRatio ?IndustryRatio . }}
        OPTIONAL {{?country v:hasServiceRatio ?ServiceRatio . }}
        OPTIONAL {{?country v:label ?label . }}

        FILTER(?code = v:{country_code}).
        FILTER(?label = CONCAT(?label2, " ")).
        
        }}
    """)

    # Set the output format to JSON
    sparql.setReturnFormat(JSON)

    # Execute the query
    results = sparql.query().convert()
    # print(results)

    if len(results["results"]["bindings"]) == 0:
        return {"message": "No results found for country ID: {country_code}."}

    # Extract and store results
    result = results["results"]["bindings"][0]
    for key in result.keys():
        final_result[key] = result[key]["value"]




    ##########################################################################

    sparql.setQuery(f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX v: <http://myairports.com/data/>
    PREFIX va: <http://myairports.com/vocab#>
    PREFIX c: <http://example.org/countries/>

    select distinct * where {{
        ?airportId rdfs:label ?airport .
        ?airportId va:country ?isoCountry .
        
        ?code rdfs:label ?countryLabel2 .
        ?code va:partOf ?continentCode . 
        
        ?country v:label ?countryLabel1 . 
        
        FILTER(?code = v:{country_code}).
        FILTER(?isoCountry = v:{country_code}).
        FILTER(?countryLabel1 = (CONCAT(?countryLabel2, " "))).
        FILTER(isLITERAL(?continentCode)).
    
            }}
    """)

    sparql.setReturnFormat(JSON)

    # Execute the query
    results = sparql.query().convert()

    airports = []
    airports_labels = []

    for result in results["results"]["bindings"]:
        airports.append(result["airportId"]["value"])
        airports_labels.append(result["airport"]["value"])

    final_result["airports"] = airports
    final_result["airports_labels"] = airports_labels


    ##########################################################################

    sparql.setQuery(f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX v: <http://myairports.com/data/>
    PREFIX va: <http://myairports.com/vocab#>
    PREFIX c: <http://example.org/countries/>

    select * where {{
        ?regionId va:partOf ?isoCountry.
        ?regionId rdfs:label ?regionName.
        ?regionId va:hasLocalCode ?code.
        
        FILTER(?isoCountry = v:{country_code})
    }}
    """)

    sparql.setReturnFormat(JSON)

    # Execute the query
    results = sparql.query().convert()

    regions_contained = []
    regions_contained_labels = []

    for result in results["results"]["bindings"]:
        regions_contained.append(result["regionId"]["value"])
        regions_contained_labels.append(result["regionName"]["value"])

    final_result["regions_contained"] = regions_contained
    final_result["regions_contained_labels"] = regions_contained_labels

    # print(final_result['regions_contained'])
    

    return final_result


def get_all_countries(sparql):
    final_result = dict()

    sparql.setQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX c: <http://example.org/countries/>
        PREFIX v: <http://myairports.com/data/>
        PREFIX va: <http://myairports.com/vocab#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        select * where {
            ?code v:isoHasLabel ?label .
            FILTER(STRSTARTS(STR(?code), STR(v:))) . 
        } 
    """)

    # Set the output format to JSON
    sparql.setReturnFormat(JSON)

    # Execute the query
    results = sparql.query().convert()

    countries_code = []
    countries_labels = []

    for result in results["results"]["bindings"]:
        countries_code.append(result["code"]["value"])
        countries_labels.append(result["label"]["value"])

    final_result["countries_code"] = countries_code
    final_result["countries_labels"] = countries_labels

    return final_result