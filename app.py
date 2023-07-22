from flask import Flask, request, flash, render_template, jsonify
from instagram import get_comments
import pandas as pd

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if (request.method == 'GET'):
        return render_template('upload.html')
    elif (request.method == 'POST'):
        get_comments(request.form['dataset_instagram'])

        text = pd.read_csv('uploads/instagram.csv', encoding='latin-1')
        return render_template('upload.html',tables=[text.to_html(classes='table table-bordered', table_id='dataTable')])
