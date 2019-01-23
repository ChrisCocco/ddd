# -*- coding: utf-8 -*-
"""
Lecture des annotations
Raphaël Ceré
Python 3.6.5
"""

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

# def get_annotation_gods(annotation)



if __name__ == '__main__':
	import os
	import csv
	import json
	import numpy as np
	import itertools
	import networkx as nx
	import matplotlib.pyplot as plt

	BASE_PATH  = get_data(tmp_path)
	annotation_drawings = list() 
	annotation_drawings_id = list()
	for annotation in [x for x in os.listdir(BASE_PATH) if x[:10]=="annotation"]:
		drawing = get_annotation(BASE_PATH+annotation, True)
		annotation_drawings.append((annotation, drawing[0]))

	### Counts by god representations
	ann_by_god = [x[0] for x in [y[1] for y in annotation_drawings if y[1]] if x[0]]
	id_by_god  = [y[0] for y in annotation_drawings if y[1] and [y[0]]*len(y[1][0])]

	g = len(ann_by_god)
	n = len(annotation_drawings)

	print(">>> %s gods identified for %s drawings <<< p = %f" %(g,n, float(g/n)))

	# unique items present (to edit to a single prototypes list)
	items_by_gods = list()
	for i in ann_by_god: [items_by_gods.append(x) for x in i] 
	items_unique = list(set(items_by_gods)) # headers
	h = len(items_unique)

	print(">>> %s unique caracteristics." %(h))

	# Contengency table gods x items
	count_items_by_god = np.zeros((g,0))
	for i in items_unique:
		a = [j.count(i) for j in ann_by_god]
		count_items_by_god = np.hstack((count_items_by_god,np.array(a)[:,np.newaxis]))

	rows = np.array(id_by_god , dtype='|S'+str(np.max([len(x) for x in id_by_god])))[:, np.newaxis]
	data = np.char.mod("%10.0f", count_items_by_god)
	with open('count_items_by_god.csv', 'w') as f:
		np.savetxt(f, np.hstack((rows, data)), delimiter=', ', fmt='%s', header=str(rows))

	# Binary table gods x items
	binary_items_by_god = np.zeros((g,h))
	binary_items_by_god[np.where(count_items_by_god >=1.)] = 1.

	rows = np.array(id_by_god , dtype='|S'+str(np.max([len(x) for x in id_by_god])))[:, np.newaxis]
	data = np.char.mod("%10.0f", binary_items_by_god)
	with open('binary_items_by_god.csv', 'w') as f:
		np.savetxt(f, np.hstack((rows, data)), delimiter=', ', fmt='%s', header=str(rows))

	# Contengency table items x items
	count_by_items = np.zeros((h,h))
	for i in range(h):
		for j in range(h):
			a = [np.sum([x.count(items_unique[i]), x.count(items_unique[j])]) for x in ann_by_god if x.count(items_unique[i]) != 0 and x.count(items_unique[j]) !=0]
			count_by_items[i,j] = np.sum(a)

	rows = np.array(items_unique, dtype='|S'+str(np.max([len(x) for x in items_unique])))[:, np.newaxis]
	data = np.char.mod("%10.0f", count_by_items)
	with open('count_by_items.csv', 'w') as f:
		np.savetxt(f,  np.hstack((rows, data)), delimiter=', ', fmt='%s')

	# Binary table items x items
	binary_by_items = np.zeros((h,h))
	binary_by_items[np.where(count_by_items >=1.)] = 1.

	rows = np.array(items_unique, dtype='|S'+str(np.max([len(x) for x in items_unique])))[:, np.newaxis]
	data = np.char.mod("%10.0f", binary_by_items)
	with open('binary_by_items.csv', 'w') as f:
		np.savetxt(f, np.hstack((rows, data)), delimiter=', ', fmt='%s')

	# All combinaison possible of items
	k = 2
	comb_possible = np.math.factorial(h)/(np.math.factorial(h-k)*np.math.factorial(k))
	dict_comb_items = dict()
	dict_comb_items_binary = dict()
	for item in itertools.combinations(items_unique, k):
		a = [[x.count(y) for y in item] for x in ann_by_god]
		b = [x for x in a if np.count_nonzero(x) == k]
		dict_comb_items[item] = len(b)

	# print(dict_comb_items.items())
	# rows = np.array(list(dict_comb_items.keys()), dtype='|S'+str(np.max([len(x) for x in dict_comb_items.keys()])))[:, np.newaxis]
	# data = np.char.mod("%10.0f", dict_comb_items.items())
	# with open('comb_items_'+str(k)+'.csv', 'w') as f:
	# 	np.savetxt(f, np.hstack((rows, data.T)), delimiter=', ', fmt='%s')

	#print(dict_comb_items)
	print(dict_comb_items)
	#print(comb_possible)
	# print(dict_comb_items_binary)
	G = nx.from_numpy_matrix(count_by_items)
	nx.draw(G, with_labels=True, font_weight='bold')
	plt.show()


