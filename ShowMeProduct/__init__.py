import logging
import json

import azure.functions as func

from __app__.Shared import map_request, graphql, utils

def main(req: func.HttpRequest) -> func.HttpResponse:
    data = req.get_json()
    pattern_key = data['exchange']['pattern_key']
    pattern = data['context'][pattern_key]
    user_query = data['message'].replace(pattern, "")
    preprocessed_query = map_request.preprocess_query(user_query, format='str')
    json_response = graphql.get_products(preprocessed_query)
    response = utils.create_carousel(json_response)
    return func.HttpResponse(body=json.dumps(response), mimetype="application/json")

