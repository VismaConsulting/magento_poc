from graphql import get_products, get_best_quess_item
import nltk
import en_core_web_sm

import spacy
from sense2vec import Sense2VecComponent, Sense2Vec

nlp = spacy.load("en_core_web_sm")
#s2v = Sense2Vec().from_disk("s2v_reddit_2015_md/s2v_old")
colors = ['lily', 'liliac', 'rain', 'peach', 'lava', 'forest']

nltk.download('punkt')
nltk.download('stopwords')

ACCEPTED_SEARCH_WORD_CLASSES = ['NOUN', 'ADJ', 'PROPN']


# nlp = en_core_web_sm.load()

def similarity(query):
    similarities = []
    for token in query:
        for color in color_representation():
            try:
                similarities.append((token, color, s2v.similarity(token, color)))
            except:
                pass
    similarities = sorted(similarities, key=lambda x: x[2], reverse=True)
    return similarities


def search_for_product(preprocessed_query):
    return get_products(preprocessed_query)


def preprocess_query(query, format=None):
    doc = nlp(query)
    tagged = [(x.orth_, x.pos_, x.lemma_) for x in doc if not x.is_stop and x.pos_ != 'PUNCT']

    if format is None:
        return tagged

    elif format == 'str':
        search_query = []
        for token, word_class, lemma in tagged:
            if word_class in ACCEPTED_SEARCH_WORD_CLASSES:
                search_query.append(lemma)
        return " ".join(search_query)

    elif format == 'sense2vec':
        search_query = []
        for token, word_class, lemma in tagged:
            if word_class in ACCEPTED_SEARCH_WORD_CLASSES:
                search_query.append('{}|{}'.format(token, word_class.upper()))
        return search_query


def color_representation():
    cs = []
    for c in colors:
        processed = nlp(c)[0]
        formated = '{}|{}'.format(c, processed.pos_)
        other_senses = s2v.get_other_senses(formated)
        cs = cs + [formated] + other_senses
    return cs


if __name__ == '__main__':
    query = "i feel moody"
    d = preprocess_query(query, format='sense2vec')
    similarity(d)
    exit()

    product_json = get_best_quess_item(query.lower())
    print(product_json)
