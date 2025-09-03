from kokoro import KPipeline
from IPython.display import display, Audio
import soundfile as sf
import torch
import sys
import os
import vlc
from time import sleep

pipeline = KPipeline(lang_code='a', device='xpu')

# filename argument
file_path = sys.argv[1]
directory, file_name = os.path.split(file_path)

name = '.'.join(file_name.split('.')[:-1])

file = open(file_path, "r")
text = file.read()
generator = pipeline(text, voice='af_bella')

output_files = []

for i, (gs, ps, audio) in enumerate(generator):
    # print(i, gs, ps)
    display(Audio(data=audio, rate=24000, autoplay=i==0))
    output_file_name=f'{name}-{i}.wav'
    print(f"Done generating audio: {output_file_name}")
    sf.write(output_file_name, audio, 24000)
    output_files.append(output_file_name)

for output in output_files:
    full_path = os.path.abspath(output)
    print(f"Playing: {output}")
    media = vlc.MediaPlayer(f"file://{full_path}")
    media.play()
    sleep(0.1)
    duration=media.get_length() / 1000
    print(f"duration: {duration}s")
    sleep(duration)
