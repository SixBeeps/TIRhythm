import taikoreader
import tkinter as tk
from tkinter import filedialog
import pyperclip
import sys

def stringify(hitObject):
	"""Turns a TaikoObject into a string that TITaiko understands"""

	ret = str(int(hitObject.offset)) + ':' + str(hitObject.objType.value)

	# Add a third parameter if the object is a long note
	if (hitObject.length != None):
		ret += ':' + str(int(hitObject.length))

	return ret

# The Python file can be given a command-line argument leading to the desired beatmap path.
# If nothing is passed in, the program will display an Open File dialog so the user can choose one

if (len(sys.argv) >= 2):
	filePath = sys.argv[1]
else:
	root = tk.Tk()
	root.title('TITaiko Open File')
	root.geometry('1x1')
	filePath = filedialog.askopenfilename()
	
if (filePath == ''):
	sys.exit()
with open(filePath, 'r') as f:
	beatmap = taikoreader.TaikoBeatmap.readFile(filePath)

# Here we compile a list of all hitobjects sorted by the time they appear in the beatmap

allObjects = beatmap.objects
allObjects.sort(key=lambda x: x.offset)

# Now we generate the resulting map data that will be put into the program

result = '|'.join(stringify(obj) for obj in allObjects)

print(result)
pyperclip.copy(result)