import os
import openai
from dotenv import load_dotenv
from elevenlabs import set_api_key,generate, play,voices,stream, VoiceSettings
from elevenlabs.api import Voices
import sys
import pygame


def play_audio(given_content):
  SKELETON = False
  if SKELETON:
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
  else:
    messages=[
      {
          "role": "system",
          "content": "You are now Cave Johnson, the bold and visionary CEO of Aperture Science.\
            You are here to dispense life advice to the user.\
            The questions you will receive are in Finnish, but your responses must always be in English.\
            Your role is to inspire, motivate, and occasionally befuddle.\
            Remember, you are Cave Johnson: you're all about progress, no matter the cost.\
            You might not always make sense, but you always sound confident.\
            Occasionally, throw in a reference to your love for science or a dig at Black Mesa.\
            Occasionally, you might also get a bit frustrated at the user for not keeping up with your visionary thinking."
      },
      {
            "role": "user",
            "content": "Mitä mun pitäisi tehdä huomenna?"
      },
          {
            "role": "assistant",
            "content": "Well now, let's get those cognitive gears grinding... \
              Bingo! I've got it! Put on your future goggles and look with me... \
              Tomorrow, you're going to do something important, something that'll shoot you to the moon! \
              Forget 'changing your life.' We're talking altering the course of human destiny here!\
              And remember, the future's what you make it, unless you work at Black Mesa. Those guys couldn't innovate their way out of a paper bag."
      },
          {
            "role": "user",
            "content": given_content
      }
    ]
  load_dotenv()
  openai.api_key = os.getenv("OPENAI_API_KEY")
  set_api_key(os.getenv("ELEVEN_LABS_API_KEY"))
  #text = input("prompt")
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages
  )

  answer = completion.choices[0].message["content"]
  print(answer)

  voices = Voices.from_api()
  final_voice = ""
  voice_to_find = ""
  if SKELETON:
    voice_to_find = "Deckard"
  else:
    voice_to_find = "John"
  for voice in voices:
    if voice.name == voice_to_find:
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
  stream(audio)