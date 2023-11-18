import re
import io
import collections
import textwrap
from termcolor import colored

PROMPT = """We will be playing a text adventure game together.
I will provide the gameplay scenario, and you will respond with the actions you would like to take, and narrate your thought process along the way.
I may give you hints, if you get stuck.
Try the "inventory" or "help" commands if you get stuck.
You should only respond with a command in a <command> tag and your thought process in a <thinking> tag, no other tags should be included in your response.

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


Remember you should only respond with a command in a <command> tag and your thought process in a <thinking> tag, no other tags should be included in your response.
"""

Message = collections.namedtuple('Message', ['role', 'content'])

class ChatHistory():
    human_readable: io.StringIO
    roffset: int
    messages: list[Message]

    def __init__(self):
        self.human_readable = io.StringIO()
        self.roffset = 0
        self.messages = []
        self.add_system_prompt(PROMPT)

    def add_message(self, role: str, content: str):
        self.messages.append(Message(role, content))

    def get_messages(self):
        return [m._asdict() for m in self.messages]

    def add_user_hint(self, hint: str):
        h = f"<hint>\n{hint}\n</hint>"
        self.add_message("user", h)

    def add_model_response(self, response: str):
        self.add_message("assistant", response)
        match = re.search(r'<thinking>(.*?)</thinking>', response)
        if match:
            thinking = match.group(1)
            lines = textwrap.wrap(thinking, 75)
            output = f"ChatGPT: {lines[0]}\n"
            offset = len("ChatGPT: ") * " "
            for line in lines[1:]:
                output += f"{offset}{line}\n"
            return output

    def add_gameplay(self, gameplay: str):
        g = f"<gameplay>{gameplay}</gameplay>"
        self.add_message("user", g)
        self.human_readable.write(gameplay) 

    def add_system_prompt(self, prompt: str):
        self.add_message("system", prompt)
        return prompt
    
    def read(self):
        self.human_readable.seek(self.roffset)
        content = self.human_readable.read()
        self.roffset = self.human_readable.tell()
        return f"{content}\n"