import os
import traceback
from openai import OpenAI
import requests
import speech_recognition as sr
from dotenv import load_dotenv
import json
# Initialize recognizer
recognizer = sr.Recognizer()
load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

lifx_token = os.environ.get("LIFX_KEY")

headers = {
    "Authorization": "Bearer %s" % lifx_token,
}

# Function to capture and transcribe speech
def transcribe_speech():
    with sr.Microphone() as source:
        print("Listening...")
        # Adjusts for ambient noise and listens
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
    
    try:
        # Transcribe speech using Google Speech Recognition
        print("Transcribing...")
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        return None
    
def parse_transcript(transcript):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role":"system",
                    "content":'''
                        You are an AI that listens to voice commands and converts them into a specific JSON format. Your job is to output only the final JSON string, with no additional text or explanations.

                        Color commands: If the command involves changing a color (e.g., 'change the color to green'), output:
                        {"color": "<color_value>"}
                        Example: 'change the color to green' becomes {"color": "green"}.

                        Power commands: If the command involves turning the power on or off (e.g., 'turn the power on' or 'turn the device off'), output:
                        {"power": "<on_or_off>"}
                        Example: 'turn the power on' becomes {"power": "on"}.

                        Make sure the JSON is formatted correctly with double quotes and that only one JSON output is generated based on the command. Do not output anything else except the JSON string.
                    '''
                },
                {
                    "role": "user",
                    "content": transcript
                }
            ],
            model="gpt-4o",
        )
        command = chat_completion.choices[0].message.content
        return command
    except:
        print("Failed")
        traceback.print_exc()
        return None

# Run the transcription function
if __name__ == "__main__":
    transcript = transcribe_speech()
    while transcript != "stop":
        if transcript is not None:
            payload_text = parse_transcript(transcript)
            print(payload_text)
            try:
                payload = json.loads(payload_text)
                response = requests.put('https://api.lifx.com/v1/lights/all/state', data=payload, headers=headers)
            except Exception:
                print("fuck no")
            
            transcript = transcribe_speech()
    

