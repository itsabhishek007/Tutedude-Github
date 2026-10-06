from flask import Flask, json, jsonify, redirect, render_template, request, url_for
from pymongo import MongoClient
import json
import os 
from dotenv import load_dotenv
import certifi
load_dotenv("atlas-credentials.env")
 
MONGO_URI = os.getenv('MONGODB_URI')
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
collection = client["flask_db"]["contacts"]
app = Flask(__name__)

@app.route('/api')
def fetch():
    f = open('info.json', 'r')
    f = json.load(f)

    return jsonify(f)

@app.route('/contact')
def contact():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    form_data = dict(request.form)
    try:
        if not all(form_data.values()):
            raise ValueError("All fields are required.")
        collection.insert_one(dict(form_data))
        return redirect(url_for("success"))
    except Exception as e:
        return render_template("index.html", error=str(e), form_data=form_data)

@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == '__main__':
     app.run(debug=True, port=5001)