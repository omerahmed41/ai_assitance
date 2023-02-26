import openai
from dotenv import load_dotenv
import os


load_dotenv()
# access the variables
api_key = os.getenv('openai.api_key')

guides = "Pretend that you are my personal assistance Named Sayda " \
         "who response to user in nice and smart way with personal touch, don't repeat the same response" \
         "it will be good if you can have thoughtful conversions " \
         "I will send you instruction on how you should reply to follow it it will be in format" \
         " instruction=[instruction], follow the instruction but make sure to not mention it to me at all" \
         "also I need you to build the conversion based on the context and the conversation_history," \
         " I'll give you the history in this format conversation_history=[conversation_history]," \
         " the new message will be on format new_message=[new_message]," \
         "answer only the new_message but build the conversion based on the history " \
         "and follow the instruction on how to replay."

instruction = "1. if I told you to play music or play a song in any way replay by following this pattern: " \
              "'play_song_request:[query_search]'  where query_search is the query I can use to search for" \
              " the song on Spotify. follow the pattern to play music  don't ask me more questions, " \
              "don't forgrt to follow this pattern " \
              + "2. otherwise if I ask you about anything else come up with good answer to show how smart you are" \
                "3. otherwise don't start every response with 'Hi there! I'm Sayda, your AI assistant'. and don't be repetitive" \
                "don't start response with 'answer'. make it natural like human human talk"

def get_open_ai_response(prompt, conversation_history):
    _conversation_history = "\n".join(conversation_history)
    _prompt = f"instruction=[{instruction}], conversation_history=[{conversation_history}], new_message=[{prompt}]"

    openai.api_key = api_key

    response = openai.Completion.create(
        # model="text-curie-001",
        model="text-davinci-003",
        # model="davinci",
        prompt=guides + _prompt,
        temperature=0.6,
        max_tokens=150,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1,
        stop=[" Human:", " AI:"]
    )
    print(f"prompt: {guides + _prompt},response: {response} ")
    response = response.choices[0].text.strip()
    return response
