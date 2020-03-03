import logging
import json

import azure.functions as func

from __app__.Shared import constants, map_request, graphql

def main(req: func.HttpRequest) -> func.HttpResponse:
    data = req.get_json()
    pattern_key = data['exchange']['pattern_key']
    pattern = data['context'][pattern_key]
    user_query = data['message'].replace(pattern, "")
    preprocessed_query = map_request.preprocess_query(user_query, format='str')
    top_product = graphql.get_products(preprocessed_query)[0]
    if top_product['stock_status'] == 'IN_STOCK':
        response = {'reply': top_product['name'] + ' er på lager',
            "buttons": [
            {
                "button_type": "link",
                "label": 'Kjøp ' + top_product['name'] + ' her',
                "value": constants.Globals.URL + top_product['url_key'] + top_product['url_suffix']
            }
        ]}
    else:
        response = {"reply": top_product['name'] + ' er dessverre ikke på lager'}
    return func.HttpResponse(body=json.dumps(response), mimetype="application/json")
