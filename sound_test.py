import sounddevice as sd
import numpy as np
import keyboard
import requests
import runpod_test
import ai_skeleton
from dotenv import load_dotenv
import os
import soundfile as sf
import pygame
import sys
import upload_audio
import string
import random



    

# Call the function


class Recorder:
    def __init__(self, fs=16000):
        self.fs = fs
        self.is_recording = False
        self.frames = []

    def start_recording(self):
        print("Recording Audio")
        self.is_recording = True
        self.frames = []
        self.stream = sd.InputStream(callback=self.callback, channels=1, samplerate=self.fs, dtype='float32')
        self.stream.start()

    def stop_recording(self):
        print("Audio recording complete")
        self.is_recording = False
        self.stream.stop()
        self.stream.close()

    def callback(self, indata, frames, time, status):
        if self.is_recording:
            self.frames.append(indata.copy())

    def play_recording(self):
        if not self.is_recording and len(self.frames) > 0:
            print("Play Audio")
            self.recording = np.concatenate(self.frames) 
            sd.play(self.recording, self.fs)
            sd.wait()
            print("Play Audio Complete")

    def save_recording(self, filename):
        if not self.is_recording and len(self.frames) > 0:
            self.recording = np.concatenate(self.frames)  
            sf.write(filename, self.recording, self.fs)



# Call the function


recorder = Recorder()
print("Welcome to the skeleton fortuneteller")
pygame.mixer.init()
pygame.mixer.music.load("greetings.mp3")
pygame.mixer.music.play()

def generate_random_string(length=9):
    # Define the characters that will be used
    alphabet = string.ascii_letters + string.digits

    # Use random.choice to select characters randomly
    return ''.join(random.choice(alphabet) for i in range(length))


def toggle_recording(e):  
    try:          
        if not recorder.is_recording:
            recorder.start_recording()
        else:
            load_dotenv()
            source = os.getenv("SOURCE")
            destination = os.getenv("DESTINATION")
            recorder.stop_recording()
            file_path = generate_random_string()+".wav"
            recorder.save_recording(file_path)
            upload_audio.uploadAudio(file_path,source,destination)
            pygame.mixer.music.load("interesting.mp3")
            pygame.mixer.music.play()
            text_to_speak = runpod_test.get_transcription(file_path)  
            ai_skeleton.play_audio(text_to_speak)
            pygame.mixer.music.load("listening.mp3")
            pygame.mixer.music.play()
            os.remove(os.path.join(source, file_path))  
    except Exception as e:
        print(e)
        sys.exit(1)


keyboard.on_press_key("space", toggle_recording)

keyboard.wait()
