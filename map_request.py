from graphql import get_products, get_best_quess_item
import nltk
import en_core_web_sm


nltk.download('punkt')
nltk.download('stopwords')

ACCEPTED_SEARCH_WORD_CLASSES = ['NOUN', 'ADJ', 'PROPN']

nlp = en_core_web_sm.load()

def search_for_product(query):
    preprocessed_query = preprocess_query(query)
    return get_products(preprocessed_query)

def preprocess_query(query):
    doc = nlp(query)
    tagged = [(x.orth_, x.pos_, x.lemma_) for x in doc if not x.is_stop and x.pos_ != 'PUNCT']
    print(tagged)
    search_query = []
    for token, word_class, lemma in tagged:
        if word_class in ACCEPTED_SEARCH_WORD_CLASSES:
            search_query.append(lemma)
    return " ".join(search_query)


if __name__ == '__main__':
    query = "blue pants"
    product_json = get_best_quess_item(query.lower())
    print(product_json)


