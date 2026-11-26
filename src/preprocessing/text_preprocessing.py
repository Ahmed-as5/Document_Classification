import re
import nltk
from functools import lru_cache

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag


@lru_cache(maxsize=1)
def _load_nltk_resources():
    resources = (
        'punkt_tab',
        'stopwords',
        'wordnet',
        'omw-1.4',
        'averaged_perceptron_tagger_eng',
    )
    for resource in resources:
        if not nltk.download(resource, quiet=True):
            raise RuntimeError(f"Unable to download required NLTK resource: {resource}")

    words = set(stopwords.words('english'))
    words.difference_update({'no', 'nor', 'not'})
    return words, WordNetLemmatizer()


def clean_text(text):

    text = text.lower()

    text = re.sub(r'\b\d+\b', '', text)

    text = re.sub(r'[^\w\s]', ' ', text)

    text = re.sub(r'\s+', ' ', text).strip()

    return text


def tokenize_text(text):
    _load_nltk_resources()
    tokens = word_tokenize(text)
    return tokens


def remove_stopwords(tokens):
    stop_words, _ = _load_nltk_resources()
    filtered_tokens = [
        word for word in tokens
        if word not in stop_words
    ]
    return filtered_tokens


def lemmatize_text(tokens):
    _, lemmatizer = _load_nltk_resources()
    tagged_words = pos_tag(tokens)
    lemmatized_tokens = []
    for word, tag in tagged_words:
        if tag.startswith('J'):
            pos = wordnet.ADJ
        elif tag.startswith('V'):
            pos = wordnet.VERB
        elif tag.startswith('N'):
            pos = wordnet.NOUN
        elif tag.startswith('R'):
            pos = wordnet.ADV
        else:
            pos = wordnet.NOUN
        lemmatized_tokens.append(lemmatizer.lemmatize(word, pos))
    return lemmatized_tokens


def reconstruct_text(tokens):
    return ' '.join(tokens)


def preprocess_text(text):

    text = clean_text(text)

    tokens = tokenize_text(text)

    tokens = remove_stopwords(tokens)

    tokens = lemmatize_text(tokens)

    processed_text = reconstruct_text(tokens)

    return processed_text