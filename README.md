# Stratagem Hero Player

A bot to play the Stratagem Hero minigame in Helldivers 2.

Please note: this is not intended for inputting stratagems in-mission, only in the minigame. This project makes no 
efforts to hide itself, evade detection, or circumvent any anti-cheat measures. 
If you use this software in Helldivers 2, there is no guarantee of any kind that you will not be banned. **Use at your own 
risk**.


<video src="https://github.com/spyoungtech/stratagem-hero-player/assets/15212758/ee1f9861-5e57-447f-b2d9-00646898846d"></video>

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
