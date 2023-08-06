#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
simple client from new oauth API

PRIVATE FILE
"""

import click 
import requests



@click.command()
@click.argument('query', nargs=-1)
def main(query=1):
    """
    Simple test script for new API based on Readcube

    From command line:

    export endpoint="https://sandbox-api.dimensions.ai/"
    export DSL_TOKEN="$(curl -X GET "https://$endpoint/token?api_key=8cGaPHPQfxjmMR5NcnWCwzwjHIleGrTz")"
    curl -X POST https://$endpoint/api/query -H "authorization: Bearer $DSL_TOKEN" -d 'search publications return publications'

    """
    if not query: 
        q = "search publications return publications"
    else:
        q = " ".join([x for x in query])
    

    if True: #analytics 
        api_key = "8cGaPHPQfxjmMR5NcnWCwzwjHIleGrTz"
        endpoint = "sandbox-api.dimensions.ai"
    else: #CRIS
        api_key = "uTQEFiYYeBzLSBGZr39zGBhaxuAiLkHp"
        endpoint = "sandbox-cris-api.dimensions.ai"

    # get token from key    

    url_token = f"https://{endpoint}/token?api_key={api_key}"
    response = requests.get(url_token)
    response.raise_for_status()
    token = response.text.strip("\n") # NOTE token has newline char at the end
    # print("Token:",  token)
    
    # query using token
    
    headers = {'Authorization': "Bearer " + token}
    url_query = f"https://{endpoint}/api/query"
    response = requests.post(url_query, data=q, headers=headers)
    
    try:
        res_json = response.json()
        print(res_json)
    except:
        print('Unexpected error. JSON could not be parsed.')
        print("Raw Response:",  response)



if __name__ == '__main__':
    main()


