import os
from pprint import pprint
import numpy as np
import scipy.io.wavfile as wav

from morse_coder import Morse2WaveFile

def interpolate_linearly(wave_table, index):
    truncated_index = int(np.floor(index))
    next_index = (truncated_index + 1) % wave_table.shape[0]
    next_index_weight = index - truncated_index
    truncated_index_weight = 1 - next_index_weight
    return truncated_index_weight * wave_table[truncated_index] + next_index_weight * wave_table[next_index]

def fade_in_out(signal, fade_length):
    fade_in = (1 - np.cos(np.linspace(0, np.pi, fade_length))) * 0.5
    fade_out = np.flip(fade_in)
    signal[:fade_length] = np.multiply(fade_in, signal[:fade_length])
    signal[-fade_length:] = np.multiply(fade_out, signal[-fade_length:])
    return signal

def make_wave_table():
    waveform = np.sin
    wavetable_length = 400
    wave_table = np.zeros((wavetable_length,))
    for n in range(wavetable_length):
        wave_table[n] = waveform(2 * np.pi * n / wavetable_length)
    return wave_table

def gain(array, gain_dB):
    amplitude = 10 ** (gain_dB / 20)
    array *= amplitude

def signal(wave_table, time, pitch, gain_dB, sample_rate, fade_length):
    wavetable_length = wave_table.size
    e = int(time * sample_rate)
    output = np.zeros((e,))
    index = 0
    index_increment = pitch * wavetable_length / sample_rate
    for n in range(output.shape[0]):
        output[n] = interpolate_linearly(wave_table, index)
        index += index_increment
        index %= wavetable_length
    gain(output, gain_dB)
    output = fade_in_out(output, fade_length)
    return output

def gap(time, sample_rate):
    e = int(time * sample_rate)
    output = np.zeros((e,))
    return output

def main():
    aux_data = dict()
    character_speed_wpm = 25
    effective_speed_wpm = 25
    pitch = 400
    gain_dB = -10
    sample_rate = 48000

    slope_rise_and_fall_time = 0.010
    fade_in_out_length = int(slope_rise_and_fall_time*sample_rate)
    wave_table = make_wave_table()

    unit_period = 1.2/character_speed_wpm
    dah_period = 3 * unit_period
    farnsworth_time = (60*character_speed_wpm - 37.2*effective_speed_wpm)/(character_speed_wpm*effective_speed_wpm)
    period_between_characters = 3*farnsworth_time/19
    period_between_words = 7*farnsworth_time/19

    # aux_data['sample_rate'] = sample_rate
    aux_data['dit'] = signal(wave_table, unit_period, pitch, gain_dB, sample_rate, fade_in_out_length)
    aux_data['dit_time'] = unit_period
    aux_data['dah'] = signal(wave_table, dah_period, pitch, gain_dB, sample_rate, fade_in_out_length)
    aux_data['dah_time'] = dah_period
    aux_data['gap1'] = gap(unit_period, sample_rate)
    aux_data['gap1_time'] = unit_period
    aux_data['gap3'] = gap(period_between_characters, sample_rate)
    aux_data['gap3_time'] = period_between_characters
    aux_data['gap7'] = gap(period_between_words, sample_rate)
    aux_data['gap7_time'] = period_between_words
    dir = '.\\media\\audio' 
    if not os.path.exists(dir):
        os.makedirs(dir)
    output_file = os.path.join("media\\audio", "out2.wav")

    gen = Morse2WaveFile()
    gen.ctrl_log("OP1")
    gen.render("CQ CQ CQ DE SP5DD SP5DD K", param=aux_data)
    gen.ctrl_log("OP2")
    gen.render("    ", param=aux_data)
    gen.render("OK1FF DE SP5DD K", param=aux_data)

    wav.write(output_file, sample_rate, aux_data['output'].astype(np.float32))

    metadata_file = os.path.join("media\\audio", "out2.txt")
    with open(metadata_file, "w") as file:
        for event in aux_data['log']:
            file.write(f"{event[0]}::{event[1]}::{event[2]}\n")

if __name__ == "__main__":
    main()