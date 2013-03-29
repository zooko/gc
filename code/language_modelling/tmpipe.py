#!/usr/bin/python

import os, subprocess, codecs

class TMPipe:
    def __init__(self, pathtotmpipeexecutable, pathtolangmod):
        self.tmpipe = subprocess.Popen([pathtotmpipeexecutable, pathtolangmod], stdin=-1, stdout=-1)
        self.stdin = self.tmpipe.stdin
        self.stdin_byte_writer = codecs.getwriter('utf-8')(self.tmpipe.stdin)
        self.stdout = self.tmpipe.stdout

    def in_vocabulary(self, token):
        self.stdin.write("v " + token + '\n')
        return int(self.stdout.readline())

    def shutdown(self):
        if hasattr(self, "tmpipe"):
            if hasattr(self.tmpipe, "pid") and self.tmpipe.pid:
                os.kill(self.tmpipe.pid, 15)
            self.tmpipe.wait()

    def __del__(self):
        self.shutdown()
