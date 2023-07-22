import json, re
import pandas as pd
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

text_example = "perpusnya tai anjing"
cleantext = "(@[A-Za-z0-9_-]+)|([^A-Za-z \t\n])|(\w+:\/\/\S+)|(x[A-Za-z0-9]+)|(X[A-Za-z0-9]+)" 

text = text_example.rstrip("\n")
text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
text = re.sub(cleantext,' ',str(text).lower()).strip() #casefolding dan remove punctuation

lexicon_csv = pd.read_csv('dict/indonesian-lexicon.csv', encoding='latin-1')
lexicon_csv.drop('number_of_words', inplace=True, axis=1)
lexicon_csv.reset_index()

lexicon_json = lexicon_csv.to_json(orient='records')
lexicon_json = json.loads(lexicon_json)

new_lexicon_json = {}
for new_lexicon in lexicon_json:
   new_lexicon_json[new_lexicon['word']] = new_lexicon['weight']

print(new_lexicon_json)

sia = SentimentIntensityAnalyzer()
sia.lexicon.update(new_lexicon_json)

print(sia.polarity_scores(text_example))