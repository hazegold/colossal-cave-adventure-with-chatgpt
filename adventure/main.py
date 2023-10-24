import sys
import time
import adventuregame
import chatgpt
import chathistory

# TODO - uses curses to manage the terminal display
# TODO - debug issues with 3.5 failing to interact with the game 

MAX_TURNS = 20
PROMPT = """Input a command to continue playing the game.
You should always attempt to input a valid command, even if previous commands failed."""

def main():
    history = chathistory.ChatHistory()
    history.add_system_prompt(PROMPT)

    with adventuregame.AdventureGame() as game:
        history.add_gameplay(game.read())
        print(history.read())

        for k in range(MAX_TURNS):
            response = chatgpt.respond(history.get_messages())
            history.add_model_response(response)
            game.play(response)
            history.add_gameplay(game.read())
            print(history.read())

            time.sleep(5)

if __name__ == "__main__":
    main()