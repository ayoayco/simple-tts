import os
from time import sleep, time
import warnings
import importlib

import torch
import argparse
from kokoro import KPipeline
import soundfile as sf
# import vlc
from tqdm import tqdm
import pyperclip

# Disable all warnings
warnings.filterwarnings("ignore")

# See voices: https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md
voices = {
    'pro': 'af_heart',
    'hot': 'af_bella',
    'asmr':'af_nicole',
    'brit': 'bf_emma'
}

def parse_args():
    parser = argparse.ArgumentParser(description="Simple TTS", allow_abbrev=False)
    parser.add_argument(
        "input_text",
        type=str,
        nargs='?',
        default="",
        help="Text to read",
    )
    parser.add_argument(
        "--title",
        "-t",
        required=False,
        type=str,
        default="generated",
        help="Title to use as label to the generated outputs",
    )
    parser.add_argument(
        "--voice",
        "-v",
        required=False,
        type=str,
        default="pro",
        help="Voice to use (pro, hot, asmr, brit)",
    )
    parser.add_argument(
        "--input_file",
        "-i",
        required=False,
        type=str,
        default="demo/tongue-twister.txt",
        help="Path to the input text file",
    )
    parser.add_argument(
        "--clipboard",
        "-c",
        required=False,
        action="store_true",
        help="Use text from the clipboard (i.e., copied text)",
    )
    parser.add_argument(
        "--device",
        "-d",
        required=False,
        type=str,
        default=("cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else ("xpu" if torch.xpu.is_available() else "cpu"))),
        help="Device for inference: cuda | mps | cpu",
    )
    parser.add_argument(
        "--skip_play",
        "-s",
        required=False,
        action="store_true",
        help="Prevent playing the generated audio",
    )
    return parser.parse_args()

def generate_audio(generator, name, voice, device):
    start_time = time()
    output_files = []
    print(f"Using {device} device...")
    for i, (gs, ps, audio) in enumerate(generator):
        output_file_name=f'outputs/{name}/{name}-{voice}-{i}.wav'
        os.makedirs(os.path.dirname(output_file_name), exist_ok=True)
        output_files.append(output_file_name)
        sf.write(output_file_name, audio, 24000)
    generation_time = time() - start_time
    print(f"{len(output_files)} chunks generated in {generation_time:.2f} seconds")
    return output_files

def play_audio(output_files):
    vlc_module = importlib.import_module("vlc")
    print("Now playing generated audio...")
    length = len(output_files)
    for i, output in enumerate(output_files):
        full_path = os.path.abspath(output)
        media = vlc_module.MediaPlayer(f"file://{full_path}")
        media.play()
        sleep(0.1)
        duration=media.get_length() / 1000
        chunk=f"{i+1}/{length} " if length > 1 else ""
        description = f"\u25B6 {chunk}"
        for i in tqdm(range(100),
            desc=description,
            bar_format='{l_bar} {elapsed} {bar} {remaining}',
            colour='yellow'):
            sleep(duration / 100)

def main():
    args=parse_args()
    pipeline = KPipeline(lang_code='a', device=args.device, repo_id='hexgrad/Kokoro-82M')
    if args.voice in voices:
        voice=voices[args.voice]
    else:
        voice=voices['pro'] if args.voice is None else args.voice

    # filename argument
    if args.input_text == "":
        if args.clipboard:
            # use copied text
            print('Using copied text as input...')
            text = pyperclip.paste()
            name = 'copied'
        else:
            file_path = args.input_file
            directory, file_name = os.path.split(file_path)
            name = '.'.join(file_name.split('.')[:-1])
            file = open(file_path, "r")
            text = file.read()
    else:
        name = "chat"
        text = args.input_text

    if args.title:
        name = args.title

    # make safe for filenames
    name = name.replace(" ", "_")
    name = name.replace("\\", "_")
    name = name.replace("/", "_")

    generator = pipeline(text, voice=voice, split_pattern=r'[:.?!;]\n+')
    output_files = generate_audio(generator, name, voice, args.device)
    directory, output_file_name = os.path.split(output_files[0])
    if args.skip_play:
        print(f"Audio player disabled: {directory}/*")
    else:
        try:
            play_audio(output_files)
        except:
            print(f"Something went wrong when trying to play the audio. Play the output files manually: {directory}/*")

if __name__ == "__main__":
    main()
