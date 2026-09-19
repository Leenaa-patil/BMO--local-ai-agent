'''
BMO's voice is supposed to be cute, as we were using sapi5 engine voice, it was very rough for bmo's character..
 intsead lets use kokoro and get the original like voice as i dont want to use voice of real voice artists.

af_kore feels most like bmo but still doesnt have that warmth.
will tweak 2 or more voices and see if we can get a better one.

'''

import os
import soundfile as sf
from kokoro_onnx import Kokoro


# Find the BMO project folder
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
BMO_ROOT = os.path.dirname(os.path.dirname(THIS_DIR))


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


# Load Kokoro
kokoro = Kokoro(MODEL, VOICES)


# Test sentence
text = "Hey buddy! I'm BMO. Ready to play?"


# Generate voice
samples, sample_rate = kokoro.create(
    text,
    voice="af_kore",
    speed=1.0,
    lang="en-us"
)


# Save audio
sf.write("bmo_test.wav", samples, sample_rate)

print("BMO voice created!")
