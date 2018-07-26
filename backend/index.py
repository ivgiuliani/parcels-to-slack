from slack import all_users, send_parcel_notification
from flask import Flask, jsonify, request, abort, send_from_directory, render_template
from name_matcher import NameMatcher
from ocr import get_text_from_image

import os
import base64

app = Flask(__name__)

ROOT = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_PATH = os.path.join(ROOT, "../../service_account.json")
NAME_LIST_PATH = os.path.join(ROOT, "name_list.txt")

ALL_USERS = {k.lower(): v for k,v in all_users().items()}


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
    try:
        image = base64.b64decode(request.data)
        text = get_text_from_image(SERVICE_ACCOUNT_PATH, image)

        nm = NameMatcher(ALL_USERS)
        name = nm.find_name_in_blob_of_text(text)

        user_id = ALL_USERS[name]

        send_parcel_notification(user_id, base64_image=request.data)
    except RuntimeError as e:
        return jsonify({
            "error": str(e)
        })

    return jsonify({
        "name": name,
    })
