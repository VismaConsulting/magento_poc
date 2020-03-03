import logging
import json

import azure.functions as func

from __app__.Shared import map_request, graphql, utils

def main(req: func.HttpRequest) -> func.HttpResponse:
    data = req.get_json()
    chosen_category = data['message']
    json_response = graphql.get_products('', category=chosen_category)
    response = utils.create_carousel(json_response)
    return func.HttpResponse(body=json.dumps(response), mimetype="application/json")

