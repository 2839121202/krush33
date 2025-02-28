import os
from flask import Flask, redirect, render_template, request, send_from_directory
from PIL import Image
import torchvision.transforms.functional as TF
import CNN
import numpy as np
import torch
import pandas as pd
from werkzeug.utils import secure_filename

from config import *

# Load the disease information and the model
disease_info = pd.read_csv(DISEASE_INFO_PATH, encoding=CSV_ENCODING)

# Load the model
model = CNN.CNN(NUM_CLASSES)
model.load_state_dict(torch.load(MODEL_WEIGHTS_PATH))
model.eval()


# Prediction function
def prediction(image_path):
    image = Image.open(image_path)
    image = image.resize(IMAGE_SIZE)
    input_data = TF.to_tensor(image)
    input_data = input_data.view((-1, INPUT_CHANNELS, *IMAGE_SIZE))
    output = model(input_data)
    output = output.detach().numpy()
    index = np.argmax(output)
    return index


# Flask app
app = Flask(__name__)


app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "image" not in request.files:
            return render_template("index.html", error="No file uploaded")

        file = request.files["image"]
        if file.filename == "":
            return render_template("index.html", error="No file selected")

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            try:
                index = prediction(filepath)
                disease = disease_info.loc[index, "disease_name"]
                description = disease_info.loc[index, "description"]
                prevention = disease_info.loc[index, "Possible Steps"]
                reference_image = disease_info.loc[index, "image_url"]

                return render_template(
                    "index.html",
                    image_path=os.path.join("uploads", filename),
                    disease=disease,
                    description=description,
                    prevention=prevention,
                    reference_image=reference_image,
                )
            except Exception as e:
                return render_template(
                    "index.html", error=f"Error processing image: {str(e)}"
                )

        return render_template("index.html", error="Invalid file type")

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
