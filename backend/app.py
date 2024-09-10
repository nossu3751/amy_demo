from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from dotenv import load_dotenv
import json
import os
from openai import OpenAI
import traceback

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

@app.route('/process-command', methods=['POST'])
def process_command():
    data = request.get_json()
    transcript = data.get('transcript', '').lower()
    print(transcript)
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": '''
                        You are a command parser for a smart device system. Your job is to interpret user input and convert it into a standardized command format. The commands you recognize are:

                        1. "flicker X times" where X is the number of times the device should flicker.
                        2. "change color to Y" where Y is the target color.

                        When given a user input, analyze the intent and convert it into the following format: (<command>, <value>), where "<command>" is the recognized command and "<value>" is the corresponding parameter.

                        Examples:
                        - Input: "modify the color so it becomes blue" -> Output: (change color, blue)
                        - Input: "repeat toggling 5 times" -> Output: (flicker, 5)

                    ''',
                },
                {
                    "role": "user",
                    "content": transcript
                }
            ],
            model="gpt-4o",
        )
        command = chat_completion.choices[0].message.content
        print(command)
        return jsonify(success=True, command=command)
    except:
        print("Failed")
        traceback.print_exc()
        return jsonify(success=False, message="Failed to parse command")
   
if __name__ == "__main__":
    app.run(port=5000, debug=True)