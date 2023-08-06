from tqdm import tqdm
import numpy as np
import csv

lbar     = None
norm_log = []
obj_log  = []

def generic_progress_hook(_cur,_tot,_nam):
	if type(_nam) is not str:
		_nam = _nam.decode('utf-8')

	global lbar

	if lbar is None:
		lbar = tqdm(total=_tot, desc=_nam, position=0, leave=True)

	lbar.update(_cur - lbar.n)
	lbar.set_description(_nam)

	if _cur == _tot:
		lbar.close()
		lbar = None

def opt_progress_hook(state_p):
	state = state_p.contents
	global lbar
	global norm_log
	global obj_log

	if lbar is None:
		lbar = tqdm(total=state.max_iterations)
		norm_log.clear()
		obj_log.clear()

	norm_log.append(state.best_norm)
	obj_log.append(state.best_obj)
	
	nrm = state.best_norm
	if nrm > 1:
		nrm = 1
	val = state.best_obj
	if val > 10**50:
		val = np.inf
	
	lbar.set_description( "OPT;" + "{:.4f};{:.4f}".format(nrm,val) )
	lbar.update(1)

	if state.iteration == state.max_iterations:
		lbar.close()
		lbar = None


		
def genfromstrcsv(filename, targets=None, has_header=True):
	N = 0
	n = None
	values = None

	csv_data = open(filename)
	csv_reader = csv.reader(csv_data)
	header = next(csv_reader)
	n = len(header)

	if targets is None:
		targets = range(n)
	values = dict()

	if not has_header:
		N = N+1
		for i in targets:
			if i not in values.keys():
				values[i] = set()
			values[i].add(header[i])

	for row in csv_reader:
		N = N+1
		for i in targets:
			if i not in values.keys():
				values[i] = set()
			values[i].add(row[i])

	vmaps  = dict()
	rvmaps = dict()

	for i in targets:
		j = 0

		if i not in vmaps.keys():
			vmaps[i] = dict()
			rvmaps[i] = dict()

		for v in values[i]:
			vmaps[i][v] = j
			rvmaps[i][j] = v

			j = j+1

	result = np.zeros((N,len(targets)), dtype=np.uint16)


	csv_data.seek(0)

	csv_reader = csv.reader(csv_data)
	header = next(csv_reader)

	if targets is None:
		targets = range(n)

	I = 0
	if not has_header:
		J = 0
		for i in targets:
			result[I,J] = vmaps[i][header[i]]
			J = J + 1
		I = 1

	for row in csv_reader:
		J = 0
		for i in targets:
			result[I,J] = vmaps[i][row[i]]
			J = J + 1
		I = I + 1

	return result, rvmaps

