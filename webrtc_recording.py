# Purpose: Recording conversation with a Raspberry Pi continually for one month
#          Will need about 7G storage for one-month of wave files if recording two hours per day
#
# Feature: use WebRTC VAD (should be the best one for real-time streaming) for filtering out non-speech
#
# Adapted from https://github.com/wiseman/py-webrtcvad/blob/master/example.py
#

import collections
import contextlib
import os
import sys
import wave
import signal
import pyaudio
import datetime

import webrtcvad

debug = False

channels = 1
sample_rate = 16000
frame_duration_ms = 30  # supports 10, 20 and 30 (ms)
frame_data_size = int(sample_rate * frame_duration_ms / 1000)

vad = webrtcvad.Vad(3)  # 3: most aggressive of filtering out non-speech

pa = pyaudio.PyAudio()
stream = pa.open(format = pyaudio.paInt16,
                 channels = channels,
                 rate = sample_rate,
                 input = True,
                 output = False,
                 frames_per_buffer = 2048)

def vad_loop(num_padding_frames=30):
    ring_buffer = collections.deque(maxlen=num_padding_frames)
    voiced_frames = []
    triggered = False

    stream.start_stream()

    while True:
        frame_chunk = stream.read(frame_data_size)
        is_speech = vad.is_speech(frame_chunk, sample_rate)
        if debug:
            sys.stdout.write('1' if is_speech else '0')
        if not triggered:
            ring_buffer.append((frame_chunk, is_speech))
            num_voiced = len([f for f, speech in ring_buffer if speech])

            if num_voiced > 0.9 * ring_buffer.maxlen:
                triggered = True
                for f, is_speech in ring_buffer:
                    voiced_frames.append(f)
                ring_buffer.clear()
        else:
            voiced_frames.append(frame_chunk)
            ring_buffer.append((frame_chunk, is_speech))
            num_unvoiced = len([f for f, speech in ring_buffer if not speech])
            if num_unvoiced > 0.9 * ring_buffer.maxlen:
                triggered = False
                print('voiced_frames size:', len(voiced_frames))
                audio = b''.join([f for f in voiced_frames])
                save_to_wave_file(audio)
                ring_buffer.clear()
                voiced_frames = []

def save_to_wave_file(audio):
    now = datetime.datetime.now()
    date = now.strftime("%Y%m%d")
    tm = now.strftime("%H%M%S")
    path = "data/{}/{}.wav".format(date, tm)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with contextlib.closing(wave.open(path, 'wb')) as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio)

def main():
    # you need to adjust the value of num_padding_frames to meet your need
    vad_loop(num_padding_frames=50)

if __name__ == '__main__':
    main()
