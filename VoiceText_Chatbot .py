import speech_recognition as sr
import requests
import pyttsx3

r = sr.Recognizer()
r.energy_threshold = 300
r.dynamic_energy_threshold = True
engine = pyttsx3.init()
engine.setProperty("rate", 175)

spoken_text = []
chat_history = []

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to communicate with Ollama
def ask_ollama(prompt, history):
    full_prompt = ""
    for q, a in history:
        full_prompt += f"User: {q}\nAssistant: {a}\n"
    full_prompt += f"User: {prompt}\nAssistant:"

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:1b",  # or any model you've pulled
                "prompt": full_prompt,
                "stream": False
            }
        )
        if response.status_code == 200:
            return response.json()["response"].strip()
        else:
            return " Ollama API error"
    except Exception as e:
        return f" Error: {str(e)}"

# Choose mode
mode = input("Press 'v' for voice input or 't' for text input: ").strip().lower()

# Voice Mode
if mode == "v":
    print("\n Voice mode started. Say something... (say 'stop' to exit)\n")

    try:
        while True:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=1)
                audio = r.listen(source, phrase_time_limit=5)
                try:
                    text = r.recognize_google(audio)
                    print("You said:", text)

                    if "stop" in text.lower():
                        print(" Exiting voice mode.\n")
                        break

                    spoken_text.append(text)
                    response = ask_ollama(text, chat_history)
                    chat_history.append((text, response))
                    print(" LLaMA:", response, "\n")
                    speak(response)



                except Exception as e:
                    print("Error:", e)

    except KeyboardInterrupt:
        print("\n Stopped manually.")

#  Text Mode
elif mode == "t":
    print("\n Text mode started. Type your messages (type 'stop' to exit):\n")
    while True:
        text = input("You: ").strip()
        if text.lower() == "stop":
            print("sa Text mode stopped.\n")
            break
        spoken_text.append(text)
        response = ask_ollama(text, chat_history)
        chat_history.append((text, response))
        print(" Bot:", response, "\n")
        speak(response)

else:
    print(" Invalid input. Please restart and press 'v' or 't'.")

# Chat Summary
if chat_history:
    print("\nConversation Summary:")
    for i, (q, a) in enumerate(chat_history, 1):
        print(f"{i}. You: {q}")
        print(f"   Bot: {a}")
