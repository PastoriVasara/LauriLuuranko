import requests
from dotenv import load_dotenv
import os

def get_transcription():
    load_dotenv()
    url = "https://api.runpod.ai/v2/faster-whisper/run"
    status = "https://api.runpod.ai/v2/faster-whisper/status/"
    API_KEY = os.getenv("RUN_POD_API")
    voice_url = os.getenv("audio_url")
    payload = {"input": {
        "audio": voice_url,
        "model": "large-v2",
        "transcription": "plain text",
        "translate": False,
        "temperature": 0,
        "best_of": 5,
        "beam_size": 5,
        "suppress_tokens": "-1",
        "condition_on_previous_text": False,
        "temperature_increment_on_fallback": 0.2,
        "compression_ratio_threshold": 2.4,
        "logprob_threshold": -1,
        "no_speech_threshold": 0.6,
        "language": "fi",
        "patience": 11,
        "length_penalty": 0,
        "initial_prompt": "string"
    }}

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
         "Authorization": "Bearer " + API_KEY
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)

    while(True):
        response = requests.get(status + response.json()["id"], headers=headers)
        #print(response.json())
        responseJson = response.json()
        if responseJson["status"] == "COMPLETED":
            returnme = ""
            for segment in responseJson['output']['segments']:
                returnme += segment['text']
            print(responseJson['output']['segments'][0]['text'])
            return returnme
            break