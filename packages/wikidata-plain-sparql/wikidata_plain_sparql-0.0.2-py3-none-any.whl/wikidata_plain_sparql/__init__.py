import pandas as pd
import requests
import json

def query(query):
    url = 'https://query.wikidata.org/sparql'
    payload = {
        'query': query
    }
    # add header to receive result as json
    headers = {
        'Accept': 'application/sparql-results+json'
    }
    while True:
        response = requests.get(url, params = payload, headers = headers)
        # check if request was successful
        if response.ok:
            # load json as dict
            data = json.loads(response.content)
            # create empty data frame
            df = pd.DataFrame(columns = data['head']['vars'])
            # iterate through all results
            for result in data['results']['bindings']:
                # flatten result objects (result <- result.value)
                mappedResult = {}
                for column in result:
                    mappedResult[column] = result[column]['value']
                # append result to data frame
                df = df.append(mappedResult, ignore_index = True)
            return df
        else:
            # raise exception in case of http error
            response.raise_for_status()
            break
    raise Exception