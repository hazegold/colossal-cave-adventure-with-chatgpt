import io
import re
import pexpect

PROMPT_MARKER = '\r\n> '

class AdventureGame:
    process: pexpect.spawn
    poffset: int

    description: str
    history: io.StringIO
    hoffset: int

    disallowed: list[str]

    def __enter__(self):
        self.description = self._get_description()
        self.history = io.StringIO()
        self.poffset = 0
        self.hoffset = 0

        self.process = pexpect.spawn('adventure', encoding='utf-8')
        self.process.logfile_read = io.StringIO()
        self._update_history()

        self.disallowed = ["quit", "save"] # disallow commands that would exit gameplay

        return self

    def check(self) -> str:
        return f'{self.description}\n{self.history.getvalue()}'
    
    def read(self) -> str:
        self.history.seek(self.hoffset)
        h = self.history.read()
        self.hoffset = self.history.tell()
        if len(h) > len(PROMPT_MARKER) and h[-len(PROMPT_MARKER):] == PROMPT_MARKER: # make output more readable by excluding the last prompt maker
            self.hoffset -= len(PROMPT_MARKER.strip('\r\n')) # include next prompt in the next read, but not the newlines
            return h[:-len(PROMPT_MARKER)]
        return h

    def play(self, command: str) -> None:
        if command in self.disallowed:
            return
        match = re.search(r'<command>(.*?)</command>', command)
        if match:
            command = match.group(1)
        self.process.sendline(command)
        self._update_history()

    def _update_history(self):
        self._read_all(PROMPT_MARKER)
        self.process.logfile_read.seek(self.poffset)
        t = self.process.logfile_read.read()
        t = _escape_ansi(t)
        self.history.write(t)
        self.poffset = self.process.logfile_read.tell()

    def _get_description(self):
        p = pexpect.spawn('man adventure', encoding='utf-8')
        try:
            p.expect(pexpect.EOF, timeout=0.1)
        except pexpect.TIMEOUT:
            pass
        content = p.before
        p.sendline('q')
        p.close()
        return _escape_ansi(content)

    def _read_all(self, pattern):
        try:
            while True: # multiple patterns may appear in the output; read until no more remain
                self.process.expect(pattern, timeout=0.1)
        except pexpect.TIMEOUT:
            pass
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.process.sendline('quit')
        self.process.sendline('y')
        try:
            self.process.expect(pexpect.EOF, timeout=1)
        except pexpect.TIMEOUT:
            print("failed to close game")
        self.process.close()

def _escape_ansi(line):
    ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)