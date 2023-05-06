from matplotlib import pyplot as plt
import numpy as np
import scipy.io.wavfile as wav
from base_morse_coder import BaseMorseCoder

class Morse2WaveFile(BaseMorseCoder):

    def __init__(self) -> None:
        self.output = np.empty((0,))
        self.time_offset = 0.0
        self.event_log = []
        super().__init__()

    def ctrl_log(self, data):
        self.event_log.append((self.time_offset, "CTRL", data))

    def enter_phrase(self, ctx):
        # param['output'] = np.empty((0,))
        # param['time'] = 0.0
        # param['log'] = []
        self.event_log.append((self.time_offset, "ENTER PHRASE", ctx))

    def exit_phrase(self, ctx):
        # # plt.xlim(0, 8192)
        # plt.plot(np.concatenate((param['dit'], param['gap1'], param['dah'])))
        # plt.title('Morse letter "A"')
        # plt.show()
        self.event_log.append((self.time_offset, "EXIT PHRASE", ctx))
        self.param['output'] = self.output
        self.param['log'] = self.event_log

    def enter_group(self, ctx):
        self.event_log.append((self.time_offset, "ENTER GROUP", ctx))

    def exit_group(self, ctx):
        self.event_log.append((self.time_offset, "EXIT GROUP", ctx))

    def enter_char(self, ctx):
        self.event_log.append((self.time_offset, "ENTER CHAR", ctx))

    def exit_char(self, ctx):
        self.event_log.append((self.time_offset, "EXIT CHAR", ctx))
    
    def visit_dit(self, ctx) -> None:
        self.event_log.append((self.time_offset, "START DIT", ctx))
        self.output = np.concatenate((self.output, self.param['dit']))
        self.time_offset += self.param['dit_time']
        self.event_log.append((self.time_offset, "STOP DIT", ctx))

    def visit_dah(self, ctx) -> None:
        self.event_log.append((self.time_offset, "START DAH", ctx))
        self.output = np.concatenate((self.output, self.param['dah']))
        self.time_offset += self.param['dah_time']
        self.event_log.append((self.time_offset, "STOP DAH", ctx))
    
    def visit_gap1(self, ctx) -> None:
        self.event_log.append((self.time_offset, "START GAP1", ctx))
        self.output = np.concatenate((self.output, self.param['gap1']))
        self.time_offset += self.param['gap1_time']
        self.event_log.append((self.time_offset, "STOP GAP1", ctx))
    
    def visit_gap3(self, ctx) -> None:
        self.event_log.append((self.time_offset, "START GAP3", ctx))
        self.output = np.concatenate((self.output, self.param['gap3']))
        self.time_offset += self.param['gap3_time']
        self.event_log.append((self.time_offset, "STOP GAP3", ctx))
    
    def visit_gap7(self, ctx) -> None:
        self.event_log.append((self.time_offset, "START GAP7", ctx))
        self.output = np.concatenate((self.output, self.param['gap7']))
        self.time_offset += self.param['gap7_time']
        self.event_log.append((self.time_offset, "STOP GAP7", ctx))
