import requests
import json
import pandas as pd
from globals import Globals

categories = """
  query { categoryList(filters: {}) {
    name
  }}
  """

product_query = '''query { 
    products (search:"%s")
        {items{
            name
            stock_status
            meta_description
            }
        }
    }'''


best_quess_item = '''query { 
    products (search:"%s")
        {items{
          name
          url_key
          url_suffix
            image{
              url
            }
            }
        }
    }'''

def get_best_quess_item(search_terms, num_to_fetch=1):
    print("SEARCHING FOR: " + search_terms)
    data = requests.post(url=Globals.GRAPHQL_URL, json={'query': best_quess_item % (search_terms)})
    json_data = json.loads(data.text)
    df_data = json_data['data']['products']['items']
    return df_data[:num_to_fetch]


def get_products(search_terms):
    print("SEARCHING FOR: " + search_terms)
    data = requests.post(url=Globals.GRAPHQL_URL, json={'query': product_query % (search_terms)})
    json_data = json.loads(data.text)
    print(json_data)
    df_data = json_data['data']['products']['items']
    df = create_dataframe(df_data)
    return df


def create_dataframe(df_data):
    df = pd.DataFrame(df_data)
    df = df.apply(lambda x: x.astype(str).str.lower())
    return df