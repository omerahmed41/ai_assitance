from UserInputHandler import UserInputHandler, listener, music_player
from utils import text_to_speech, string_contain

user_input_handler = UserInputHandler()


def is_special_keyword(user_input):
    keywords = ["stop", "next", "reset", "restart"]
    return string_contain(user_input, keywords)


def main():
    while True:
        try:
            # user_input = input()
            user_input = listener.listen()
            print("user_input:", user_input)
            if not user_input:
                continue

            if string_contain(user_input, ["simsima", "sarah", "sara", "cedar", 'cedar', 'cider', 'Sada', 'say that']):
                listener.active = True
                listener.reduce_music_volume_to_hear(10, music_player)
                text_to_speech("Tell me")
                continue

            print("listener.active: ", listener.active)

            if listener.active or is_special_keyword(user_input):
                user_input_handler.handle_input(user_input)
                main()

        except Exception as e:
            print("error happened", e)
            # text_to_speech("error happened")
            main()


if __name__ == '__main__':
    main()
