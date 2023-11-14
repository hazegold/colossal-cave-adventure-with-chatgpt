import sys
import time
import adventuregame
import chatgpt
import chathistory
import user

MAX_TURNS = 100
PROMPT = """We will be playing a text adventure game together.
I will provide the gameplay scenario, and you will respond with the actions you would like to take, and narrate your thought process along the way.
I may give you hints, if you get stuck.
Try the "inventory" or "help" commands if you get stuck.

Here are some examples:

<example>
user: <gameplay>There is a shiny brass lamp nearby.</gameplay>
assistant: <command>take lamp</command><thinking>The lamp may be useful for showing the way in a dark place later in the game, so I will take it.</thinking>
user: <gameplay>take lamp\r\nOK</gameplay>
assistant: <command>go north</command><thinking>Now that I've taken the keys, I can explore further, maybe there is somewhere dark that I can use the lamp for.</thinking>
...
assistant: <gameplay>It is now pitch dark. If you proceed you will likely fall into a pit.</gameplay>
assistant: <command>light lamp</command><thinking>I collected a lamp earlier. I should light it now to take advantage of the light it provides.</thinking>
</example>

<example>
user: <gameplay>There are some keys on the ground here.</gameplay>
assistant: <command>take keys</command><thinking>The keys may be useful for unlocking something later, so I will take them.</thinking>
user: <gameplay>take keys\r\nOK</gameplay>
assistant: <command>go south</command><thinking>Now that I've taken the keys, I can explore further, maybe there is something I can unlock with the keys.</thinking>
user: <gameplay>You're outside door. The door is locked.</gameplay>
assistant: <command>unlock door</command><thinking>Earlier I picked up a set of keys, now I can try using them to unlock this locked door.</thinking>
</example>

<example>
user: <gameplay>You are standing at the end of a road before a small brick building. Around you is a forest. A small stream flows out of the building and down a gully.</gameplay>
assistant: <command>south</command><thinking>Heading south may lead to interesting places to explore, following the direction of the stream.</thinking>
user: <gameplay>You are in a valley in the forest beside a stream tumbling along a rocky bed.</gameplay>
assistant: <command>south</command><thinking>Continuing southward along the stream might reveal new locations or items.</thinking>
user: <gameplay>At your feet all the water of the stream splashes into a 2-inch slit in the rock. Downstream the streambed is bare rock.</gameplay>
assistant: <command>south</command><thinking>Exploring further south could uncover more about this stream or lead to other interesting discoveries.</thinking>
user: <gameplay>You are in a 20-foot depression floored with bare dirt. Set into the dirt is a strong steel grate mounted in concrete. A dry streambed leads into the depression. The grate is locked.</gameplay>
assistant: <command>inventory</command><thinking>Checking my inventory could provide insights into objects I have that might interact with the environment, like something to unlock the grate.</thinking>
user: <gameplay>You're not carrying anything.</gameplay>
assistant: <command>south</command><thinking>Since I can't interact with the grate, I should continue exploring the area, moving further south.</thinking>
user: <gameplay>You are in open forest, with a deep valley to one side.</gameplay>
assistant: <command>south</command><thinking>Further exploration of the forest might reveal more clues or areas of interest.</thinking>
user: <gameplay></gameplay>
assistant: <command>south</command><thinking>It's worth continuing to explore in this direction, even if the immediate surroundings don't change much.</thinking>
user: <gameplay></gameplay>
assistant: <command>north</command><thinking>If the surroundings stopped changing, I should probably go back the way I came and try exploring in a different direction.</thinking>
</example>
"""

def main():
    chat = chatgpt.ChatGPT(debug=True)
    # chat = chatgpt.FakeChatGPT(responsefile="logs/chatgpt-2023-10-26-06-46-26-responseonly.log")
    # chat = chatgpt.FakeChatGPT(responses=["south"])

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