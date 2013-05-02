# L. Amber Wilcox-O'Hearn 2013
# SRILMServerPipe.py

import os, random, subprocess, time, telnetlib

class PostMortemExecutor:
    def __init__(self, subpobj):
        self.subpobj = subpobj

    def shutdown(self):
        if self.subpobj is not None:
            self.subpobj.kill()
        self.subpobj = None

    def __del__(self):
        self.shutdown()

class SRILMServerPipe:
    def _launch_server(self, port_number, model_path, order, unk=True, debug=True):
        if debug:
            if unk:
                try:
                    srilm_server = subprocess.Popen(['ngram', '-order', order, '-lm', model_path, '-server-port', str(port_number), '-unk', '-debug', '4'], stderr=open('logging' + str(time.time()), 'w'))
                except EnvironmentError, e:
                    raise EnvironmentError((e, 'ngram', '-order', order, '-lm', model_path, '-server-port', str(port_number), '-unk', '-debug', '4'))
            else:
                try:
                    srilm_server = subprocess.Popen(['ngram', '-order', order, '-lm', model_path, '-server-port', str(port_number), '-debug', '4'], stderr=open('logging' + str(time.time()), 'w'))
                except EnvironmentError, e:
                    raise EnvironmentError((e, 'ngram', '-order', order, '-lm', model_path, '-server-port', str(port_number), '-debug', '4'))
        else:
            if unk:
                try:
                    srilm_server = subprocess.Popen(['ngram', '-order', order, '-lm', model_path, '-server-port', str(port_number), '-unk'])
                except EnvironmentError, e:
                    raise EnvironmentError((e, 'ngram', '-order', order, '-lm', model_path, '-server-port', str(port_number), '-unk'))
            else:
                try:
                    srilm_server = subprocess.Popen(['ngram', '-order', order, '-lm', model_path, '-server-port', str(port_number)])
                except EnvironmentError, e:
                    raise EnvironmentError((e, 'ngram', '-order', order, '-lm', model_path, '-server-port', str(port_number)))
        time.sleep(3)
        if srilm_server.poll() is None:
            return srilm_server
        else:
            return None

    def __init__(self, model_path, order, unk=True, debug=False):
        tried_port_numbers = set()

        while len(tried_port_numbers) < 4:
            port_number = random.randrange(1025, 65535)
            tried_port_numbers.add(port_number)
            subpo = self._launch_server(port_number, model_path, order, unk=unk, debug=debug)
            if subpo is not None:
                self.pme = PostMortemExecutor(subpo)
                self.srilm_server_pipe = telnetlib.Telnet('localhost', port_number)
                self.srilm_server_pipe.read_until('probserver ready\n')
                return

        errmsg = "FAILURE: the SRILM server subprocess has already terminated, 3 seconds after we started it. We tried all of the following port numbers? %r Enable debug-mode of the SRILMServerPipe object and try again to learn more." % (tried_port_numbers,)
        import sys
        sys.stderr.write(errmsg)
        sys.stderr.write('\n')
        raise EnvironmentError(errmsg)

    def log_probability(self, token_string):
        self.srilm_server_pipe.write((u' '.join(token_string) + u'\n').encode('utf-8'))
        result = self.srilm_server_pipe.read_until('\n')
        return float(result)

    def shutdown(self):
        self.pme.shutdown()

    def __del__(self):
        self.shutdown()
