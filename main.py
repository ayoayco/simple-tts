from kokoro import KPipeline
import soundfile as sf
import sys
import os
import vlc
from time import sleep
from tqdm import tqdm

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
    output_file_name=f'outputs/{name}-{i}.wav'
    os.makedirs(os.path.dirname(output_file_name), exist_ok=True)
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
    #for i in tqdm(range(100)):
    sleep(duration)
