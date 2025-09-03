# Simple TTS

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

> [!Important]
> For using Intel XPUs, you need to set up [ipex-llm environment with pytorch 2.6](https://git.ayo.run/ayo/ipex-llm/src/branch/main/docs/mddocs/Quickstart/install_pytorch26_gpu.md). Also, see [Intel XPU environmental variables"](#intel-xpu-environmental-variables) section below.

Activate the environment and install the dependencies

```bash
$ conda activate tts
$ python -m pip install -r requirements.txt
```

Because `vlc` is used to automatically play the generated audio, you will have to install it:

```bash
$ sudo apt update
$ sudo apt install vlc
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

To run the program it needs an input file using the flag `--input`.

```bash
$ python tts.py --input demo/tongue-twister.txt --voice asmr
```

### Voices

Optionally, you can indicate a voice you want to use with the `--voice` flag. See [all voices available](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md).

```bash
$ python tts.py --voice am_michael
```

There are four shortcuts available to the best voices: `pro`, `hot`, `asmr`, `brit` (i.e., best trained voices), and `pro` is the default if no value is given

```bash
$ python tts.py --voice pro # af_heart

$ python tts.py --voice hot # af_bella

$ python tts.py --voice asmr # af_nicole

$ python tts.py --voice brit # bf_emma
```
