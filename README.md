# TIRhythm
A variety of rhythm game map players for the TI Nspire

## Installation
Included inside each of the folders is the Python source code for both the beatmap converters and the runners. Download and extract the repository as a .zip file, and navigate to the desired project's folder.

To convert a beatmap, run the converter.py script. This will open a file chooser for you to select a beatmap to convert. Once the beatmap has been converted, the contents will output to the console as well as your clipboard. From there, edit the contents of TI\[x\].py (where \[x\] is the game mode, e.x. TIMania.py) and paste the resulting beatmap data into the `data` variable.

**Protip for advanced haxors**: you can also run converter.py in the console and pass in a file path to a beatmap. This will let you bypass the file dialog entirely. Theoretically, this could be used to pipe data into another program for conversion there.

## Runtime issue
The TI Nspire has a strange bug that causes the timer to run slower than realtime speed. This is fixed by multiplying the program timer's value by 1.024, as noted by the comment in the runner programs. If running on a PC, you should set the variable back to 1 so that the program doesn't run faster than expected.

## Examples
TIMania 4k: [サイバーサンダーサイダー (Cyber Thunder Cider)](https://www.youtube.com/watch?v=18ajAmFy78g)
TIMania 7k: [Fool Moon Night](https://www.youtube.com/watch?v=K4GSyjPjq4k)
