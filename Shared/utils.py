from . import constants
from translate.translate import Translator

def create_carousel(json_response, num_to_show=5):
    if len(json_response) == 0:
        return {'reply': 'Beklager fant dessverre ikke det du spurte om.'}

    response = {
        'reply': 'Hva med noen av disse?', 
        'image_carousel': [],
        'new_context': {'product_memory': json_response[num_to_show:]}
        }

    for item in json_response[:num_to_show]:
        img = {
            'imageUrl': item['image']['url'],
            'linkUrl': constants.Globals.URL + item['url_key'] + item['url_suffix'],
            }
        response['image_carousel'].append(img)

    return response


def create_category_buttons(json_response, num_to_show=7):
    translator = Translator('no', 'en')
    if len(json_response) == 0:
        return {'reply': 'Beklager fant dessverre ikke det du spurte om.'}

    response = {
        'reply': 'Dette er noen av kategoriene vi har', 
        'buttons': [],
        'new_context': {'category_memory': json_response[num_to_show:]}
        }

    for item in json_response[:num_to_show]:
        button = {
                "button_type": "quick_reply",
                "label": translator.translate(item['name']),
                "value": str(item['id'])
                }
        response['buttons'].append(button)

    return response


