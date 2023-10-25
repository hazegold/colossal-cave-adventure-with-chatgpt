import datetime
import os
import openai
import dotenv
import chatgptutils

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

START_DELIM = "[START]"
END_DELIM = "[END]"

class ChatGPT:
    # When in debug mode, responses are logged in two forms.
    # 1. Human readable, with the user's input and the model's response.
    # 2. Response only, with only the model's response, so that it can be loaded into a FakeChatGPT for debugging purposes.
    debug: bool
    logfile_humanreadable: str
    logfile_responseonly: str

    def __init__(self, debug: bool = False):
        self.debug = debug
        self.logfile_humanreadable = f"logs/chatgpt-{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-humanreadable.log"
        self.logfile_responseonly = f"logs/chatgpt-{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-responseonly.log"

    @chatgptutils.ratelimited(interval=3)
    def respond(self, messages) -> str:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        response_message = response["choices"][0]["message"]["content"]
        if self.debug:
            self.log_humanreadable("\n".join([str(m) for m in messages]))
            self.log_humanreadable(response_message)
            self.log_responseonly(response_message)
        return response_message
    
    def log_humanreadable(self, text):
        with open(self.logfile_humanreadable, 'a') as file:
            file.write(f"{START_DELIM}{text}{END_DELIM}\n")

    def log_responseonly(self, text):
        with open(self.logfile_responseonly, 'a') as file:
            file.write(f"{START_DELIM}{text}{END_DELIM}")


class FakeChatGPT:
    # FakeChatGPT is used for debugging purposes
    # It can be initialized with a -responseonly.log file, which is a log of responses from a ChatGPT instance
    #   Example: `chat = chatgpt.FakeChatGPT(responsefile="logs/chatgpt-2023-10-25-07-14-38-responseonly.log")`.
    # Alternatively, it can be initialized with a list of responses directly.
    #   Example: `chat = chatgpt.FakeChatGPT(responses=["west", "south", "east"])`.
    responses: list[str]
    ind: int

    def __init__(self, responsefile: str=None, responses: list[str]=None):
        if responsefile is not None:
            with open(responsefile, 'r') as file:
                self.responses = [item.strip(START_DELIM) for item in file.read().split(END_DELIM) if item != ""]
        else:
            self.responses = responses
        self.ind = 0

    def respond(self, messages) -> str:
        msg = self.responses[self.ind % len(self.responses)]
        self.ind += 1
        return msg
