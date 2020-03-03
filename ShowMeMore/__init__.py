import logging
import json
import uuid

import azure.functions as func

from __app__.Shared import utils

def main(req: func.HttpRequest) -> func.HttpResponse:
    data = req.get_json()
    if 'product_memory' in data['context'].keys():
        response = utils.create_carousel(data['context']['product_memory'])
    else:
        response = {'reply': 'Fant dessverre ikke noe mer'}
    return func.HttpResponse(body=json.dumps(response), mimetype="application/json")

