import subprocess
import psutil
import pyttsx3
import pyautogui
import speech_recognition as sr
import os

# Initialize the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.say("Hi, I am Malware.")
engine.runAndWait()

# Coordinates for Chrome profiles and YouTube (example coordinates, these need to be adjusted based on actual screen)
profile_coords = {
    "minhaj": (626, 471),
    "minhaj uhr": (797, 450),
    "work": (968, 518),
    "youtube to ": (459, 576),  # Replace with the actual coordinates for the YouTube shortcut
    "gmail 2": (55, 110),    # Replace with actual coordinates for the Gmail shortcut
    "search bar": (400, 60),
    "youtube search bar":(469,113),
    "it":(669,458),
    "skip":(831,537),
    "home":(142,111),
    "next":(971,265),
    "email one":(325,277),
    "email 2":(306,322),
    "mail":(121,120)
}

def open_application(app_name):
    try:
        # Map app names to their respective commands
        app_commands = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            # Add more applications and their commands here
        }
        
        # Get the command for the specified app
        app_command = app_commands.get(app_name)
        
        if app_command:
            # Open the application using subprocess
            subprocess.Popen(app_command)
            print(f"Opening {app_name}...")
        else:
            print("Application not found.")
    except Exception as e:
        print(f"Error: {e}")

def close_application(app_name):
    for proc in psutil.process_iter():
        try:
            if app_name.lower() in proc.name().lower():
                proc.kill()
                print(f"Closing {app_name}...")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    print(f"Application {app_name} is not running.")

def minimize_window():
    pyautogui.hotkey('win', 'down')

def maximize_window():
    pyautogui.hotkey('win', 'up')

def restore_down_window():
    pyautogui.hotkey('win', 'down')

def click_profile(profile_name):
    coords = profile_coords.get(profile_name)
    if coords:
        pyautogui.moveTo(coords)
        pyautogui.click()
        print(f"Clicked on profile: {profile_name}")
    else:
        print("Profile not found.")
        engine.say("Profile not found.")
        engine.runAndWait()

def type_text(text):
    pyautogui.write(text, interval=0.1)
    pyautogui.press('enter')

def delete_text():
    # Assuming the search bar is already selected, delete the existing text
    pyautogui.hotkey('ctrl', 'a')  # Select all text
    pyautogui.press('backspace')   # Delete the selected text

def listen_for_commands():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for commands...")
        engine.say("Listening for commands")
        engine.runAndWait()
        recognizer.adjust_for_ambient_noise(source)  # Adjust for noise
        audio = recognizer.listen(source)
    
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"Command: {command}")
        
        if "open" in command:
            app_name = command.replace("open", "").strip()
            open_application(app_name)
        elif "close" in command:
            app_name = command.replace("close", "").strip()
            close_application(app_name)
        elif "minimise" in command:
            minimize_window()
        elif "full screen" in command:
            maximize_window()
        elif "select" in command:
            profile_name = command.replace("select", "").strip()
            click_profile(profile_name) 
        elif "type" in command:
            text_to_type = command.replace("type", "").strip()
            type_text(text_to_type)
        elif "please recycle the text" in command:
            delete_text()
        elif "please quit" in command:
            engine.say("I don't have any interest to waste time for you, I have a lot of job, so go to hell buddy")
            engine.runAndWait()
            print("I don't have any interest to waste time for you, I have a lot of job, so go to hell buddy..")
            return "quit"
        elif "ahead" in command:
            scroll_page("up")
        elif "down" in command:
            scroll_page("down")
        else:
            print("Command not recognized.")
            engine.say("Command not recognized.")
            engine.runAndWait()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand your command.")
        engine.say("Sorry, I couldn't understand command.")
        engine.runAndWait()
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        engine.say(f"Could not request results from Google Speech Recognition service; {e}.")
        engine.runAndWait()


def scroll_page(direction):
    if direction == "up":
        pyautogui.scroll(800)  # Adjust the scroll amount as needed
    elif direction == "down":
        pyautogui.scroll(-800)              

def restore_notepad():
    # Assuming "notepad" is the window title, you may need to adjust it based on your system
    pyautogui.hotkey('alt', 'tab')  # Switch to the previous window

def main():
    while True:
        if listen_for_commands() == "quit":
            break

if __name__ == "__main__":
    main()
