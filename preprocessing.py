import json
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def preprocessing(text):
    # inisialisasi stopword list dengan Sastrawi
    stop_factory = StopWordRemoverFactory()
    stop_word_list = stop_factory.get_stop_words()

    # inisialisasi stemming dengan module Sastrawi
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    # regex untuk remove punctuation
    cleantext = "(@[A-Za-z0-9_-]+)|([^A-Za-z \t\n])|(\w+:\/\/\S+)|(x[A-Za-z0-9]+)|(X[A-Za-z0-9]+)"

    text = text.rstrip("\n")
    text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)

    # casefolding dan remove punctuation
    text = re.sub(cleantext, ' ', str(text).lower()).strip()

    # tokenization
    tokens = []
    for token in text.split():

        # jika token tidak dalam stopwords, maka simpan:
        if token not in stop_word_list:
            token = stemmer.stem(token)  # lakukan stemming

            tokens.append(token)
            text = " ".join(tokens)

    return text


def labeling(text):
    lexicon_csv = pd.read_csv(
        'dict/indonesian-lexicon.csv', encoding='latin-1')
    lexicon_csv.drop('number_of_words', inplace=True, axis=1)
    lexicon_csv.reset_index()

    lexicon_json = lexicon_csv.to_json(orient='records')
    lexicon_json = json.loads(lexicon_json)

    new_lexicon_json = {}
    for new_lexicon in lexicon_json:
        new_lexicon_json[new_lexicon['word']] = new_lexicon['weight']

    sia = SentimentIntensityAnalyzer()
    sia.lexicon.update(new_lexicon_json)

    sentiment_dict = sia.polarity_scores(text)

    if sentiment_dict['compound'] >= 0.05:
        return "pos"
    elif sentiment_dict['compound'] <= - 0.05:
        return "neg"
    else:
        return "neu"


factory = StemmerFactory()
stemmer = factory.create_stemmer()

preprocessed_text = preprocessing("Gym nya kurang besar min")
labelled_text = labeling(preprocessed_text)

print(labelled_text)
