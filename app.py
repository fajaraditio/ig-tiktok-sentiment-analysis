from flask import Flask, request, flash, render_template, jsonify

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')