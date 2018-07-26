from flask import Flask, jsonify, request, abort, send_from_directory, render_template
from NameMatcher import NameMatcher
from ocr import get_text_from_image

import os


app = Flask(__name__)

ROOT = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_PATH = os.path.join(ROOT, "../../service_account.json")
NAME_LIST_PATH = os.path.join(ROOT, "name_list.txt")


@app.route('/')
def root():
    return render_template('index.html')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)


@app.route("/submit_image", methods=['POST'])
def submit_image():

    text = ''
    try:
        text = get_text_from_image(SERVICE_ACCOUNT_PATH, request.data)
    except Exception as e:
        return jsonify({
            "error": str(e),
        })

    nm = NameMatcher(path=NAME_LIST_PATH)
    name = nm.find_name_in_blob_of_text(text)

    return jsonify({
        "name": name,
    })
