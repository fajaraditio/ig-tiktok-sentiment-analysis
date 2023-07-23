import pandas as pd
import re
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score, multilabel_confusion_matrix


def mapping(clean_data):
    # netral, negatif, positif = y_test['label'].value_counts()
    # total = positif + negatif + netral
    # print(y_test['label'].value_counts() )

    # pie_labels = labels
    # pie_colors = colors
    # pie_values = [positif, negatif, netral]

    # bar_labels = labels
    # bar_values = [positif, negatif, netral]
    return ''


def evaluating_data(csv):
    clean_data = csv.fillna(' ')

    clean_data['label'] = clean_data['label'].map(
        {'pos': 2, 'neg': 1, 'neu': 0})
    features = clean_data['comment'].fillna(' ')
    labels = clean_data['label']

    vectorizer = TfidfVectorizer()
    features = vectorizer.fit_transform(features)

    # training data
    x_train, x_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.5, random_state=0)

    # menggunakan metode klasifikasi Naive Bayes
    mnb = MultinomialNB()
    mnb.fit(x_train, y_train)
    y_mnb = mnb.predict(x_test)

    mnb_classification_report = classification_report(y_test, y_mnb, target_names=['pos', 'neg', 'neu'], output_dict=True)
    mnb_accuracy = accuracy_score(y_test, y_mnb)

    return mnb_classification_report, mnb_accuracy