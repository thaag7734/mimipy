# mimipy
Python parser for [MIMI](https://github.com/thaag7734/mimi)

## How to use
#### Windows users:
1. Download the version of PyAudio that corresponds with your system ([here](https://download.lfd.uci.edu/pythonlibs/q5gtlas7/PyAudio-0.2.11-cp37-cp37m-win32.whl) for 32-bit and [here](https://download.lfd.uci.edu/pythonlibs/q5gtlas7/PyAudio-0.2.11-cp37-cp37m-win_amd64.whl) for 64-bit)
2. Install the file you just downloaded by running `pip install [filename]` at the command prompt in your download directory.
3. Run `pip install -r requirements.txt` at the command prompt in your MIMIPy folder.
4. Run `playfile.py`.
#### Linux users:
1. Install `python-pyaudio` with your favourite package manager.
2. Install the file you just downloaded by running `python3 -m pip install [filename]` from the terminal in your download directory.
3. Run `python3 -m pip install -r requirements.txt` from the terminal in your MIMIPy folder.
4. Run `playfile.py`.
#### Mac users:
1. Install XCode from the app store, then run these 4 commands in sequence from the terminal:
```
xcode-select --install
brew remove portaudio
brew install portaudio
pip3 install pyaudio
```
2. Run `pip3 install -r requirements.txt` from the terminal in your MIMIPy folder.
3. Run `playfile.py`.
