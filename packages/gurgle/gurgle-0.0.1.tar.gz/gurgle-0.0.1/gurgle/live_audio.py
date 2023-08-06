from IPython.display import clear_output
from io import BytesIO
import time
from typing import *

import numpy as np
import soundfile as sf

from stream2py import SourceReader, StreamBuffer, BufferReader
from stream2py.sources.audio import PyAudioSourceReader


class VisualizationStream(SourceReader):
    def __init__(self, mk_int16_array_gen: Callable, chk_to_viz: Callable):
        self.mk_int16_array_gen = mk_int16_array_gen
        self.chk_to_viz = chk_to_viz
        self._viz_gen = None

    def _mk_viz_gen(self):
        for i, a in enumerate(self.mk_int16_array_gen()):
            yield i, self.chk_to_viz(a)

    def open(self):
        """Setup data generator"""
        self._viz_gen = self._mk_viz_gen()

    def read(self):
        return next(self._viz_gen)

    def close(self):
        """Clean up if needed"""
        del self._viz_gen
        self._viz_gen = None

    @property
    def info(self):
        """Whatever info is useful to you
        StreamBuffer will record info right after open"""
        return dict(mk_int16_array_gen=str(self.mk_int16_array_gen), chk_to_viz=str(self.chk_to_viz))

    def key(self, data):
        """Convert data to a sortable value that increases with each read.
        the enumerate index in this case
        """
        return data[0]


def bytes_to_waveform(b: bytes, sr: int, n_channels: int, sample_width: int, dtype='int16') -> np.array:
    """Convert raw bytes to a numpy array cast to dtype

    :param b: bytes
    :param sr: sample rate
    :param n_channels: number of channels
    :param sample_width: sample byte width [2, 3, 4]
    :param dtype: data type used by numpy, i.e. dtype=np.int16 is the same as dtype='int16'
    :return: numpy.array
    """
    sample_width_to_subtype = {
        2: 'PCM_16',
        3: 'PCM_24',
        4: 'PCM_32',
    }
    return sf.read(BytesIO(b), samplerate=sr, channels=n_channels, format='RAW',
                   subtype=sample_width_to_subtype[sample_width], dtype=dtype)[0]


from functools import partial


def list_recording_device_index_names():
    """List (index, name) of available recording devices"""
    return sorted((d['index'], d['name']) for d in PyAudioSourceReader.list_device_info() if d['maxInputChannels'] > 0)


def find_a_default_input_device_index():
    for index, name in list_recording_device_index_names():
        if 'microphone' in name.lower():
            print(f"Found {name}. Will use it as the default input device. It's index is {index}")
            return index
    for index, name in list_recording_device_index_names():
        if 'mic' in name.lower():
            print(f"Found {name}. Will use it as the default input device. It's index is {index}")
            return index


DFLT_INPUT_DEVICE_INDEX = find_a_default_input_device_index()


def device_info_by_index(index):
    try:
        return next(d for d in PyAudioSourceReader.list_device_info() if d['index'] == index)
    except StopIteration:
        raise ValueError(f"Not found for input device index: {index}")


def mk_pyaudio_to_int16_array_gen_callable(audio_reader: BufferReader):
    _info = audio_reader.source_reader_info
    specific_bytes_to_wf = partial(bytes_to_waveform,
                                   sr=_info['rate'],
                                   n_channels=_info['channels'],
                                   sample_width=_info['width'])

    def mk_pyaudio_to_int16_array_gen():
        for timestamp, wf_bytes, frame_count, time_info, status_flags in audio_reader:
            yield specific_bytes_to_wf(wf_bytes)

    return mk_pyaudio_to_int16_array_gen


def launch_audio_tracking(chk_callback: Callable, input_device_index: int):
    _info = device_info_by_index(input_device_index)
    frames_per_buffer = int(_info['defaultSampleRate'] / 10)

    try:
        with StreamBuffer(
                source_reader=PyAudioSourceReader(input_device_index=input_device_index,
                                                  rate=int(_info['defaultSampleRate']),
                                                  width=2,
                                                  channels=_info['maxInputChannels'],
                                                  frames_per_buffer=frames_per_buffer,
                                                  ),
                maxlen=PyAudioSourceReader.audio_buffer_size_seconds_to_maxlen(buffer_size_seconds=60,
                                                                               rate=_info['defaultSampleRate'],
                                                                               frames_per_buffer=frames_per_buffer,
                                                                               ),
                auto_drop=False,
                sleep_time_on_read_none_s=0.1
        ) as audio_buffer:
            audio_reader = audio_buffer.mk_reader()

            with StreamBuffer(
                    source_reader=VisualizationStream(
                        mk_int16_array_gen=mk_pyaudio_to_int16_array_gen_callable(audio_reader),
                        chk_to_viz=chk_callback
                    ),
                    maxlen=10
            ) as viz_buffer:
                viz_reader = viz_buffer.mk_reader()

                yield from viz_reader
    except KeyboardInterrupt:
        print("KeyboardInterrupt: So I'm stopping the process")
