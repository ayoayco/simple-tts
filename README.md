# Simple TTTS

A simple text to speech powered by [kokoro](https://huggingface.co/hexgrad/Kokoro-82M).

## Setup

Create new environment. Here I use `conda`

```bash
$ conda create -n tts
```

Because I use an intel-based laptop, I use [ipex-llm environment with pytorch 2.6](https://git.ayo.run/ayo/ipex-llm/src/branch/main/docs/mddocs/Quickstart/install_pytorch26_gpu.md)

```bash
### for Intel XPU specific device usage:
$ conda create -n tts --clone llm-pt26
```

Activate the environment and install the dependencies

```bash
$ conda activate tts
$ python -m pip install -r requirements.txt
```

Because `vlc` to automatically play the generated audio, you will have to install it:

```bash
sudo apt update
sudo apt install vlc
```

Note: installing `vlc` via flatpak or snap will not work, as the code need access to `libvlc`.
