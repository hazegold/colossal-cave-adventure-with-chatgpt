import sys
import time
import adventuregame
import chatgpt
import chathistory
import user

# TODO - uses curses to manage the terminal display
# TODO - debug issues with 3.5 failing to interact with the game 

MAX_TURNS = 100
PROMPT = """Your job is to input commands to continue playing the game.\
The user may provide a hint in <hint></hint> tags.\
Do not output anything in <gameplay></gameplay> tags in your response, only the user has access to this information.\
Put your response in <command></command> tags.

Here's an example:

user: <gameplay>You are inside a building, a well house for a large spring.
There are some keys on the ground here.
There is a shiny brass lamp nearby.
There is tasty food here.
There is a bottle of water here.</gameplay>
assistant: <command>take the keys</command>
"""

def main():
    chat = chatgpt.ChatGPT(debug=True)

    history = chathistory.ChatHistory()
    history.add_system_prompt(PROMPT)

    with adventuregame.AdventureGame() as game:
        # get the initial output of the game
        history.add_gameplay(game.read())
        print(history.read())

        for k in range(MAX_TURNS):
            # get the model's response to the game 
            command = chat.respond(history.get_messages())
            history.add_model_response(command)

            # get the output of the game, given the model's response
            game.play(command)
            history.add_gameplay(game.read())

            # display the game for the user
            print(history.read())

            # allow the user to provide hints to the model 
            hint = user.ask_for_user_hint()
            if hint:
                history.add_user_hint(hint)  

if __name__ == "__main__":
    main()