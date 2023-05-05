from matplotlib import pyplot as plt
import numpy as np
import scipy.io.wavfile as wav
from base_morse_coder import BaseMorseCoder

class Morse2WaveFile(BaseMorseCoder):
    
    def enter_phrase(self, ctx, param):
        param['output'] = np.empty((0,))
        param['time'] = 0.0
        param['log'] = []
        param['log'].append((param['time'], "ENTER PHRASE", ctx))

    def exit_phrase(self, ctx, param):
        # # plt.xlim(0, 8192)
        # plt.plot(np.concatenate((param['dit'], param['gap1'], param['dah'])))
        # plt.title('Morse letter "A"')
        # plt.show()
        param['log'].append((param['time'], "EXIT PHRASE", ctx))
        wav.write(param['output_file'], param['sample_rate'], param['output'].astype(np.float32))

    def enter_group(self, ctx, param):
        param['log'].append((param['time'], "ENTER GROUP", ctx))

    def exit_group(self, ctx, param):
        param['log'].append((param['time'], "EXIT GROUP", ctx))

    def enter_char(self, ctx, param):
        param['log'].append((param['time'], "ENTER CHAR", ctx))

    def exit_char(self, ctx, param):
        param['log'].append((param['time'], "EXIT CHAR", ctx))
    
    def visit_dit(self, ctx, param) -> None:
        param['log'].append((param['time'], "START DIT", ctx))
        param['output'] = np.concatenate((param['output'], param['dit']))
        param['time'] += param['dit_time']
        param['log'].append((param['time'], "STOP DIT", ctx))

    def visit_dah(self, ctx, param) -> None:
        param['log'].append((param['time'], "START DAH", ctx))
        param['output'] = np.concatenate((param['output'], param['dah']))
        param['time'] += param['dah_time']
        param['log'].append((param['time'], "STOP DAH", ctx))
    
    def visit_gap1(self, ctx, param) -> None:
        param['log'].append((param['time'], "START GAP1", ctx))
        param['output'] = np.concatenate((param['output'], param['gap1']))
        param['time'] += param['gap1_time']
        param['log'].append((param['time'], "STOP GAP1", ctx))
    
    def visit_gap3(self, ctx, param) -> None:
        param['log'].append((param['time'], "START GAP3", ctx))
        param['output'] = np.concatenate((param['output'], param['gap3']))
        param['time'] += param['gap3_time']
        param['log'].append((param['time'], "STOP GAP3", ctx))
    
    def visit_gap7(self, ctx, param) -> None:
        param['log'].append((param['time'], "START GAP7", ctx))
        param['output'] = np.concatenate((param['output'], param['gap7']))
        param['time'] += param['gap7_time']
        param['log'].append((param['time'], "STOP GAP7", ctx))
