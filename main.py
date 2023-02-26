from UserInputHandler import UserInputHandler, listener
from utils import text_to_speech

user_input_handler = UserInputHandler()


def is_special_keyword(user_input):
    keywords = ["stop", "next"]
    for keyword in keywords:
        if keyword in user_input:
            return True
    return False


def main():
    while True:
        try:
            # user_input = input()
            user_input = listener.listen()
            print(user_input)
            if user_input in ["cedar", 'cedar', 'cider', 'Sada', 'say that']:
                listener.active = True
                text_to_speech("Tell me")
                main()
            print("listener.active: ", listener.active)
            if user_input and (listener.active or is_special_keyword(user_input)):
                pass
                user_input_handler.handle_input(user_input)
                main()

        except Exception as e:
            print("error happened", e)
            # text_to_speech("error happened")
            main()


if __name__ == '__main__':
    main()
