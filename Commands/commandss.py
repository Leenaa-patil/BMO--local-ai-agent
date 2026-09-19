import webbrowser
import subprocess

def browser_commands(command):
 command = command.lower()
 
 try:
 # Websites    
    if "open google" in command:
        webbrowser.open("https://google.com")
    elif "open brave" in command:
        webbrowser.open("https://brave.com")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
    elif "open github" in command:
        webbrowser.open("https://github.com")

 # Applications 
    elif "open vscode" in command:
        subprocess.Popen("code")

    elif "open notepad" in command:
        subprocess.Popen("notepad")

    elif "open calculator" in command:
        subprocess.Popen("calc")

    elif "open paint" in command:
        subprocess.Popen("mspaint")

    elif "open command prompt" in command:
        subprocess.Popen("cmd")

    elif "open powershell" in command:
        subprocess.Popen("powershell")

    elif "open task manager" in command:
        subprocess.Popen("taskmgr")     
 except Exception as e:
     print(f"sorry could not open that app. {e}")       
