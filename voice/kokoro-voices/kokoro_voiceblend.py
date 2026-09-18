'''
af_kore feels most like bmo but still doesnt have that warmth.
will tweak 2 or more voices and see if we can get a better one.

we'll have 3 tests here with af_kore as baseline
'''
import os
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro


# ==========================================
# FIND BMO PROJECT FOLDER
# ==========================================

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
BMO_ROOT = os.path.dirname(os.path.dirname(THIS_DIR))


# ==========================================
# KOKORO MODEL FILES
# ==========================================

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


# ==========================================
# OUTPUT FOLDER
# ==========================================

OUTPUT_DIR = os.path.join(
    THIS_DIR,
    "bmo_variants"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==========================================
# LOAD KOKORO
# ==========================================

kokoro = Kokoro(MODEL, VOICES)


# ==========================================
# BMO TEST DIALOGUE
# ==========================================

text = """
Hey buddy!

I'm BMO.

Oh! You're back!

I was waiting for you.

Do you want to play a game?

Okay okay okay!

That sounds fun!
"""


# ==========================================
# GET BASE VOICES
# ==========================================

kore = kokoro.get_voice_style("af_kore")
sky = kokoro.get_voice_style("af_sky")
heart = kokoro.get_voice_style("af_heart")
jessica = kokoro.get_voice_style("af_jessica")
bella = kokoro.get_voice_style("af_bella")


# ==========================================
# FUNCTION TO BLEND VOICES
# ==========================================

def blend_voices(voice_a, voice_b, weight_a):
    """
    Mix two Kokoro voices.

    weight_a:
        0.0 = 100% voice B
        0.5 = 50% A + 50% B
        1.0 = 100% voice A
    """

    weight_b = 1.0 - weight_a

    return (
        voice_a * weight_a
        + voice_b * weight_b
    )


# ==========================================
# BMO VOICE EXPERIMENTS
# ==========================================

variants = {

    # --------------------------------------
    # Pure baseline
    # --------------------------------------

    "01_af_kore": {
        "voice": kore,
        "speed": 1.00
    },


    # --------------------------------------
    # Kore + Sky
    # Softer / lighter
    # --------------------------------------

    "02_kore_sky_80_20": {
        "voice": blend_voices(kore, sky, 0.80),
        "speed": 1.05
    },

    "03_kore_sky_70_30": {
        "voice": blend_voices(kore, sky, 0.70),
        "speed": 1.05
    },

    "04_kore_sky_60_40": {
        "voice": blend_voices(kore, sky, 0.60),
        "speed": 1.05
    },


    # --------------------------------------
    # Kore + Heart
    # Warmer / friendlier
    # --------------------------------------

    "05_kore_heart_80_20": {
        "voice": blend_voices(kore, heart, 0.80),
        "speed": 1.03
    },

    "06_kore_heart_70_30": {
        "voice": blend_voices(kore, heart, 0.70),
        "speed": 1.03
    },

    "07_kore_heart_60_40": {
        "voice": blend_voices(kore, heart, 0.60),
        "speed": 1.03
    },


    # --------------------------------------
    # Kore + Jessica
    # More expressive / animated
    # --------------------------------------

    "08_kore_jessica_80_20": {
        "voice": blend_voices(kore, jessica, 0.80),
        "speed": 1.04
    },

    "09_kore_jessica_70_30": {
        "voice": blend_voices(kore, jessica, 0.70),
        "speed": 1.04
    },


    # --------------------------------------
    # Kore + Bella
    # More warmth / emotion
    # --------------------------------------

    "10_kore_bella_80_20": {
        "voice": blend_voices(kore, bella, 0.80),
        "speed": 1.03
    },

    "11_kore_bella_70_30": {
        "voice": blend_voices(kore, bella, 0.70),
        "speed": 1.03
    },
}


# ==========================================
# GENERATE ALL VARIANTS
# ==========================================

print()
print("======================================")
print("        BMO VOICE LAB")
print("======================================")
print()


for name, settings in variants.items():

    print(f"Generating: {name}")

    samples, sample_rate = kokoro.create(
        text,
        voice=settings["voice"],
        speed=settings["speed"],
        lang="en-us"
    )

    output_file = os.path.join(
        OUTPUT_DIR,
        f"{name}.wav"
    )

    sf.write(
        output_file,
        samples,
        sample_rate
    )

    print(f"Saved: {output_file}")
    print()


print("======================================")
print("All BMO voice variants created!")
print("======================================")