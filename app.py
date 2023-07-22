from flask import Flask, request, flash, render_template, jsonify
from fetcher import get_ig_comments, get_tiktok_comments
from preprocessing import sentiment, preprocessing_text, labeling_text
import pandas as pd
import os
import json

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.debug = True


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/upload-ajax', methods=['POST'])
def upload_ajax():
    if (request.form.get('url_instagram_post')):
        if (not os.path.exists('uploads/instagram_src.csv')):
            get_ig_comments(request.form.get('url_instagram_post'))

        text = pd.read_csv('uploads/instagram_src.csv', encoding='latin-1')
        return text.to_json(orient='records')

    elif (request.form.get('url_tiktok_post')):
        if (not os.path.exists('uploads/tiktok_src.csv')):
            get_tiktok_comments(request.form.get('url_tiktok_post'))

        text = pd.read_csv('uploads/tiktok_src.csv', encoding='latin-1')
        return text.to_json(orient='records')


@app.route('/preprocessing')
def preprocessing():
    return render_template('preprocessing.html')


@app.route('/preprocessing-ajax', methods=['POST'])
def preprocessing_ajax():
    if (request.form.get('preprocessing_ig')):
        if (not os.path.exists('uploads/instagram_src.csv')):
            return {'data': 'empty'}

        text = pd.read_csv('uploads/instagram_src.csv', encoding='latin-1')
        json_text = text.to_json(orient='records')
        json_text = json.loads(json_text)

        comments = []
        for comment in json_text:
            username = comment['username']
            comment_text = comment['comment']
            clean_comment = preprocessing_text(comment_text)
            labeled_comment = labeling_text(clean_comment)
            sentiment_result = sentiment(clean_comment)

            comments.append({'username': username, 'comment': comment_text,
                            'clean_comment': clean_comment, 'label': labeled_comment,
                             'pos': sentiment_result['pos'], 'neg': sentiment_result['neg'], 'neu': sentiment_result['neu'],
                             'compound': sentiment_result['compound']})

        pd.DataFrame(comments).to_csv(
            'uploads/instagram_clean.csv',
            header=['username', 'comment', 'clean_comment', 'label', 'pos', 'neg', 'neu', 'compund'],
            index=False)

        return comments

    elif (request.form.get('preprocessing_tt')):
        if (not os.path.exists('uploads/tiktok_src.csv')):
            return {'data': 'empty'}

        text = pd.read_csv('uploads/tiktok_src.csv', encoding='latin-1')
        json_text = text.to_json(orient='records')
        json_text = json.loads(json_text)

        comments = []
        for comment in json_text:
            username = comment['username']
            comment_text = comment['comment']
            clean_comment = preprocessing_text(comment_text)
            labeled_comment = labeling_text(clean_comment)
            sentiment_result = sentiment(clean_comment)

            comments.append({'username': username, 'comment': comment_text,
                            'clean_comment': clean_comment, 'label': labeled_comment,
                             'pos': sentiment_result['pos'], 'neg': sentiment_result['neg'], 'neu': sentiment_result['neu'],
                             'compound': sentiment_result['compound']})

        pd.DataFrame(comments).to_csv(
            'uploads/tiktok_clean.csv',
            header=['username', 'comment', 'clean_comment', 'label', 'pos', 'neg', 'neu', 'compund'],
            index=False)

        return comments
