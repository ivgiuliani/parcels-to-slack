from flask import Flask, jsonify
from NameMatcher import NameMatcher
from ocr import get_text_from_image

app = Flask(__name__)

@app.route("/")
def hello():
    return jsonify({"Hello": "World"})

@app.route("/submit_image", methods=['POST'])
def submit_image():
    text = get_text_from_image(service_account_path, image_buff.read(), preprocess_arg)
    nm = NameMatcher(path=names_arg)
    name = nm.find_name_in_blob_of_text(text)