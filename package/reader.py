# -*- coding: utf-8 -*-
"""
Lecture des annotations
Raphaël Ceré
Python 3.6.5
"""

import os
import csv
import json

__author__ = "Raphael Cere"
__copyright__ = "Copyright 2019, University of Lausanne, Switzerland"
__credits__ = ["Raphael Cere"]
__license__ = "GNU GPLv3"
__version__ = "0.1a0"
__maintainer__ = "Raphael Cere"
__email__ = "Raphael.Cere@unil.ch"
__status__ = "Development"


# tmp paramters
tmp_path =  "/Users/rcere/switchdrive/ddd_cvmm/DATA/ANNOTATION_ANT"
#tmp_path = str(input("PATH OF ANNOTATION:"))

def get_data(path):
	"""
	retrun path of data
	"""
	return os.path.dirname(os.path.abspath(path))+"/ANNOTATION_ANT/"

def ann_reader(file):
	"""
	return a list of annotation dictionnaries
	"""
	try:
		with open(file, 'r') as csv_file:
			r_reader = csv.reader(csv_file, delimiter=',')
			h = r_reader.__next__()
			d = list()
			for r in r_reader:
				o = dict()
				[o.update({h[x] : r[x]}) for x in range(0, len(r))]
				d.append(o)
		return d, h
	except IOError: raise IOError("Couldn't read file %s" % file)

def pb_inter(bp0, bp1, head):
	"""
	retrun True if the annotation intersecting R1
	"""
	pl1, pl2, al = [head[8], head[9]], [head[10], head[11]], head[3]
	if bp0[al] == "point" and bp1[al] == "box":
		x0, y0 = (float(bp0[pl1[0]]), float(bp0[pl1[1]]))
		x1, y1, x2, y2 = (float(bp1[pl1[0]]), float(bp1[pl1[0]]), float(bp1[pl2[0]]),float(bp1[pl2[0]]))
		return True if (x1 <= x0 <= x2) and (y1 <= y0 <= y2) else False
	elif bp0[al] == "box" and bp1[al] == "box":
		x01, y01, x02, y02 = (float(bp0[pl1[0]]), float(bp0[pl1[1]]), float(bp0[pl2[0]]),float(bp0[pl2[1]]))
		x11, y11, x22, y22 = (float(bp1[pl1[0]]), float(bp1[pl1[1]]), float(bp1[pl2[0]]),float(bp1[pl2[0]]))
		down = True if (x01 <= x11 <= x02) and (y01 <= y11 <= y02) else False
		up = True if (x01 <= x22 <= x02) and (y01 <= y22 <= y02) else False
		return True if down and up else False

def get_annotation(file, inter=False):
	"""
	retrun dictionnary by object from database
	file : path to the file
	inter : keep only annotation intersecting with one or more R.1
	"""
	if inter:
		a, h = ann_reader(file)
		is_r1 = [x for x in a if x[h[1]] == "R1"]
		if is_r1:
			b = list()
			for p0 in is_r1: is_c1_r1 = [x for x in a if pb_inter(p0, x, h) and x[h[1]] != "R1" and x[h[1]] == "C1"]
			for p1 in is_c1_r1: b.append([x[h[1]] for x in a if pb_inter(p1, x, h) and x[h[1]] != "R1" and x[h[1]] != "C1"])
		else: b = []
	else: b, h = ann_reader(file)
	return b,h 


BASE_PATH  = get_data(tmp_path)

for annotation in [x for x in os.listdir(BASE_PATH) if x[:10]=="annotation"]:
	drawing = get_annotation(BASE_PATH+annotation, True)
	#print("----"+annotation)
	print(drawing[0])
	






