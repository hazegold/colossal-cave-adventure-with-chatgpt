import io
import re
import pexpect

class AdventureGame:
    process: pexpect.spawn

    description: str
    history: io.StringIO
    offset: int

    def __enter__(self):
        self.description = self._get_description()
        self.history = io.StringIO()
        self.offset = 0

        self.process = pexpect.spawn('adventure', encoding='utf-8')
        self.process.logfile = io.StringIO()
        self.process.expect('>')
        self._update_history()

        return self
    
    def check(self) -> str:
        return f'{self.description}\n{self.history.getvalue()}'

    def play(self, command: str) -> None:
        self.process.sendline(command)
        self.process.expect('>')
        self._update_history()

    def _update_history(self):
        self.process.logfile.seek(self.offset)
        t = self.process.logfile.read()
        t = _escape_ansi(t)
        self.history.write(t)
        self.offset = self.process.logfile.tell()

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