from flask import Flask, jsonify, request
from NameMatcher import NameMatcher
from ocr import get_text_from_image

import os


app = Flask(__name__)

ROOT = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_PATH = os.path.join(ROOT, "../../service_account.json")
NAME_LIST_PATH = os.path.join(ROOT, "name_list.txt")


@app.route("/")
def hello():
    return jsonify({"Hello": "World"})


@app.route("/submit_image", methods=['POST'])
def submit_image():
    text = get_text_from_image(SERVICE_ACCOUNT_PATH, request.data)
    nm = NameMatcher(path=NAME_LIST_PATH)
    name = nm.find_name_in_blob_of_text(text)

    return jsonify({
        "name": name,
    })
