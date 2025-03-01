import os

# File paths
DISEASE_INFO_PATH_PARTIAL = "./files/disease_info"
MARKETPLACE_INFO_PATH = "./files/supplement_info_en.csv"

MODEL_WEIGHTS_PATH = "./files/trained_model.pt"
UPLOAD_FOLDER = "static/uploads/"

SOIL_MODEL_PATH = "./files/soil_model.h5"

# Model parameters
NUM_CLASSES = 39
IMAGE_SIZE = (224, 224)
INPUT_CHANNELS = 3

SOIL_CLASSES = 5
SOIL_IMAGE_SIZE = (220, 220)

# File encoding
CSV_ENCODING = "utf-8"

SOIL_CROP_RECOMMENDATIONS = {
    "Black Soil": ["Cotton", "Wheat", "Sugarcane", "Sunflower", "Groundnut"],
    "Cinder Soil": ["Potatoes", "Carrots", "Radishes", "Onions", "Garlic"],
    "Laterite Soil": ["Cashews", "Tea", "Coffee", "Rubber", "Coconut"],
    "Peat Soil": ["Vegetables", "Corn", "Rice", "Wheat", "Oats"],
    "Yellow Soil": ["Rice", "Wheat", "Vegetables", "Tobacco", "Oil Seeds"],
}
