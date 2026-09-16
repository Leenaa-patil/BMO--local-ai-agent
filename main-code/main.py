"""
main.py - BMO's brain and body, all wired together.

Folder layout this expects (BMO/):
    APIs/api_prompt.py        -> ask_groq(question)
    commands/commandss.py     -> browser_commands(command)
    voice_test/voice.py       -> speak(text)   [BMO's actual voice, not the test file]
    code/main.py              -> THIS FILE

Run it from anywhere; it locates its siblings by walking up from this
file's own location, so you don't need to fuss with PYTHONPATH.
"""

import os
import sys

# ---------------------------------------------------------------------------
# Make BMO/APIs, BMO/commands, BMO/voice_test importable no matter where
# this script is launched from. This file lives in BMO/code/, so its parent
# is BMO/, which holds all the sibling folders.
# ---------------------------------------------------------------------------
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
BMO_ROOT = os.path.dirname(THIS_DIR)
'''for folder in ("APIs", "commands", "voice_test"):
     path = os.path.join(BMO_ROOT, folder)
     if path not in sys.path:
        sys.path.insert(0, path) '''
if BMO_ROOT not in sys.path:
    sys.path.insert(0, BMO_ROOT)

# ---------------------------------------------------------------------------
# Brain: talk to Groq
# ---------------------------------------------------------------------------
try:
    from APIs.api_prompt import ask_groq
except Exception as e:
    print(f"[main.py] Could not import ask_groq from APIs/api_prompt.py: {e}")

    def ask_groq(question):
        return "Oh no! BMO's brain circuit is unplugged. Cannot think right now, buddy!"


# ---------------------------------------------------------------------------
# Hands: open apps / websites
# ---------------------------------------------------------------------------
try:
    from commands.commandss import browser_commands
except Exception as e:
    print(f"[main.py] Could not import browser_commands from commands/commandss.py: {e}")

    def browser_commands(command):
        print("[main.py] Command system offline, skipping:", command)


# ---------------------------------------------------------------------------
# Voice: speak out loud
#
# NOTE: engine_voice_test.py is a throwaway check script, not the real
# voice module (its own docstring says so). This imports from voice.py
# instead, which should hold BMO's actual speak() function. If voice.py
# doesn't exist yet or doesn't expose speak(text), we fall back to a
# plain pyttsx3 engine so BMO can still talk while you build voice.py.
# ---------------------------------------------------------------------------
try:
    from voice_test.voice import speak  # expects: def speak(text): ...
except Exception as e:
    print(f"[main.py] Could not import speak from voice_test/voice.py: {e}")
    print("[main.py] Falling back to a basic pyttsx3 voice for now.")

    import pyttsx3

    _engine = pyttsx3.init("sapi5")

    def speak(text):
        _engine.say(text)
        _engine.runAndWait()


# ---------------------------------------------------------------------------
# Command detection: does this input want an app/website opened, or
# does it want BMO to think and reply?
# ---------------------------------------------------------------------------
COMMAND_TRIGGERS = (
    "open google", "open brave", "open youtube", "open github",
    "open vscode", "open notepad", "open calculator", "open paint",
    "open command prompt", "open powershell", "open task manager",
)


def is_command(user_text):
    lowered = user_text.lower()
    return any(trigger in lowered for trigger in COMMAND_TRIGGERS)


# ---------------------------------------------------------------------------
# BMO's main loop
# ---------------------------------------------------------------------------
def run_bmo():
    print("BMO: Beep boop! BMO is on! Type something, buddy!")
    print("BMO: (type 'quit' or 'exit' to power BMO down)\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBMO: Aw, powering down. Bye bye, best friend!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "bye", "shutdown"):
            farewell = "Bye bye! BMO will be right here, charging up for next time!"
            print(f"BMO: {farewell}")
            speak(farewell)
            break

        if is_command(user_input):
            print(f"BMO: Okay! Opening that for you now!")
            browser_commands(user_input)
            continue

        reply = ask_groq(user_input)
        print(f"BMO: {reply}")
        speak(reply)


if __name__ == "__main__":
    run_bmo()
