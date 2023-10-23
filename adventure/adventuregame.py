import io
import re
import pexpect

class AdventureGame:
    process: pexpect.spawn
    poffset: int

    description: str
    history: io.StringIO
    hoffset: int

    def __enter__(self):
        self.description = self._get_description()
        self.history = io.StringIO()
        self.poffset = 0
        self.hoffset = 0

        self.process = pexpect.spawn('adventure', encoding='utf-8')
        self.process.logfile_read = io.StringIO()
        self.process.expect('>')
        self._update_history()

        return self

    def check(self) -> str:
        return f'{self.description}\n{self.history.getvalue()}'
    
    def read(self) -> str:
        self.history.seek(self.hoffset)
        h = self.history.read()
        self.hoffset = self.history.tell()
        if len(h) > 4 and h[-4:] == '\r\n> ': # make output more readable by excluding the next prompt
            self.hoffset -= 2 # include next prompt in the next read, but not the newlines
            return h[:-4]
        return h

    def play(self, command: str) -> None:
        self.process.sendline(command)
        self.process.expect('> ')
        self._update_history()

    def _update_history(self):
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