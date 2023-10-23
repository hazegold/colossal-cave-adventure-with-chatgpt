import sys
import time
import adventuregame
import chatgpt

MAX_TURNS = 10
PROMPT = """Input a command to continue playing the game.
You should always attempt to input a valid command, even if previous commands failed."""

def main():
    with adventuregame.AdventureGame() as game:
        for k in range(MAX_TURNS):
            game.play(chatgpt.respond(PROMPT, game.check()))
            print(game.check())
            time.sleep(10)

if __name__ == "__main__":
    main()