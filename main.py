import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
from datetime import datetime

# Initialize recognizer and speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
genai.configure(api_key="AIzaSyCNB0bEJYtGKU0tiDnc6VWaudebTM5F5CY")  

# Speak out loud
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Get AI response or built-in commands
def ai_response(prompt):
    prompt = prompt.lower()

    # Handle built-in commands
    if "time" in prompt:
        return datetime.now().strftime("The time is %I:%M %p")
    elif "date" in prompt:
        return datetime.now().strftime("Today's date is %B %d, %Y")
    
    # Otherwise, call Gemini
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip().split('\n')[0]  # One-line reply

# Main
if __name__ == "__main__":
    
    speak("Jarvis online. Say 'Jarvis' to begin.")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word 'Jarvis'...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, phrase_time_limit=3)
                wake_word = recognizer.recognize_google(audio).lower()

                if "jarvis" in wake_word:
                    speak("Yes?")
                    with sr.Microphone() as source:
                        print("Listening to your question...")
                        recognizer.adjust_for_ambient_noise(source, duration=1)
                        audio = recognizer.listen(source, phrase_time_limit=6)
                        question = recognizer.recognize_google(audio)

                        print("You said:", question)  #  Print your speech
                        reply = ai_response(question)
                        print("Jarvis:", reply)
                        speak(reply)

        except sr.UnknownValueError:
            print("Didn't catch that.")
        except sr.RequestError as e:
            print("Speech recognition request error:", e)
        except Exception as e:
            print("Error:", e)