import json
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def labeling_text(text):
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

    print(sentiment_dict)

labeling_text("unit sehat punya fasilitas lengkap")