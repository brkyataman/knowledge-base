import os
import subprocess
from threading import Thread


class GeniaTaggerClient:

    _input_arr = []

    def print_pos_tags(self):
        print(self._input_arr)

    def send_message(self, text):
        self._input_arr = [text]
        self._tagger.stdin.write((text + '\n').encode('utf-8'))
        self._tagger.stdin.flush()
        return True

    def reader(self, source, buffer):
        while True:
            line = source.readline()
            if line:
                line = line.rstrip().decode("utf-8")
                buffer.append(line)
                self._input_arr.append(line.split("\t"))
                print(line)
            else:
                break

    def __init__(self):
        self._linebuffer=[]
        self._tagger = self.__init_subprocess()
        self.__init_reader()

    def __init_subprocess(self):
        path_to_tagger = 'geniatagger-3.0.2/geniatagger.exe'
        dir_to_tagger = os.path.dirname(path_to_tagger)
        return subprocess.Popen(path_to_tagger, cwd=dir_to_tagger, stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, shell=False)

    def __init_reader(self):
        t = Thread(target=self.reader, args=(self._tagger.stdout, self._linebuffer))
        t.daemon = True
        t.start()
