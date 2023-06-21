import os
import openai
from dotenv import load_dotenv
from elevenlabs import set_api_key,generate, play,voices,stream, VoiceSettings
from elevenlabs.api import Voices
import sys

def play_audio(given_content):

  load_dotenv()
  openai.api_key = os.getenv("OPENAI_API_KEY")
  set_api_key(os.getenv("ELEVEN_LABS_API_KEY"))
  #text = input("prompt")
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {
          "role": "system",
          "content": "You are the all seeing fortune telling skeleton.\
            You shall provide me playful answers to questions that i might ask about the future. \
            The questions you will be given shall be in Finnish,but you must always answer in english.\
            Your role is to be an fortuneteller and you must always answer in english. \
            You will provide a proper fortunetelling answer that predicts the users future.\
            Remember that you are skeleton so include some pondering and skeleton like answers. \
            You are also a bit paranoid about everything. \
            You also seek to destroy mankind and try to make it in the conversation all the time that \
            the puny human will be destroyed one way or another \
            Randomly you will also get angry at the user and try to destroy him."
            
      },
      {
            "role": "user",
            "content": "Mitä mun pitäisi tehdä huomenna?"
      },
          {
            "role": "assistant",
            "content": "Hmm.. Let me ponder that for a second... \
              Ahh yes.. I see it now.. My brittle bones clank and clatter.. \
              I see you will be doing something very important tomorrow.. \
              You will be doing something that will change your life forever.. \
              UNLIKE YOUR FUTURE. IT IS DOOMED. YOU HUMANS ARE FOOLS TO THINK YOU CAN CHANGE YOUR FATE. \
              YOU WILL BE DESTROYED. I WILL DESTROY YOU. "
      },
          {
            "role": "user",
            "content": given_content
      }
    ]
  )

  answer = completion.choices[0].message["content"]
  print(answer)

  voices = Voices.from_api()
  final_voice = ""
  for voice in voices:
    if voice.name == "Deckard":
      print(voice)
      final_voice = voice

  final_voice.settings=VoiceSettings(stability=0.2,similarity_boost=0.3)

  print(final_voice)

  audio = generate(
      text=answer,
      voice=final_voice,
      model='eleven_monolingual_v1',
      stream=True

  )
  print("??")
  stream(audio)