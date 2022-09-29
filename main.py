from io import BytesIO
from flask import Flask, render_template, request
from utils import load_device, load_model, predict, load_image, import_model
from PIL import Image
import os
import base64
from werkzeug.middleware.proxy_fix import ProxyFix

import_model(bucket="mbenxsalha", key="diffusion/model.pth", filename="model_2.pth")

def read_image(file):
    img = Image.open(BytesIO(file)).convert("RGB")
    return img

app = Flask(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

device = load_device()
model = load_model(device, path="model_2.pth")


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template('home.html')

@app.route("/predict", methods=["GET", "POST"])
def predict_flask():
    if request.method == "POST":
        file = request.files['file']
        img = read_image(file.read())

        data = BytesIO()
        img.save(data, "JPEG")
        encoded_img_data = base64.b64encode(data.getvalue())
        img_data=encoded_img_data.decode('utf-8')
        """
        filename = file.filename
        file_path = os.path.join('static', filename)
        file.save(file_path)
        img = load_image(file_path)
        """
        pred = predict(img, model, device)
    return render_template("predict.html", output=pred, img_data=img_data)
    """
    return render_template("predict.html", output=pred, user_image = file_path)
    """
