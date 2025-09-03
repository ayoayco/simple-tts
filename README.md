# Simple TTTS

A simple text-to-speech program powered by [kokoro](https://huggingface.co/hexgrad/Kokoro-82M).

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

> [!Note]
> For using Intel XPUs, see section below

Activate the environment and install the dependencies

```bash
$ conda activate tts
$ python -m pip install -r requirements.txt
```

Because `vlc` to automatically play the generated audio, you will have to install it:

```bash
$ sudo apt update
$ sudo apt install vlc
```

> [!Note]
> Installing `vlc` via flatpak or snap will not work, as the code need access to `libvlc`.

## Intel XPU environmental variables

Because I use an intel-based laptop, I use [ipex-llm environment with pytorch 2.6](https://git.ayo.run/ayo/ipex-llm/src/branch/main/docs/mddocs/Quickstart/install_pytorch26_gpu.md).

For XPUs, we need to set some environmental variables. I have added a `env.sh` script which will activate the conda environment `tts` and set the environmental variables.

```bash
$ . env.sh
```

## Usage

To run the program it needs an input file using the flag `--input`.

```bash
$ python tts.py --input demo/tongue-twister.txt --voice asmr
```

### Voices

Optionally, you can indicate a [voice](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md) you want to use with `--voice`.

```bash
$ python tts.py --voice am_michael
```

There are four shortcuts available to the best voices: pro, hot, asmr, brit (i.e., best trained voices), and `pro` is the default if no value is given

```bash
$ python tts.py --voice pro # af_heart

$ python tts.py --voice hot # af_bella

$ python tts.py --voice asmr # af_nicole

$ python tts.py --voice brit # bf_emma
```
