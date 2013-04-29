# L. Amber Wilcox-O'Hearn 2013
# SRILMServerPipe.py

import os, subprocess, codecs, time, telnetlib

class SRILMServerPipe:
    def __init__(self, port_number, model_path, order, unk=True):
        if unk:
            self.srilm_server = subprocess.Popen(['ngram', '-order', order, '-lm', model_path, '-server-port', port_number, '-unk', '-debug', '4'], stderr=open('logging' + str(time.time()), 'w'))
        else:
            self.srilm_server = subprocess.Popen(['ngram', '-order', order, '-lm', model_path, '-server-port', port_number, '-debug', '4'], stderr=open('logging' + str(time.time()), 'w'))
        time.sleep(3)

        self.srilm_server_pipe = telnetlib.Telnet('localhost', port_number)
        self.srilm_server_pipe.read_until('probserver ready\n')

    def log_probability(self, token_string):
        self.srilm_server_pipe.write((u' '.join(token_string) + u'\n').encode('utf-8'))
        result = self.srilm_server_pipe.read_until('\n')
        return float(result)

    def shutdown(self):
        if hasattr(self, "srilm_server"):
            if hasattr(self.srilm_server, "pid") and self.srilm_server.pid:
                os.kill(self.srilm_server.pid, 15)
            self.srilm_server.wait()

    def __del__(self):
        self.shutdown()
