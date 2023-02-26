from Listener import Listener
from OpenAI import get_open_ai_response
from music_player import MusicPlayer
from utils import text_to_speech

music_player = MusicPlayer()
listener = Listener()
conversation_history = []


class UserInputHandler:
    def __init__(self):
        pass

    def handle_input(self, user_input):
        if music_player.is_playing:
            if "stop" in user_input:
                text_to_speech("sure")
                music_player.stop()
                return
            if "next" in user_input:
                text_to_speech("Got it")
                music_player.next_track()
                listener.active = False
                return
        print(f"You said: {user_input}")
        response = get_open_ai_response(user_input, conversation_history)
        if not response:
            self.handle_open_ai_bad_reponse()
            return
        if len(conversation_history) > 5:
            conversation_history.remove(conversation_history[0])
        conversation_history.append(f"- Human: {user_input}, AI: {response}.")

        print("response: ", response)
        if response.lower().find("play_song_request") > -1:
            music_player.run(response[response.lower().find("play_song_request") + len("play_song_request"):])
            listener.active = False
        else:
            text_to_speech(response)

    def handle_open_ai_bad_reponse(self):
        print("sorry I didn't understand you, please say again")
        text_to_speech("sorry I didn't understand you, please say again")

