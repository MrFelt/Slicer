# slicer

Slicer is a tool designed to automate the processing of audio files. Here's how it works:

1. **Initialization**: Provide the file directory, and slicer will initialize the process.
2. **Resampling**: It ensures that the audio files are resampled to 48 kHz, converting any 44.1 kHz files commonly outputted by UVR.
3. **Transcription and Rough Cut**: Runs `faster-whisper` via `whisper.py`, preconfigured to load the `large-v2` model (can be changed on line 38 of `whisper.py`). It transcribes the audio and makes a rough cut into sections.
4. **Segment Splitting**: Lastly, it executes `split.py` to ensure that all segments follow the 1-3.7s rule, skipping preprocessing in variants of the RVC WebUI.


### Disclaimer

I hold no experience in coding, and everything is provided pretty much as is, but,

 **it works on my system™**




### Installation:

1. Download as a zip, or clone. You will know the benefits of either or, if you don't, just download as a zip.
2. Make sure you have python 3.10.x installed. Should not matter which, just as long as it is 3.10.
3. Run start.bat, leaving it in folder. If you want to run it from a different spot, please just right click it and create a shortcut, and then copy that shortcut to the destination of where you want your shortcut to be. 
