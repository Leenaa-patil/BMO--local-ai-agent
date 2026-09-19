import os
import sounddevice as sd
from kokoro_onnx import Kokoro


# Find the BMO project folder
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
BMO_ROOT = os.path.dirname(THIS_DIR)


# Kokoro model files
MODEL = os.path.join(
    BMO_ROOT,
    "models",
    "kokoro",
    "kokoro-v1.0.onnx"
)

VOICES = os.path.join(
    BMO_ROOT,
    "models",
    "kokoro",
    "voices-v1.0.bin"
)


# Load Kokoro once
kokoro = Kokoro(MODEL, VOICES)


# BMO's custom voice
kore = kokoro.get_voice_style("af_kore")
jessica = kokoro.get_voice_style("af_jessica")

bmo_voice = (
    kore * 0.70 +
    jessica * 0.30
)


def speak(text):

    samples, sample_rate = kokoro.create(
        text,
        voice=bmo_voice,
        speed=1.05,
        lang="en-us"
    )

    sd.play(samples, sample_rate)
    sd.wait()