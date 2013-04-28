# L. Amber Wilcox-O'Hearn 2013
# SRILMServerPipe.py

import os, subprocess, codecs

class SRILMServerPipe:
    def __init__(self, port_number, model_path, order, unk=True):
        if unk:
            self.srilm_server = subprocess.Popen(['ngram', '-order', order, '-lm', model_path, '-server-port', port_number, '-unk'], stderr=-1)
        else:
            self.srilm_server = subprocess.Popen(['ngram', '-order', order, '-lm', model_path, '-server-port', port_number], stderr=-1)
        ack = self.srilm_server.stderr.readline()
        exected_ack = 'starting prob server on port ' + port_number + '\n'
        assert ack == exected_ack, ack

        self.srilm_server_pipe = subprocess.Popen(['telnet', 'localhost', port_number], stdin=-1, stdout=-1)

        self.stdin_byte_writer = codecs.getwriter('utf-8')(self.srilm_server_pipe.stdin)
        self.stdout = self.srilm_server_pipe.stdout
        stuff = self.stdout.readline()
        assert stuff == 'Trying 127.0.0.1...\n', stuff
        stuff = self.stdout.readline()
        assert stuff == 'Connected to localhost.\n', stuff
        stuff = self.stdout.readline()
        assert stuff == 'Escape character is \'^]\'.\n', stuff
        stuff = self.stdout.readline()
        assert stuff == 'probserver ready\n', stuff

    def log_probability(self, token_string):
        self.stdin_byte_writer.write(u' '.join(token_string) + u'\n')
        result = self.stdout.readline()
        return float(result)

    def shutdown(self):
        if hasattr(self, "srilm_server"):
            if hasattr(self.srilm_server, "pid") and self.srilm_server.pid:
                os.kill(self.srilm_server.pid, 15)
            self.srilm_server.wait()

    def __del__(self):
        self.shutdown()
