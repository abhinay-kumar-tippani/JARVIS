import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
from datetime import datetime
import os
import webbrowser
import pywhatkit

genai.configure(api_key="<YOUR_API_KEY>")  

recognizer = sr.Recognizer()
engine = pyttsx3.init()
chat_model = genai.GenerativeModel("gemini-1.5-flash")
chat_session = chat_model.start_chat()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def custom_commands(prompt):
    prompt = prompt.lower()

    if "open youtube" in prompt:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube"

    elif "open google" in prompt:
        webbrowser.open("https://google.com")
        return "Opening Google"

    elif "shutdown" in prompt:
        os.system("shutdown /s /t 1")
        return "Shutting down your system"

    elif "play" in prompt and "on youtube" in prompt:
        try:
            song = prompt.split("play")[1].split("on youtube")[0].strip()
            pywhatkit.playonyt(song)
            return f"Playing {song} on YouTube"
        except Exception as e:
            print("YouTube error:", e)
            return "Sorry, I couldn't play that on YouTube."

    return None

def ai_response(prompt):
    prompt = prompt.lower()

    if "time" in prompt:
        return datetime.now().strftime("The time is %I:%M %p")
    elif "date" in prompt:
        return datetime.now().strftime("Today's date is %B %d, %Y")

    command_response = custom_commands(prompt)
    if command_response:
        return command_response

    speak("Let me think...")
    try:
        response = chat_session.send_message(prompt)
        return response.text.strip().split('\n')[0]
    except Exception as e:
        print("AI Error:", e)
        return "Sorry, I couldn't process that."

if _name_ == "_main_":
    speak("Jarvis online. Say 'Jarvis' to begin.")
    
    while True:
        try:
            with sr.Microphone(2) as source:
                print("Listening for wake word 'Jarvis'...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, phrase_time_limit=3)
                wake_word = recognizer.recognize_google(audio).lower()

                if "jarvis" in wake_word:
                    speak("Yes?")
                    
                    while True:
                        with sr.Microphone(2) as source:
                            print("Listening to your question...")
                            recognizer.adjust_for_ambient_noise(source, duration=1)
                            audio = recognizer.listen(source, phrase_time_limit=6)
                            question = recognizer.recognize_google(audio)
                            print("You said:", question)

                            if any(exit_word in question.lower() for exit_word in ["stop", "thank you", "bye"]):
                                speak("Okay, going silent.")
                                break

                            reply = ai_response(question)
                            print("Jarvis:", reply)
                            speak(reply)

        except sr.UnknownValueError:
            print("Didn't catch that.")
        except sr.RequestError as e:
            print("Speech recognition request error:", e)
        except Exception as e:
            print("Error:", e)
