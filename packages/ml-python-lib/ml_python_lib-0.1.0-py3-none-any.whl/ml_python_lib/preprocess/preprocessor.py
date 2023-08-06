import os
import tensorflow as tf

# constants
NUM_COEF_MFCC = 13
# according to https://www.researchgate.net/post/
# why_most_of_reasearchers_consider_13_MFCC_coefficients_for_analysis_of_speech_or_images


def decode_audio(audio_binary):
    audio, _ = tf.audio.decode_wav(audio_binary)
    return tf.squeeze(audio, axis=-1)


def get_label(file_path):
    parts = tf.strings.split(file_path, os.path.sep)
    return parts[-2]


def get_waveform_and_label(file_path):
    label = get_label(file_path)
    audio_binary = tf.io.read_file(file_path)
    waveform = decode_audio(audio_binary)
    return waveform, label


def get_mfcc(log_mel_spectrogram):
    mfcc = tf.signal.mfccs_from_log_mel_spectrograms(log_mel_spectrogram)
    return mfcc[..., :NUM_COEF_MFCC]


class AudioProcessor(object):
    def __init__(self, commands, frame_length=255, frame_step=128,
                 sample_rate=16000, num_mel_bins=20,
                 lower_edge_hertz=20, upper_edge_hertz=8000):
        self.sample_rate = sample_rate
        self.AUTOTUNE = tf.data.experimental.AUTOTUNE
        self.commands = commands
        self.frame_length = frame_length
        self.frame_step = frame_step
        self.num_mel_bins = num_mel_bins
        self.lower_edge_hertz = lower_edge_hertz
        self.upper_edge_hertz = upper_edge_hertz

    def get_sample_rate(self, files_ds):
        for file_path in files_ds.take(1):
            audio_binary = tf.io.read_file(file_path)
            _, sr = tf.audio.decode_wav(audio_binary)
            self.sample_rate = sr.numpy()

    def get_spectrogram(self, waveform):
        # we pad it to make the clip have same length of 1 second
        zero_padding = tf.zeros(
            self.sample_rate - tf.shape(waveform), dtype=tf.float32)
        waveform = tf.cast(waveform, tf.float32)
        equal_length = tf.concat([waveform, zero_padding], 0)
        spectrogram = tf.signal.stft(
            equal_length, frame_length=self.frame_length,
            frame_step=self.frame_step)
        spectrogram = tf.abs(spectrogram)
        return spectrogram

    def get_log_mel_spectrogram(self, spectrogram):
        num_spectrogram_bins = spectrogram.shape[-1]
        linear_to_mel_weight_matrix = tf.signal.linear_to_mel_weight_matrix(
            self.num_mel_bins, num_spectrogram_bins,
            self.sample_rate, self.lower_edge_hertz, self.upper_edge_hertz)
        mel_spectrogram = tf.tensordot(
            spectrogram, linear_to_mel_weight_matrix, axes=1)
        log_mel_spectrogram = tf.math.log(mel_spectrogram + 1e-12)
        return log_mel_spectrogram

    def get_mfcc_and_label_id(self, audio, label):
        spectrogram = self.get_spectrogram(audio)
        log_mel_spectrogram = self.get_log_mel_spectrogram(spectrogram)
        mfcc = get_mfcc(log_mel_spectrogram)
        mfcc = tf.expand_dims(mfcc, -1)
        label_id = tf.argmax(label == self.commands)
        return mfcc, label_id

    def audio_preprocess(self, files_ds):
        output_ds = files_ds.map(
            get_waveform_and_label, num_parallel_calls=self.AUTOTUNE)
        output_ds = output_ds.map(
            self.get_mfcc_and_label_id, num_parallel_calls=self.AUTOTUNE)
        return output_ds


class TrainPreprocessor(object):
    def __init__(self, batch=32):
        self.batch = batch
        self.AUTOTUNE = tf.data.experimental.AUTOTUNE

    def train_preprocess(self, train_ds, val_ds):
        train_ds = train_ds.batch(self.batch).cache().prefetch(self.AUTOTUNE)
        val_ds = val_ds.batch(self.batch).cache().prefetch(self.AUTOTUNE)
        return train_ds, val_ds
