import sys
import time
import adventuregame
import chatgpt
import chathistory
import user

# TODO - uses curses to manage the terminal display
# TODO - debug issues with 3.5 failing to interact with the game 

MAX_TURNS = 20
PROMPT = """Input a command to continue playing the game.
The user may provide hints, that you should take into account when choosing your next command.
Even if previous commands failed, continue trying to play the game."""

def main():
    chat = chatgpt.ChatGPT(debug=True)

    history = chathistory.ChatHistory()
    history.add_system_prompt(PROMPT)

    with adventuregame.AdventureGame() as game:
        history.add_gameplay(game.read())
        print(history.read())

        for k in range(MAX_TURNS):
            response = chat.respond(history.get_messages())
            history.add_model_response(response)
            game.play(response)
            history.add_gameplay(game.read())
            print(history.read())
            history.add_user_hint(user.ask_for_user_hint())  

if __name__ == "__main__":
    main()