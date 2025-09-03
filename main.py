import sys
import os
from time import sleep

from kokoro import KPipeline
import soundfile as sf
import vlc
from tqdm import tqdm


# See voices: https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md
voices = {
    'pro': 'af_heart',
    'hot': 'af_bella',
    'asmr':'af_nicole',
    'brit': 'bf_emma'
}
pipeline = KPipeline(lang_code='a', device='xpu', repo_id='hexgrad/Kokoro-82M')

# filename argument
file_path = sys.argv[1]
directory, file_name = os.path.split(file_path)

name = '.'.join(file_name.split('.')[:-1])

file = open(file_path, "r")
text = file.read()
generator = pipeline(text, voice=voices['pro'])

output_files = []
length = 0

for i, (gs, ps, audio) in enumerate(generator):
    output_file_name=f'outputs/{name}-{i}.wav'
    os.makedirs(os.path.dirname(output_file_name), exist_ok=True)
    output_files.append(output_file_name)
    sf.write(output_file_name, audio, 24000)
    print(u'\u2713', output_file_name)
    length = length + 1

for i, output in enumerate(output_files):
    full_path = os.path.abspath(output)
    media = vlc.MediaPlayer(f"file://{full_path}")
    media.play()
    sleep(0.1)
    duration=media.get_length() / 1000
    description = f"\u25B6 {i+1}/{length} ({'{0:0>5.2f}'.format(duration)}s)"
    for i in tqdm(range(100), desc=description):
        sleep(duration / 100)
