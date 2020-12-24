# There were no Taiko parsers that I could find, so I decided to make my own.
# The closest thing I could find was jakads' Randosu, which randomizes Taiko beatmaps.
# This file was, in part, inspired from said project

# Also note: a lot of other information one might need from a Taiko parser has been left out, such as timing point sample sets.
# If you need this functionality, feel free to fork and implement it yourself.

from enum import Enum

def isBitSet(num, k):
	"""Returns True if bit k of num is 1, else False. This is used internally to interpret hitsounds as a TaikoObjectType"""
	return num & (1 << (k - 1)) > 0

class TaikoBeatmap:
	"""A class to hold a taiko beatmap's objects and information"""

	@staticmethod
	def readFile(path):
		"""Reads a file given the file's path and turns it into a TaikoBeatmap"""
		
		self = TaikoBeatmap()
		self.objects = []
		self.timingPoints = []

		with open(path, 'r', encoding='utf8') as f:
			fContents = f.read()

			try:
				fContents = fContents.replace('[TimingPoints]', '[HitObjects]') # This little hack I got from Reamber
				fContents = fContents.replace('[Difficulty]', '[HitObjects]')
				difficultyLines = fContents.split('[HitObjects]')[1].split('\n')
				timingLines = fContents.split('[HitObjects]')[2].split('\n')
				objectLines = fContents.split('[HitObjects]')[3].split('\n')
			except IndexError:
				print ('Failed to convert ' + path + ' into a TaikoBeatmap. Is this a valid .osu map?')
				self = None
				return

			# Extract SliderMultiplier from Difficulty StopAsyncIteration

			self.sliderMultiplier = 1.0
			for line in difficultyLines:
				if ('SliderMultiplier' in line):
					self.sliderMultiplier = float(line.split(':')[1])
					break

			# Process Timing Points

			for line in timingLines:
				lSplit = line.split(',')

				if (len(lSplit) == 8):
					newPoint = TimingPoint(int(lSplit[0]), float(lSplit[1]), int(lSplit[2]), int(lSplit[6]), float(lSplit[7]))
					self.timingPoints.append(newPoint)
				else:
					print ('There seems to be an invalid timing point, will ignore: ' + line)
			self.timingPoints.sort(key=lambda x: x.time)

			# Process Hitobjects
			
			for line in objectLines:
				lSplit = line.split(',')

				if (len(lSplit) == 6): # Process Don/Kat
					offset = int(lSplit[2])
					length = None
					hitsounds = int(lSplit[4])
					if (isBitSet(hitsounds, 2) or isBitSet(hitsounds, 4)):
						objType = TaikoObjectType.KAT
					else:
						objType = TaikoObjectType.DON
					if (isBitSet(hitsounds, 3)):
						objType = TaikoObjectType.DONL if objType == TaikoObjectType.DON else TaikoObjectType.KATL # If the Finish flag is set, the object is a large Don/Kat
				
				elif (len(lSplit) == 11 or len(lSplit) == 8): # Process Drumroll
					offset = int(lSplit[2])
					objType = TaikoObjectType.ROLL
					length = float(lSplit[7]) / (self.sliderMultiplier * 100) * self.timingPointAt(offset).beatLength
				
				elif (len(lSplit) == 7): # Process Spinner/Denden
					offset = int(lSplit[2])
					objType = TaikoObjectType.DENDEN
					length = int(lSplit[5]) - offset
				
				else:
					print ('There seems to be an invalid hitobject, will ignore: ' + line)
					continue
				
				newObj = TaikoObject(offset, objType, length)
				self.objects.append(newObj)

		return self

	def timingPointAt(self, t):
		"""Returns the beatmap's TimingPoint at a given time, or None if there isn't any"""

		for point in self.timingPoints:
			if (point.time >= t):
				return point
		return None


class TaikoObject:
	"""Holds info about a taiko hitobject"""

	def __init__(self, offset, objType, length = None):
		self.offset = offset
		self.objType = objType
		self.length = length


class TaikoObjectType(Enum):
	"""A static data type to represent the type of hitobject a TaikoHitobject is"""

	DON = 0 # Normal orange note
	KAT = 1 # Normal blue note
	DONL = 2 # Large orange note
	KATL = 3 # Large blue note
	ROLL = 4 # Drumroll
	DENDEN = 5 # Alternating spinner

class TimingPoint:
	"""Holds information about a timing point, either inherited or uninherited"""

	def __init__(self, t, beatLength, meter, uninherited, effects):
		self.time = t
		self.beatLength = beatLength
		self.meter = meter
		self.uninherited = uninherited
		self.effects = effects