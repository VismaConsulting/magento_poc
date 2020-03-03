import logging
import json

import azure.functions as func

from __app__.Shared import utils, graphql

def main(req: func.HttpRequest) -> func.HttpResponse:
    data = req.get_json()
    json_response = graphql.get_categories()
    response = utils.create_category_buttons(json_response)
    return func.HttpResponse(body=json.dumps(response), mimetype="application/json")




