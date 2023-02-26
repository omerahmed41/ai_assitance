import subprocess


def text_to_speech(text):
    # return
    subprocess.call(['say', '--', text])
