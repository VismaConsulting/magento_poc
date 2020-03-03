import logging
import json

import azure.functions as func

from __app__.Shared import constants, map_request

def main(req: func.HttpRequest) -> func.HttpResponse:
    data = req.get_json()
    user_query = data['message']
    preprocessed_query = map_request.preprocess_query(user_query, format='str')
    store_url = constants.Globals.SEARCH_URL.format(preprocessed_query.replace(' ', '%20'))
    response = {
        "reply": "Kanskje det er dette du leter etter?",
        "buttons": [
            {
                "button_type": "link",
                "label": constants.Globals.STORE_NAME,
                "value": store_url
            }
        ]}
    return func.HttpResponse(body=json.dumps(response), mimetype="application/json")
