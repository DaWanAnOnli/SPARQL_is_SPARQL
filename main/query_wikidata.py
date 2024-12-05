import requests

# Define the SPARQL endpoint for Wikidata
url = 'https://query.wikidata.org/sparql'

# Define the SPARQL query to get the ISO 2-digit code for Brunei
query = """
SELECT ?isoCode
WHERE {
  ?country wdt:P31 wd:Q6256;  # Instance of country (Q6256)
           rdfs:label "Brunei"@en;  # Filter by label "Brunei"
           wdt:P297 ?isoCode.  # ISO 2-digit code (P297)
}
"""

# Send the query to Wikidata's SPARQL endpoint
response = requests.get(url, params={'query': query, 'format': 'json'})

# Check if the request was successful (status code 200)
if response.status_code == 200:
    data = response.json()  # Parse the response as JSON
    if data['results']['bindings']:
        iso_code = data['results']['bindings'][0]['isoCode']['value']
        print(f"ISO 2-digit code for Brunei: {iso_code}")
    else:
        print("No result found for Brunei.")
else:
    print(f"Error: {response.status_code}")
