from io import BytesIO
from flask import Flask, render_template, request
from utils import load_device, load_model, predict, load_image
from PIL import Image
import os
from werkzeug.middleware.proxy_fix import ProxyFix


def read_image(file):
    img = Image.open(BytesIO(file))
    return img

app = Flask(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

device = load_device()
model = load_model(device)


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template('home.html')

@app.route("/predict", methods=["GET", "POST"])
def predict_flask():
    if request.method == "POST":
        file = request.files['file']
        filename = file.filename
        file_path = os.path.join('static', filename)
        file.save(file_path)
        img = load_image(file_path)
        pred = predict(img, model, device)
    return render_template("predict.html", output=pred, user_image = file_path)
