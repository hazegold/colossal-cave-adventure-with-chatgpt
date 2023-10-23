import sys
import time
import adventuregame
import chatgpt

# TODO - uses curses to manage the terminal display
# TODO - debug issues with 3.5 failing to interact with the game 

MAX_TURNS = 10
PROMPT = """Input a command to continue playing the game.
You should always attempt to input a valid command, even if previous commands failed."""

def main():
    with adventuregame.AdventureGame() as game:
        for k in range(MAX_TURNS):
            game.play(chatgpt.respond(PROMPT, game.check()))
            print(game.read())
            time.sleep(5)

if __name__ == "__main__":
    main()