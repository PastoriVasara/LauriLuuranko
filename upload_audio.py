import shutil
import subprocess
import os
import tempfile

def uploadAudio(file_name, source, destination):
    
    source_directory = source
    destination_directory = destination
    commit_message = "Add audio file"

    # Change directory to the destination
    os.chdir(destination_directory)

    # Remove existing .wav files
    existing_files = [f for f in os.listdir() if f.endswith('.wav')]
    for f in existing_files:
        subprocess.run(["git", "rm", f])

    # Copy the new file to the destination directory
    shutil.copy(os.path.join(source_directory, file_name), destination_directory)

    # Run git commands to add the new file and make a commit
    subprocess.run(["git", "pull"])
    subprocess.run(["git", "add", file_name])
    subprocess.run(["git", "commit", "-m", commit_message])
    subprocess.run(["git", "push"])

    # Change back to the original directory
    os.chdir(source_directory)