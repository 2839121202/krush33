import os
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    jsonify,
)
from PIL import Image
import torchvision.transforms.functional as TF
import CNN
import numpy as np
import torch
import pandas as pd
from werkzeug.utils import secure_filename

from disease_tts import DiseaseTTS
from weather import geocode_location, get_weather_data, get_weather_icon
from translation import get_translation

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

from config import *

## ============== Model ============== ##
# Load the model
model = CNN.CNN(NUM_CLASSES)
model.load_state_dict(torch.load(MODEL_WEIGHTS_PATH))
model.eval()

# Load soil model
soil_model = load_model(SOIL_MODEL_PATH)


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


def predict_soil(image_path):
    img = load_img(image_path, target_size=SOIL_IMAGE_SIZE)
    img_array = img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = soil_model.predict(img_array)
    soil_type_index = np.argmax(predictions[0])
    confidence = float(predictions[0][soil_type_index] * 100)

    soil_types = [
        "Black Soil",
        "Cinder Soil",
        "Laterite Soil",
        "Peat Soil",
        "Yellow Soil",
    ]
    return soil_types[soil_type_index], confidence


## ============== Disease Info ============== ##
# Multi-language support
LANGUAGES = {
    "en": {"name": "English", "file": f"{DISEASE_INFO_PATH_PARTIAL}_en.csv"},
    "hi": {"name": "हिंदी", "file": f"{DISEASE_INFO_PATH_PARTIAL}_hi.csv"},
    "pa": {"name": "ਪੰਜਾਬੀ", "file": f"{DISEASE_INFO_PATH_PARTIAL}_pa.csv"},
    "bn": {"name": "বাংলা", "file": f"{DISEASE_INFO_PATH_PARTIAL}_bn.csv"},
    "te": {"name": "తెలుగు", "file": f"{DISEASE_INFO_PATH_PARTIAL}_te.csv"},
    "ta": {"name": "தமிழ்", "file": f"{DISEASE_INFO_PATH_PARTIAL}_ta.csv"},
    "ml": {"name": "മലയാളം", "file": f"{DISEASE_INFO_PATH_PARTIAL}_ml.csv"},
    "kn": {"name": "ಕನ್ನಡ", "file": f"{DISEASE_INFO_PATH_PARTIAL}_kn.csv"},
    "or": {"name": "ଓଡ଼ିଆ", "file": f"{DISEASE_INFO_PATH_PARTIAL}_or.csv"},
    "mr": {"name": "मराठी", "file": f"{DISEASE_INFO_PATH_PARTIAL}_mr.csv"},
    "ur": {"name": "اردو", "file": f"{DISEASE_INFO_PATH_PARTIAL}_ur.csv"},
}

disease_info_dict = {}
for lang_code, lang_data in LANGUAGES.items():
    try:
        disease_info_dict[lang_code] = pd.read_csv(
            lang_data["file"], encoding=CSV_ENCODING
        )
    except Exception as e:
        print(f"Error loading {lang_code}: {str(e)}")

## ============== Marketplace Info ============== ##
# Load the marketplace info
disease_info = pd.read_csv(MARKETPLACE_INFO_PATH, encoding=CSV_ENCODING)
products = disease_info.to_dict("records")

## ============== Flask App ============== ##
# Flask app
app = Flask(__name__)

tts = DiseaseTTS()

app.secret_key = os.urandom(24)
app.jinja_env.globals.update(t=get_translation)


@app.before_request
def before_request():
    lang = request.args.get("lang")
    if lang in LANGUAGES:
        session["lang"] = lang
    elif "lang" not in session:
        session["lang"] = "en"


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
            return render_template(
                "index.html",
                error="No file uploaded",
                languages=LANGUAGES,
                selected_lang=session.get("lang", "en"),
            )

        file = request.files["image"]
        if file.filename == "":
            return render_template(
                "index.html",
                error="No file selected",
                languages=LANGUAGES,
                selected_lang=session.get("lang", "en"),
            )

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            try:
                index = prediction(filepath)
                lang = session.get("lang", "en")
                disease_info = disease_info_dict.get(lang, disease_info_dict["en"])

                disease = disease_info.loc[index, "disease_name"]
                description = disease_info.loc[index, "description"]
                prevention = disease_info.loc[index, "Possible Steps"]
                reference_image = disease_info.loc[index, "image_url"]

                return render_template(
                    "index.html",
                    languages=LANGUAGES,
                    selected_lang=lang,
                    image_path=os.path.join("uploads", filename),
                    disease=disease,
                    description=description,
                    prevention=prevention,
                    reference_image=reference_image,
                    recommended_product=products[index],
                )
            except Exception as e:
                return render_template(
                    "index.html",
                    languages=LANGUAGES,
                    selected_lang=session.get("lang", "en"),
                    error=f"Error processing image: {str(e)}",
                )

        return render_template(
            "index.html",
            languages=LANGUAGES,
            selected_lang=session.get("lang", "en"),
            error="Invalid file type",
        )

    return render_template(
        "index.html",
        languages=LANGUAGES,
        selected_lang=session.get("lang", "en"),
    )


@app.route("/soil", methods=["GET", "POST"])
def soil():
    if request.method == "POST":
        if "image" not in request.files:
            return render_template(
                "soil.html",
                error="No file uploaded",
                languages=LANGUAGES,
                selected_lang=session.get("lang", "en"),
            )

        file = request.files["image"]
        if file.filename == "":
            return render_template(
                "soil.html",
                error="No file selected",
                languages=LANGUAGES,
                selected_lang=session.get("lang", "en"),
            )

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            try:
                soil_type, confidence = predict_soil(filepath)
                recommended_crops = SOIL_CROP_RECOMMENDATIONS[soil_type]

                return render_template(
                    "soil.html",
                    languages=LANGUAGES,
                    selected_lang=session.get("lang", "en"),
                    image_path=os.path.join("uploads", filename),
                    soil_type=soil_type,
                    confidence=f"{confidence:.2f}",
                    recommended_crops=recommended_crops,
                )
            except Exception as e:
                return render_template(
                    "soil.html",
                    languages=LANGUAGES,
                    selected_lang=session.get("lang", "en"),
                    error=f"Error processing image: {str(e)}",
                )

        return render_template(
            "soil.html",
            languages=LANGUAGES,
            selected_lang=session.get("lang", "en"),
            error="Invalid file type",
        )

    return render_template(
        "soil.html",
        languages=LANGUAGES,
        selected_lang=session.get("lang", "en"),
    )


@app.route("/marketplace")
def marketplace():
    return render_template(
        "marketplace.html",
        products=products,
        languages=LANGUAGES,
    )


@app.route("/weather")
def weather():
    return render_template(
        "weather.html",
        languages=LANGUAGES,
    )


@app.route("/api/weather")
def get_weather():
    try:
        location = request.args.get("location")

        if location:
            # Get coordinates from location name
            coords = geocode_location(location)
            if coords is None:
                return jsonify({"error": "Location not found"}), 404
            lat, lon = coords
        else:
            # Use provided coordinates (fallback to Berlin)
            lat = float(request.args.get("lat", 52.52))
            lon = float(request.args.get("lon", 13.41))

        days = int(request.args.get("days", 7))
        weather_data = get_weather_data(lat, lon, days)

        # Add weather icons
        for day in weather_data["daily"]:
            day["icon"] = get_weather_icon(int(day["weathercode"]))

        return jsonify(weather_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/speak_disease/<lang>")
def speak_disease(lang):
    description = request.args.get("description", "")
    prevention = request.args.get("prevention", "")

    if lang in tts.languages.values():
        success = tts.speak_disease_info(description, prevention, lang)
        return jsonify({"success": success})
    else:
        return jsonify({"success": False, "error": "Language not supported"})


@app.route("/stop_speech")
def stop_speech():
    tts.stop_speaking()
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)
