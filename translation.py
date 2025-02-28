import json
import os
from flask import session


def load_translations(lang_code):

    try:
        path = f"translations/locales/{lang_code}.json"
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except:
        # Fallback to English
        with open("translations/locales/en.json", encoding="utf-8") as f:
            return json.load(f)


def get_translation(key, lang_code=None):
    if not lang_code:
        lang_code = session.get("lang", "en")

    translations = load_translations(lang_code)
    keys = key.split(".")
    value = translations
    for k in keys:
        value = value.get(k, key)
    return value
