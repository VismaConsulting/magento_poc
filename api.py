from flask import Flask, jsonify, request
import logging
import requests
import json
from map_request import search_for_product

# App setup
app = Flask(__name__)


@app.route('/search_product_catalog', methods=['POST'])
def search_product_catalog():
    data = request.get_json()
    user_query = data['query']
    products_df = search_for_product(user_query)
    print(products_df)
    return user_query


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)