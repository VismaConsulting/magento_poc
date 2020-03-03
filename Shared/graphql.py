import requests
import json
import pandas as pd
from . import constants

product_query = '''query { 
    products (search:"%s", filter: {category_id: {eq: "%s"}})
        {
          items{
            name
            stock_status
            meta_description
            url_key
            url_suffix
            image {
              url
            }
          }
        }
    }'''

categories_query = '''query {
  categoryList(filters: {}) {
    id
    name
  }
}'''


def get_products(search_terms, category=''):
    data = requests.post(url=constants.Globals.GRAPHQL_URL, json={'query': product_query % (search_terms, category)})
    json_data = json.loads(data.text)
    json_data = json_data['data']['products']['items']
    return json_data


def get_categories():
    data = requests.post(url=constants.Globals.GRAPHQL_URL, json={'query': categories_query})
    json_data = json.loads(data.text)
    json_data = json_data['data']['categoryList']
    return json_data