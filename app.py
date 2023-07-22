from flask import Flask, request, flash, render_template, jsonify
from fetcher import get_ig_comments, get_tiktok_comments
import pandas as pd
import os

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
