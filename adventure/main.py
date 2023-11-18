import curses
import adventuregame
import chatgpt
import chathistory
import gamedisplay
from logutils import log

MAX_TURNS = 100

def main(display: gamedisplay.Display):
    history = chathistory.ChatHistory()

    chat = chatgpt.ChatGPT(debug=True)

    with adventuregame.AdventureGame() as game:
        # get the initial output of the game
        history.add_gameplay(game.read())
        display.add_text(history.read())

        for k in range(MAX_TURNS):
            # get the model's response to the game 
            command = chat.respond(history.get_messages())
            display.add_thinking(history.add_model_response(command))

            # get the output of the game, given the model's response
            game.play(command)
            history.add_gameplay(game.read())

            # display the game for the user
            display.add_gameplay(history.read())
            display.update()

            # allow the user to give chatgpt a hint
            hint = display.hint_prompt()
            if hint:
                display.add_hint(hint)
                history.add_user_hint(hint)
                display.update()

            display.loading()

if __name__ == "__main__":
    curses.wrapper(lambda stdscr: main(gamedisplay.Display(stdscr)))