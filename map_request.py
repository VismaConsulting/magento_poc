from graphql import get_products, get_best_quess_item
import nltk
import en_core_web_sm
from translate.translate import Translator

import spacy
from sense2vec import Sense2VecComponent, Sense2Vec

nlp = spacy.load("en_core_web_sm")
# s2v = Sense2Vec().from_disk("s2v_reddit_2015_md/s2v_old")
colors = ['lily', 'liliac', 'rain', 'peach', 'lava', 'forest']

nltk.download('punkt')
nltk.download('stopwords')

ACCEPTED_SEARCH_WORD_CLASSES = ['NOUN', 'ADJ', 'PROPN']


# nlp = en_core_web_sm.load()

def similarity(query):
    similarities = []
    for token in query:
        for color in find_all_senses(colors):
            try:
                similarities.append((token, color, s2v.similarity(token, color)))
            except:
                pass
    similarities = sorted(similarities, key=lambda x: x[2], reverse=True)
    return similarities


def preprocess_query(query, format=None):
    translator = Translator('en', 'no')
    query = translator.translate(query)
    print(query)
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

    else:
        raise ValueError('Format ' + format + ' is not supported')


def preprocess_to_sense2vec(query):
    doc = nlp(query)
    tagged = [(x.orth_, x.pos_, x.lemma_) for x in doc if not x.is_stop and x.pos_ != 'PUNCT']
    search_query = []
    for token, word_class, lemma in tagged:
        if word_class in ACCEPTED_SEARCH_WORD_CLASSES:
            search_query.append('{}|{}'.format(token, word_class.upper()))
    return search_query


def find_all_senses(tokens):
    senses = []
    for token in tokens:
        processed = nlp(token)[0]
        formated = '{}|{}'.format(token, processed.pos_)
        other_senses = s2v.get_other_senses(formated)
        senses = senses + [formated] + other_senses
    return senses


if __name__ == '__main__':
    query = "i feel moody"
    d = preprocess_to_sense2vec(query)
    similarity(d)
    exit()

    product_json = get_best_quess_item(query.lower())
    print(product_json)
