import sounddevice as sd
import numpy as np
import keyboard
import dropbox
from dropbox.exceptions import AuthError
from dropbox.exceptions import ApiError
import requests
import runpod_test
import ai_skeleton
from dotenv import load_dotenv
import os
import soundfile as sf
import pygame
import sys


def upload_to_dropbox(file_path, dest_path, access_token):

    dbx = dropbox.Dropbox(access_token)
    with open(file_path, 'rb') as f:
        try:
            dbx.files_upload(f.read(), dest_path, mute=True, mode=dropbox.files.WriteMode('overwrite'))
        except AuthError as err:
            print(f"ERROR: {err}")
    print("Uploaded:", dest_path)

def get_shareable_link(dest_path, access_token,file_path):
    dbx = dropbox.Dropbox(access_token)

    try:
        shared_link_metadata = dbx.sharing_create_shared_link_with_settings(file_path)
        link = shared_link_metadata.url
        print(link)
    except ApiError as api_error:
        if 'shared_link_already_exists' in api_error.error.get_path().get_error().description:
            links = dbx.sharing_list_shared_links(path=file_path).links
            if links:
                link = links[0].url
                print(link)
        else:
            raise api_error

    

    

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

try:
    recorder = Recorder()
    print("Welcome to the skeleton fortuneteller")
    pygame.mixer.music.load("greetings.mp3")
    pygame.mixer.music.play()
  
    def toggle_recording(e):
        if not recorder.is_recording:
            recorder.start_recording()
        else:
            load_dotenv()
            recorder.stop_recording()
            recorder.save_recording("test2.wav")
            access_token = os.getenv("DROPBOX_KEY")
            file_path = 'test2.wav'  # local file path
            dest_path = '/recording.wav'  # path on Dropbox
            upload_to_dropbox(file_path, dest_path, access_token)
            text_to_speak = runpod_test.get_transcription()
            ai_skeleton.play_audio(text_to_speak)
            pygame.mixer.music.load("listening.mp3")
            pygame.mixer.music.play()
            #get_shareable_link(dest_path, access_token,des  t_path)



    keyboard.on_press_key("space", toggle_recording)

    keyboard.wait()
except Exception as e:
    print(e)
    sys.exit(1)