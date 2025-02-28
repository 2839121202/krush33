from gtts import gTTS
import os
from time import sleep
import threading
import pygame


class DiseaseTTS:
    def __init__(self):
        self.languages = {
            "English": "en",
            "Hindi": "hi",
            "Telugu": "te",
            "Tamil": "ta",
            "Kannada": "kn",
            "Malayalam": "ml",
            "Punjabi": "pa",
            "Urdu": "ur",
            "Bengali": "bn",
            "Odia": "or",
            "Marathi": "mr",
        }

        self.start = {
            "en": "A little bit of description,",
            "hi": "थोड़ी सी विवरण,",
            "te": "కొంత వివరం,",
            "ta": "சில விளக்கம்,",
            "kn": "ಕೆಲವು ವಿವರಗಳು,",
            "ml": "കുറഞ്ഞ വിവരം,",
            "pa": "ਥੋੜਾ ਵੇਰਵਾ,",
            "ur": "تھوڑی سی تفصیل،",
            "bn": "একটু বিবরণ,",
            "or": "ଏକ ଛୋଟ ବର୍ଣ୍ଣନା,",
            "mr": "थोडंसा वर्णन,",
        }

        self.join = {
            "en": "Prevention measures are:",
            "hi": "रोकथाम के उपाय हैं:",
            "te": "నివారణ చర్యలు ఉన్నాయి:",
            "ta": "தடுப்பு முறைகள் உள்ளன:",
            "kn": "ತಡೆ ಉಪಾಯಗಳು ಇವೆ:",
            "ml": "നിവാരണ ചെയ്യുന്ന ഉപായങ്ങൾ ഉണ്ട്:",
            "pa": "ਰੋਕਣ ਦੇ ਉੱਪਾਂ ਹਨ:",
            "ur": "روکنے کے اقدام ہیں:",
            "bn": "প্রতিরোধের উপায় হল:",
            "or": "ପ୍ରତିରୋଧ ଉପାୟ ହେଉଛି:",
            "mr": "रोखण्याचे उपाय आहेत:",
        }
        # Initialize pygame mixer for audio
        pygame.mixer.init()

    def speak_disease_info(self, description, prevention, language="en"):
        try:
            # Combine description and prevention with a pause
            text = f"{self.start[language]} {description}. ... {self.join[language]} {prevention}"

            # Create gTTS object
            tts = gTTS(text=text, lang=language, slow=False)

            # Save to temporary file
            temp_file = "temp_audio.mp3"
            tts.save(temp_file)

            # Play audio
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()

            # Wait for audio to finish
            while pygame.mixer.music.get_busy():
                sleep(0.1)

            # Clean up
            pygame.mixer.music.unload()
            os.remove(temp_file)

            return True

        except Exception as e:
            print(f"Error in text-to-speech conversion: {str(e)}")
            return False

    def stop_speaking(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()


# Example usage
if __name__ == "__main__":
    tts = DiseaseTTS()

    description_en = "Apple scab is the most common disease of apple trees. It causes dark spots on leaves and fruit."
    prevention_en = "Choose resistant varieties. Rake and destroy infected leaves. Water in early morning."

    description_hi = (
        "एप्पल स्कैब एप्पल पेड़ों की सबसे आम बीमारी है। यह पत्तों और फल पर गहरे धब्बे करता है।"
    )
    prevention_hi = "प्रतिरोधी प्रजातियों का चयन करें। संक्रमित पत्तियों को बन्द करें और नष्ट करें। सुबह के समय पानी दें।"

    # Speak in different languages
    tts.speak_disease_info(description_en, prevention_en, "en")  # English
    tts.speak_disease_info(description_hi, prevention_hi, "hi")  # Hindi
