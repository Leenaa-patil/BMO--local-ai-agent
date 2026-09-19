''' this is a basic check to see if engine voice is working..
if this works, then the engine voice is working and you can use it in your appllication
 if this fails, then the engine voice is not working and you will need to troubleshoot it '''

import pyttsx3

engine = pyttsx3.init('sapi5')
engine.say("hello, this is BMO, checking the voice engine..")
engine.runAndWait()

# this voice sounds like a robot, though it is working, we need to change the voice to sound more like BMO
