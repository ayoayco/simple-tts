import os
from time import sleep, time
import warnings
import importlib
import random

import torch
import argparse
from kokoro import KPipeline
import soundfile as sf
from tqdm import tqdm
import pyperclip
from yaspin import yaspin

# See voices: https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md
voices = {
    'pro': 'af_heart',
    'hot': 'af_bella',
    'asmr':'af_nicole',
    'brit': 'bf_emma'
}

prep_texts = [
    "Check mic, 1-2-3...",
    "*Tap* *tap* ... Is this thing on?",
    "Ready, set... *Ahem!*",
    "Mic's on, lights are set, I'm ready to roll.",
    "All set? Let's make it a good one.",
    "Ready, set, go—now that's the real countdown.",
    "Checking the mic, one, two, three.",
    "Lights, mic, action—now let's do this.",
    "Hold tight—this is about to get interesting.",
    "If the mic works, we're good to go.",
    "All systems green—let's make this a good one."
]

def parse_args():
    parser = argparse.ArgumentParser(description="Simple TTS - machine learning text-to-speech for your terminal", allow_abbrev=False)
    parser.add_argument(
        "input_text",
        type=str,
        nargs='?',
        default="",
        help="text to read",
    )
    parser.add_argument(
        "--input_file",
        "-i",
        required=False,
        type=str,
        default="demo/tongue-twister.txt",
        help="path to the input text file",
    )
    parser.add_argument(
        "--clipboard",
        "-c",
        required=False,
        action="store_true",
        help="use text from the clipboard (i.e., copied text)",
    )
    parser.add_argument(
        "--title",
        "-t",
        required=False,
        type=str,
        help="title to use as label to the generated outputs",
    )
    parser.add_argument(
        "--voice",
        "-v",
        required=False,
        type=str,
        default="pro",
        help="voice to use (pro, hot, asmr, brit)",
    )
    parser.add_argument(
        "--skip_play",
        "-s",
        required=False,
        action="store_true",
        help="Prevent playing the generated audio",
    )
    parser.add_argument(
        "--force_lang",
        required=False,
        type=str,
        help="force language code",
    )
    parser.add_argument(
        "--verbose",
        default=False,
        action="store_true",
        help="show verbose reports",
    )
    parser.add_argument(
        "--device",
        "-d",
        required=False,
        type=str,
        default=("cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else ("xpu" if torch.xpu.is_available() else "cpu"))),
        help="Device for inference: cuda | mps | cpu",
    )
    return parser.parse_args()

def generate_audio(generator, name, voice):
    output_files = []

    for i, (gs, ps, audio) in enumerate(generator):
        output_file_name=f'outputs/{name}/{name}-{voice}-{i}.wav'
        os.makedirs(os.path.dirname(output_file_name), exist_ok=True)
        output_files.append(output_file_name)
        sf.write(output_file_name, audio, 24000)
    return output_files

def play_audio(output_files):
    vlc_module = importlib.import_module("vlc")
    length = len(output_files)
    for i, output in enumerate(output_files):
        full_path = os.path.abspath(output)
        media = vlc_module.MediaPlayer(f"file://{full_path}")
        media.play()
        sleep(0.5)
        duration=media.get_length() / 1000
        chunk=f"{i+1}/{length} " if length > 1 else ""
        description = f"\u25B6 {chunk}"
        for i in tqdm(range(100),
            desc=description,
            bar_format='{l_bar} {elapsed} {bar} {remaining}',
            colour='yellow'):
            sleep(duration / 100)

def main():

    # Get a randome "preparing" text
    spinner_text = random.choice(prep_texts)

    # Generate audio
    with yaspin() as spinner:
        spinner.text = spinner_text

        args=parse_args()

        if not args.verbose:
            # Disable all warnings
            warnings.filterwarnings("ignore")

        if args.voice in voices:
            voice=voices[args.voice]
        else:
            voice=voices['pro'] if not args.voice else args.voice

        # filename argument
        if args.input_text == "":
            if args.clipboard:
                # use copied text
                text = pyperclip.paste()
                name = 'copied'
            else:
                dirname = os.path.dirname(__file__)
                file_path = os.path.join(dirname, args.input_file)
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

        lang_code = args.force_lang if args.force_lang else voice[0]

        pipeline = KPipeline(lang_code=lang_code, device=args.device, repo_id='hexgrad/Kokoro-82M')

        '''
            Split patterns:
            - only multiple consecutive new line (to handle wrapped statements)
            - statements ending in punctuations (:.?!;)
            - list items starting in '-' or '*'
            - numbered items starting with a digit followed by a dot '.'
            - if a new line starts with a capital letter
        '''
        sp = r'\n{2,}|[:.?!;]\n+|\n[(\* )(\- )(\d\. )]|\n[A-Z]'

        generator = pipeline(
            text,
            voice=voice,
            split_pattern=sp
        )

        if args.verbose:
            print(f"[TTS] Using device: \"{args.device}\", voice: \"{voice}\", output label: \"{name}\"")
            if args.clipboard:
                print('[TTS] Using copied text as input.')

        start_time = time()
        output_files = generate_audio(generator, name, voice)
        generation_time = time() - start_time
        directory,f = os.path.split(output_files[0])

        if args.verbose:
            print(f"[TTS] {len(output_files)} chunks generated in {generation_time:.2f} seconds")
            print(f"[TTS] Output files are in: {directory}/*")

    # Play audio
    if args.skip_play:
        print(f"[TTS] Audio player disabled: {directory}/*")
    else:
        try:
            play_audio(output_files)
        except:
            print(f"[TTS] Something went wrong when trying to play the audio. Play the output files manually: {directory}/*")

if __name__ == "__main__":
    main()
