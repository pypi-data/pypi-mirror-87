# aermanager
*Python package for managing AER data, including .aedat4 files, live DV streams, and interfacing with pyTorch.*

This software is designed for the following purposes:
- Read aedat files (v2-4) containing DVS spike trains, accumulate them, and save them in a format that can be read by a pyTorch dataset in a faster way.
- Read the files into a pyTorch dataset
- Receive frames from the DV software, queue and batch them in order to feed them to a spiking neural network simulation (`LiveDv`).


## Installation

The easiest way to install this repository is to clone it and install it with pip:

```bash
pip install aermanager
```

## Documentation

synsense.gitlab.io/aermanager

