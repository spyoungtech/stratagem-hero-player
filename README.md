# Stratagem Hero Player

A bot to play the Stratagem Hero minigame in Helldivers 2.

Please note: this is not intended for inputting stratagems in-mission, only in the minigame. In-mission stratagem inputs 
may differ from Stratagem Hero.

## Installation

Requires Python and Windows.

Install Requirements (ideally, in a virtualenv):

```bash
pip install -r requirements.txt
```

For NVIDIA users, if you have CUDA installed (available [here](https://developer.nvidia.com/cuda-downloads)), you can install the optional cuda requirements for faster processing:

```bash
install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

## Usage

1. Open Helldivers 2 and get ready to play Stratagem Hero
1. Start the script (`python play.py`) It will take a few moments to start up.
1. While the script is starting up, with the "Enter any Stratagem Input to Start!" screen up, drag the mouse down and to the right to get the camera in a reliable position
1. The script will automatically start the game when ready and play by itself
1. To stop the bot, simply alt-tab out of Helldivers and focus any other window


Note: the capture region is hard-coded for a 3440x1440 monitor. If your monitor has a different resolution, you will probably have to adjust the capture region in `play.py`
