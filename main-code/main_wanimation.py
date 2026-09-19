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
import threading 
import re 
 

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

from Faces.bmo_face import BMOFace 
 

# --------------------------------------------------------------------------- 
# Brain: talk to Groq 
# --------------------------------------------------------------------------- 
try: 
    from APIs.api_prompt import ask_groq 
except Exception as e: 
    print(f"[main.py] Could not import ask_groq from APIs/api_prompt.py: {e}") 
 
    def ask_groq(question): 
        return "Oh no! BMO's brain circuit is unplugged. Cannot think right now, buddy!,Could not import ask_groq from APIs" 
 

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
# BMO's face
# ---------------------------------------------------------------------------
bmo_face = BMOFace()
 

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
# Remove emojis before sending text to the voice engine
# ---------------------------------------------------------------------------
def clean_for_speech(text):
    # Remove non-ASCII characters
    text = re.sub(r"[^\x00-\x7F]+", "", text)

    # Remove emojis and unusual symbols,
    # but keep punctuation useful for speech.
    text = re.sub(r"[*_#`]", "", text)

    # Remove markdown bullets at the beginning of lines
    text = re.sub(r"(?m)^\s*[-•]\s*", "", text)

    # BMO → Beemo for TTS- as it pronounces "BMO" as "Bee Em Oh", which is not what we want, it should be pronounced as "Beemo"
    text = re.sub(r"\bBMO\b", "Beemo", text, flags=re.IGNORECASE)


    return text.strip()

# ---------------------------------------------------------------------------
# Speak while switching between BMO's two talking faces
# ---------------------------------------------------------------------------
def talk_with_animation(text):

    clean_text = clean_for_speech(text)

    talking = False

    def animate():

        while talking:

            bmo_face.show_face("bmo-talking-face-v1")
            threading.Event().wait(0.3)

            if not talking:
                break

            bmo_face.show_face("bmo-talking-face-v2")
            threading.Event().wait(0.3)

    def start_animation():

        nonlocal talking

        talking = True

        animation_thread = threading.Thread(
            target=animate,
            daemon=True
        )

        animation_thread.start()

    speak(clean_text, on_start=start_animation)

    talking = False

    bmo_face.show_face("bmo-idle-face")


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
            bmo_face.show_face("bmo-idle-face")
            break 
 
        if not user_input: 
            continue 
 
        if user_input.lower() in ("quit", "exit", "bye", "shutdown"): 

            farewell = "Bye bye! BMO will be right here, charging up for next time!" 

            print(f"BMO: {farewell}") 

            bmo_face.show_face("bmo-happy-face")

            speak(farewell) 

            bmo_face.show_face("bmo-idle-face")

            break 
 
        if is_command(user_input): 

            print(f"BMO: Okay! Opening that for you now!") 

            bmo_face.show_face("bmo-happy-face")

            browser_commands(user_input) 

            bmo_face.show_face("bmo-idle-face")

            continue 
 
        bmo_face.show_face("bmo-idle-face")

        reply = ask_groq(user_input) 

        # Terminal keeps the original reply, including emojis
        print(f"BMO: {reply}") 

        # Voice removes emojis and talking faces animate
        talk_with_animation(reply)
         
 
 
 
if __name__ == "__main__": 
 
    bmo_thread = threading.Thread( 
        target=run_bmo, 
        daemon=True 
    ) 
 
    bmo_thread.start() 
 
    # Tkinter stays in the main thread 
    bmo_face.run()
