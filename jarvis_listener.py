import speech_recognition as sr
import requests
import time

# REST API Endpoint
# receives {"command":"whatever you want to execute"}
# returns status_code + msg
WEB_SERVICE_URL = "http://localhost:8080/command_exec" 

def send_command(command):
    """sends the transcribed command to the web service"""
    try:
        response = requests.post(WEB_SERVICE_URL, json={"command": command})
        print(f"Response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Failed to send command: {e}")

def jarvis_listener():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Listening for 'JARVIS'...")

    while True:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            
            try:
                # Recognize speech 
                text = recognizer.recognize_google(audio).lower()
                if "jarvis" in text:
                    print("wake word detected. waiting for command...")
                    capture_command(recognizer, microphone)

            except sr.UnknownValueError:
                print("could not understand audio")
            except sr.RequestError as e:
                print(f"speech recognition fault; {e}")

def capture_command(recognizer, microphone):
    """capture the voice command after wake word"""
    phrase = []
    start_time = time.time()

    with microphone as source:
        while True:
            try:
                audio = recognizer.listen(source, timeout=5)  # silence detection after 5 secs
                command = recognizer.recognize_google(audio).lower()
                phrase.append(command)
                print(f"captured: {command}")

                # reset timer
                start_time = time.time()

            except sr.UnknownValueError:
                print("could not understand command")
            except sr.WaitTimeoutError:
                # detect a pause longer than 2 seconds
                if time.time() - start_time > 2:
                    break

    # send the complete command
    full_command = " ".join(phrase).strip()
    print(f"sending command: {full_command}")
    send_command(full_command)

if __name__ == "__main__":
    jarvis_listener()
