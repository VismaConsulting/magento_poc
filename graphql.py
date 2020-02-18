import requests
import json
import pandas as pd


url = "https://master-7rqtwti-mfwmkrjfqvbjk.us-4.magentosite.cloud/graphql"
#
# print(process.extract(query.lower(), [x.lower() for x in brands], limit=2))
# print(process.extract(query.lower(), [x.lower() for x in products], limit=3))

categories = """
  query { categoryList(filters: {}) {
    name
  }}
  """

product_query = 'query{products(search:"%s"){items{name}}}'

def get_categories():
    data = requests.post(url=url, json={'query': categories})
    json_data = json.loads(data.text)
    df_data = json_data['data']['categoryList']
    cats = [x['name'].lower() for x in df_data]
    return cats

def get_products(search_terms):
    search_terms = "".join(search_terms)
    data = requests.post(url=url, json={'query': product_query % (search_terms)})
    json_data = json.loads(data.text)
    df_data = json_data['data']['products']['items']
    df = create_dataframe(df_data)
    return df


def create_dataframe(df_data):
    df = pd.DataFrame(df_data)
    df = df.apply(lambda x: x.astype(str).str.lower())
    return df