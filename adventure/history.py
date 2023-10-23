
import io
import collections

Message = collections.namedtuple('Message', ['role', 'content'])

# TODO - switch to using history instead of passing everything in the system prompt
class History():
    messages: list[Message]

    def __init__(self):
        self.messages = []

    def add_message(self, role: str, content: str):
        self.messages.append(Message(role, content))

    def get_messages(self):
        return [m._asdict() for m in self.messages]
    
    def add_gameplay(self, gameplay: str):
        s = "-" * 30 + "GAMEPLAY START" + "-" + 30
        e = "-" * 30 + "GAMEPLAY END" + "-" + 30
        g = f"{s}\n{gameplay}\n{e}"
        self.add_message("user", g)