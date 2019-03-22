import numpy as np
import matplotlib.pyplot as plt
import wave
from soundfile import SoundFile
from pandas import DataFrame


def draw_plot(audio_file):
    """
    Draw a signal as a plot
    :param audio_file: String - path to audio file (.wav)
    :return: Return signal plot (x - time, y - amplitude)
    """
    spf = wave.open(audio_file, 'r')
    signal = np.fromstring(spf.readframes(-1), 'Int16')
    plt.figure(1)
    plt.plot(signal)
    return plt.show()


def get_audio_total_sample(audio_file):
    """
    Get audio file total sample amount
    :param audio_file: String - path to audio file (.wav)
    :return: Return total sample amount in audio file
    """
    f = SoundFile(audio_file)
    return len(f)


def get_audio_sample_rate(audio_file):
    """
    Get sample rate
    :param audio_file: String - path to audio file (.wav)
    :return: Return sample rate
    """
    f = SoundFile(audio_file)
    return f.samplerate


def put_signal_to_dataframe(audio_file):
    """
    Present audio signal as a dataframe
    :param audio_file: String - path to audio file (.wav)
    :return: Return dataframe with two columns: amplitude and sample number
    """
    spf = wave.open(audio_file, 'r')
    signal = np.fromstring(spf.readframes(-1), 'Int16')
    df = DataFrame(signal)
    df['sample'] = [i for i in range(get_audio_total_sample(audio_file=audio_file))]
    return df


def get_last_sample_of_start_silence(audio_file):
    """
    Check where ends silence at the beginning of audio signal
    :param audio_file: String - path to audio file (.wav)
    :return: Return number of last sample of beginning silence
    """
    from_silence_to_noise = 50
    dataframe = put_signal_to_dataframe(audio_file=audio_file)
    start_silence = 0
    start_signal_index = 0
    for sample_ampli in dataframe[0]:
        start_signal_index += 1
        if abs(sample_ampli) > from_silence_to_noise:
            start_silence += 1
        if start_silence > 50:
            break
    return start_signal_index


def get_first_sample_of_end_silence(audio_file):
    """
    Check where starts silence at the end of audio signal
    :param audio_file: String - path to audio file (.wav)
    :return: Return number of first sample of ending silence
    """
    from_silence_to_noise = 50
    dataframe = put_signal_to_dataframe(audio_file=audio_file)
    end_silence = 0
    end_signal_index = get_audio_total_sample(audio_file)
    for sample_ampli in reversed(dataframe[0]):
        end_signal_index -= 1
        if abs(sample_ampli) > from_silence_to_noise:
            end_silence += 1
        if end_silence > 50:
            break
    return end_signal_index


def valid_audio(audio_file):
    """
    Valid if signal is broken - if contains silence gap
    :param audio_file: String - path to audio file (.wav)
    :return: Return 'valid' if signal is valid, otherwise return 'invalid' and first sample of silence gap
    """
    min_samples_number_in_gap = 130
    high_frequency = 1500  # frequency recognized as high
    sudden_idx_distance = 200  # indexes distance - if high_frequency found in sudden_idx_distance before found silence gap,

    dataframe = put_signal_to_dataframe(audio_file=audio_file)
    end_of_start_silence = get_last_sample_of_start_silence(audio_file)
    start_of_end_silence = get_first_sample_of_end_silence(audio_file)

    start_gap_sample = 0
    gap_length = 0
    invalid = False
    last_high_frequency_idx = 0
    for idx, sample_ampli in enumerate(dataframe[0]):
        if sample_ampli > high_frequency:
            last_high_frequency_idx = idx
        if end_of_start_silence <= idx < start_of_end_silence:
            if idx - last_high_frequency_idx < sudden_idx_distance:
                if abs(sample_ampli) <= 1:
                    start_gap_sample = idx
                    gap_length += 1
                else:
                    gap_length = 0
                if gap_length >= min_samples_number_in_gap:
                    invalid = True
                    return "{} {}".format('invalid', start_gap_sample - min_samples_number_in_gap)

    if not invalid:
        return '{}'.format('valid')
