# --coding: utf-8
import pyaudio
import wave
import speech


chunk = 1024  # Запись кусками по 1024 сэмпла
sample_format = pyaudio.paInt16  # 16 бит на выборку
channels = 2
rate = 44100  # Запись со скоростью 44100 выборок(samples) в секунду
seconds = 4
filename = "output_sound.wav"
p = pyaudio.PyAudio()  # Создать интерфейс для PortAudio

print('Recording...')

stream = p.open(format=sample_format,
                channels=channels,
                rate=rate,
                frames_per_buffer=chunk,
                input_device_index=0,  # индекс устройства с которого будет идти запись звука
                input=True)

frames = []  # Инициализировать массив для хранения кадров


for i in range(0, int(rate / chunk * seconds)):
    data = stream.read(chunk)
    frames.append(data)

# Остановить и закрыть поток
stream.stop_stream()
stream.close()
# Завершить интерфейс PortAudio
p.terminate()

print('Finished recording!')

wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(rate)
wf.writeframes(b''.join(frames))
wf.close()

#
