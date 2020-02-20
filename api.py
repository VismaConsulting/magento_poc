from flask import Flask, jsonify, request
import logging
from globals import Globals
from map_request import search_for_product, preprocess_query, get_best_quess_item

# App setup
app = Flask(__name__)


@app.route('/search_product_catalog', methods=['POST'])
def search_product_catalog():
    data = request.get_json()
    user_query = data['query']
    products_df = search_for_product(user_query)
    products_json = products_df.to_json(orient='records')
    return products_json


@app.route('/get_query_search_url', methods=['POST'])
def get_query_url():
    data = request.get_json()
    user_query = data['query']
    preprocessed_query = preprocess_query(user_query)
    return Globals.SEARCH_URL.format(preprocessed_query.replace(' ', '%20'))


@app.route('/get_query_search_url_from_kindly', methods=['POST'])
def get_query_url_from_kindly():
    data = request.get_json()
    print(data)
    user_query = data['message']
    preprocessed_query = preprocess_query(user_query)
    print(preprocessed_query)
    store_url = Globals.SEARCH_URL.format(preprocessed_query.replace(' ', '%20'))
    return {
        "reply": "Maybe this is what you want?",
        "buttons": [
            {
                "button_type": "link",
                "label": Globals.STORE_NAME,
                "value": store_url
            }
        ]}


@app.route('/get_best_guess_item_from_kindly', methods=['POST'])
def get_best_guess_item_from_kindly():
    data = request.get_json()
    pattern_key = data['exchange']['pattern_key']
    pattern = data['context'][pattern_key]
    user_query = data['message'].replace(pattern, "")
    item_json = get_best_quess_item(user_query)[0]
    return {'reply': 'Hva med ' + item_json['name'] + '?', 'image': item_json['image']['url'],
            "buttons": [
            {
                "button_type": "link",
                "label": item_json['name'] + ' at ' + Globals.STORE_NAME,
                "value": Globals.URL + item_json['url_key'] + item_json['url_suffix']
            }
        ]}


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
