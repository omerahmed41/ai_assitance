from Listener import Listener
from OpenAI import get_open_ai_response
from music_player import MusicPlayer
from utils import text_to_speech, string_contain

music_player = MusicPlayer()
listener = Listener()


class UserInputHandler:
    conversation_history = []

    def __init__(self):
        pass

    def handle_input(self, user_input):
        if music_player.is_playing and listener.active:
            listener.reduce_music_volume_to_hear(5, music_player)

        if music_player.is_playing:
            if string_contain(user_input, ["stop"]):
                text_to_speech("sure")
                music_player.stop()
                return
            elif string_contain(user_input, ["next"]):
                text_to_speech("Got it")
                music_player.next_track()
                listener.active = False
                return
            elif string_contain(user_input, ["reset", "restart"]):
                UserInputHandler.conversation_history = []
                return
        response = get_open_ai_response(user_input, UserInputHandler.conversation_history)
        if not response:
            self.handle_open_ai_bad_reponse()
            return
        if len(UserInputHandler.conversation_history) > 5:
            UserInputHandler.conversation_history.remove(UserInputHandler.conversation_history[0])
        UserInputHandler.conversation_history.append(f"- Human: {user_input}, AI: {response}.")

        print("response: ", response)
        if response.lower().find("play_song_request") > -1:
            music_player.run(response[response.lower().find("play_song_request") + len("play_song_request"):])
            listener.active = False
        else:
            text_to_speech(response)

    def handle_open_ai_bad_reponse(self):
        print("sorry I didn't understand you, please say again")
        text_to_speech("sorry I didn't understand you, please say again")

