# This file will not run on PC. It should be put into the TI Nspire
# Alternatively, you can load the .tns file onto the Nspire so you don't have to paste the code in yourself

from ti_system import *
from ti_draw import *
from time import *
import math

# Editable fields
data = ''
speedMultiplier = 0.5
correctionalFactor = 1.0  # PC=1.0, Real Hardware=1.024
playfieldWidth = 150
holdWidth = 5  # Higher values mean thinner holds

# Auto-calculated fields
dataKvp = data.split('|')
columnCount = 1
for obj in dataKvp:
    k = int(obj.split(':')[1])
    if k + 1 > columnCount:
        columnCount = k + 1

startTime = ticks_ms()
notesPassed = 0
while True:
    set_color(0, 6, 12)
    fill_rect(0, 0, 318, 212)
    set_color(25, 128, 255)
    use_buffer()
    crudeTime = ticks_ms() - startTime
    currentTime = crudeTime * correctionalFactor
    removeQueue = []
    if (get_key() == 'esc' or len(dataKvp) == 0):
        raise Exception()
    for obj in dataKvp:
        objData = obj.split(':')
        if (len(objData) == 3):
            height = int(objData[2])
        else:
            height = 0
        yPos = 318 + (currentTime - int(objData[0]))
        yPos *= speedMultiplier
        if (yPos - (height * speedMultiplier) > 212):
            notesPassed += 1
            removeQueue.append(obj)
            continue
        if (yPos < 0):
            break
        xPos = int(objData[1]) * (playfieldWidth / columnCount) + (
            318 - playfieldWidth) / 2
        fill_rect(xPos, yPos, (playfieldWidth / columnCount), 10)
        if (len(objData) == 3):
            nyPos = yPos - height * speedMultiplier
            fill_rect(xPos + holdWidth, nyPos,
                      (playfieldWidth / columnCount) - holdWidth * 2,
                      height * speedMultiplier)
    draw_rect((318 - playfieldWidth) / 2, -1, playfieldWidth, 300)
    paint_buffer()
    for obj in removeQueue:
        dataKvp.remove(obj)
