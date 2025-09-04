# Simple TTS

A simple machine learning text-to-speech program powered by [kokoro](https://huggingface.co/hexgrad/Kokoro-82M).

> [!Warning]
> This is currently only tested working on Ubuntu-based distros due to the [required packages](#required-packages).

## Setup

Clone repo and go into the directory

```bash
$ git clone https://git.ayo.run/ayo/simple-tts
$ cd simple-tts
```

Create new environment. Here I use `conda`.

```bash
$ conda create -n tts

### for Intel XPU specific device usage:
$ conda create -n tts --clone llm-pt26
```

> [!Important]
> For using Intel XPUs, you need to set up [ipex-llm environment with pytorch 2.6](https://git.ayo.run/ayo/ipex-llm/src/branch/main/docs/mddocs/Quickstart/install_pytorch26_gpu.md). Also, see [Intel XPU environmental variables"](#intel-xpu-environmental-variables) section below.

Activate the environment and install the dependencies

```bash
$ conda activate tts
$ python -m pip install -r requirements.txt
```

### Required packages

The following are required packages aside from the python dependencies. `espeak-ng` is used by `kokoro` under the hood for english languages, and `libvlc` is used as the default audio player for the generated audio.

```bash
$ sudo apt update
$ sudo apt install vlc espeak-ng
```

> [!Note]
> Installing `vlc` via flatpak or snap will not work, as the code need access to `libvlc`.

### Intel XPU environmental variables

For XPUs, we need to set some environmental variables. I have added a `env.sh` script which will activate the conda environment `tts` and set the environmental variables.

```bash
$ . env.sh
```

## Usage

Go into the directory and activate the environment:

```bash
$ cd simple-tts
$ conda activate tts
```

If using Intel XPUs, set the env variables

```bash
$ . env.sh
```

Running the program without arguments will use the demo text `tongue-twister.txt` with the default voice.

```bash
$ python tts.py # will use default arguments
```

You can pass a string as first argument:

```bash
$ python tts.py "Hello world!" # will be read by the default voice
```

To run the program with an input file, use flag `--input_file`.

```bash
$ python tts.py --input_file demo/tongue-twister.txt
```

### Voices

Optionally, you can indicate a voice you want to use with the `--voice` flag. See [all voices available](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md).

```bash
$ python tts.py --voice am_michael
```

There are four shortcuts available to the best voices: `pro`, `hot`, `asmr`, `brit` (i.e., best trained voices), and `pro` is the default if no value is given

```bash
$ python tts.py "Hello there!" --voice pro # af_heart

$ python tts.py "Hello there!" --voice hot # af_bella

$ python tts.py "Hello there!" --voice asmr # af_nicole

$ python tts.py "Hello there!" --voice brit # bf_emma
```

### Disable audio player

You can disable the built-in audio player with `--skip_play` if you choose to play the audio files generated with your preferred player.

```bash
$ python tts.py "Hello there!" --voice asmr --skip_play

```

## Demo Outputs

### Voice: pro (ah_heart)

https://git.ayo.run/ayo/simple-tts/src/branch/main/demo/tongue-twister-af_heart-0.wav

https://git.ayo.run/ayo/simple-tts/src/branch/main/demo/tongue-twister-af_heart-1.wav

https://git.ayo.run/ayo/simple-tts/src/branch/main/demo/tongue-twister-af_heart-2.wav

### Voice: asmr (ah_nicole)

https://git.ayo.run/ayo/simple-tts/src/branch/main/demo/tongue-twister-af_nicole-0.wav

https://git.ayo.run/ayo/simple-tts/src/branch/main/demo/tongue-twister-af_nicole-1.wav

https://git.ayo.run/ayo/simple-tts/src/branch/main/demo/tongue-twister-af_nicole-2.wav
