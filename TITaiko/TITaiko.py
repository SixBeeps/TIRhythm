from ti_system import *
from ti_draw import *
from time import *

# Editable fields
data=''
speedMultiplier=0.4
correctionalFactor=1.0 # PC=1.0, Real Hardware=1.024
playfieldWidth=50
holdWidth=5 # Higher values mean thinner holds

# Auto-calculated fields
dataKvp=data.split('|')

startTime=ticks_ms()
notesPassed=0
while True:
  set_color(0,6,12)
  fill_rect(0,0,318,212)
  set_color(128,0,0)
  draw_circle(5+playfieldWidth/3,106,playfieldWidth/3)
  use_buffer()
  crudeTime=ticks_ms()-startTime
  currentTime=crudeTime*correctionalFactor
  removeQueue=[]
  if(get_key()=='esc' or len(dataKvp)==0):
    raise Exception()
  for obj in dataKvp:
    objData=obj.split(':')
    objType=int(objData[1])
    if (objType==0 or objType==2): # Don
      noteColor=[250,70,30]
      size=objType*2
    elif (objType==1 or objType==3): # Kat
      noteColor=[74,189,255]
      size=(objType-1)*2
    elif (objType==4): # Roll
      noteColor=[255,201,74]
      size=0
    else: # Probably a denden
      noteColor=[255,255,255]
      size=4
    set_color(noteColor[0],noteColor[1],noteColor[2])
    xPos=int(objData[0])-currentTime
    xPos*=speedMultiplier
    if(xPos<5+playfieldWidth/3):
      notesPassed+=1
      removeQueue.append(obj)
      continue
    if(xPos>328):
      break
    fill_circle(xPos,106,playfieldWidth/3+size)
    
  set_color(25,128,255)
  draw_rect(-1,106-playfieldWidth/2,320,playfieldWidth)
  paint_buffer()
  for obj in removeQueue:
    dataKvp.remove(obj)