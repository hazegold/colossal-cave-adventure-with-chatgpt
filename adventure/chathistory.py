
import io
import collections

Message = collections.namedtuple('Message', ['role', 'content'])

class ChatHistory():
    human_readable: io.StringIO
    roffset: int
    messages: list[Message]

    def __init__(self):
        self.human_readable = io.StringIO()
        self.roffset = 0
        self.messages = []

    def add_message(self, role: str, content: str):
        self.messages.append(Message(role, content))

    def get_messages(self):
        return [m._asdict() for m in self.messages]

    def add_model_response(self, response: str):
        self.add_message("assistant", response)

    def add_gameplay(self, gameplay: str):
        s = "-" * 3 + "GAMEPLAY START" + "-" * 3
        e = "-" * 3 + "GAMEPLAY END" + "-" * 3
        # s = "GAMEPLAY:"
        # e = ""
        g = f"{s}\n{gameplay}\n{e}"
        self.add_message("user", g)
        self.human_readable.write(gameplay) 

    def add_system_prompt(self, prompt: str):
        self.add_message("system", prompt)
        return prompt
    
    def read(self):
        self.human_readable.seek(self.roffset)
        content = self.human_readable.read()
        self.roffset = self.human_readable.tell()
        return content