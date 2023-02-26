import subprocess


def text_to_speech(text):
    # return
    subprocess.call(['say', '--', text])


def string_contain(user_input, keywords):
    user_inputs = user_input.lower().split(" ")
    for user_input in user_inputs:
        if user_input in keywords:
            return True
    return False
