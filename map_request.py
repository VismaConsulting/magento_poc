from fuzzywuzzy import process
from graphql import get_categories, get_products
import nltk
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

def search_for_product(query):
    # Tokenize query
    tokenized = nltk.word_tokenize(query)
    tokenized = [w for w in tokenized if not w in set(stopwords.words('english'))]

    categories = get_categories()
    guessed_category = guess_category(tokenized, categories)[0]
    print('*** GUESSED CATEGORY *** = ' + guessed_category)
    return get_products([guessed_category])

def guess_category(query, categories):
    cat_with_rank = [process.extract(x, categories) for x in query]
    cat_with_rank_flattened = [item for sublist in cat_with_rank for item in sublist]

    all_scores = [y for (x, y) in cat_with_rank_flattened]

    max_idx = all_scores.index(max(all_scores))

    return cat_with_rank_flattened[max_idx]

if __name__ == '__main__':
    query = "I want a sweater"

    search_for_product(query.lower())


