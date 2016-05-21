import json
import implicit
from dtree import *
from prule import *
from constants import *

class Parser:
	def __init__(self):
		pass

	def train(self):
		obj = Implicit(100,100,500)
		obj.generateTrainData()