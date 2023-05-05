import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt


def interpolate_linearly(wave_table, index):
    truncated_index = int(np.floor(index))
    next_index = (truncated_index + 1) % wave_table.shape[0]
    next_index_weight = index - truncated_index
    truncated_index_weight = 1 - next_index_weight
    return truncated_index_weight * wave_table[truncated_index] + next_index_weight * wave_table[next_index]

def fade_in_out(signal, fade_length=1000):
    fade_in = (1 - np.cos(np.linspace(0, np.pi, fade_length))) * 0.5
    fade_out = np.flip(fade_in)
    signal[:fade_length] = np.multiply(fade_in, signal[:fade_length])
    signal[-fade_length:] = np.multiply(fade_out, signal[-fade_length:])
    return signal

def wave_table():
    waveform = np.sin
    wavetable_length = 64
    wave_table = np.zeros((wavetable_length,))
    for n in range(wavetable_length):
        wave_table[n] = waveform(2 * np.pi * n / wavetable_length)
    return wave_table

def gain(array, gain_dB):
    amplitude = 10 ** (gain_dB / 20)
    array *= amplitude

def output_dit():
    """
    Morse "." element
    """
    sample_rate = 44100
    f = 440
    t = 1
    wavetable_length = 64

    output = np.zeros((t * sample_rate,))

    index = 0
    index_increment = f * wavetable_length / sample_rate

    for n in range(output.shape[0]):
        # output[n] = wave_table[int(np.floor(index))]
        output[n] = interpolate_linearly(wave_table, index)
        index += index_increment
        index %= wavetable_length

    gain(output, -20)

    output = fade_in_out(output)

    plt.xlim(0, 3000)
    plt.plot(output)
    plt.show()

    wav.write('dit.wav', sample_rate, output.astype(np.float32))

def output_dah():
    """
    Morse "-" element
    """
    pass

def output_gap():
    """
    Morse "silent interval"
    """
    pass

def main():
    sample_rate = 44100
    f = 440
    t = 3
    waveform = np.sin

    wavetable_length = 64
    wave_table = np.zeros((wavetable_length,))

    for n in range(wavetable_length):
        wave_table[n] = waveform(2 * np.pi * n / wavetable_length)

    output = np.zeros((t * sample_rate,))

    index = 0
    index_increment = f * wavetable_length / sample_rate

    for n in range(output.shape[0]):
        # output[n] = wave_table[int(np.floor(index))]
        output[n] = interpolate_linearly(wave_table, index)
        index += index_increment
        index %= wavetable_length

    gain = -20
    amplitude = 10 ** (gain / 20)
    output *= amplitude

    output = fade_in_out(output)

    plt.xlim(0, 3000)
    plt.plot(output)
    plt.show()

    wav.write('sine440Hz.wav', sample_rate, output.astype(np.float32))

if __name__ == '__main__':
    main()
