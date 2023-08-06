__all__ = ['GraphType', 'ModelType', 'InferenceType', 'SamplerType', 'StatisticsType', 'Optimizer']

import ctypes
import time
import numpy
import itertools
import struct
import sys, os
import platform
from .functions import *
from pathlib import Path
path = Path(__file__)

__os  = platform.uname().system
__cpu = platform.uname().machine
__lib = 'lib/libpx'
__ext = 'lib/libpx'
__suf = '.so'

DEBUGMODE = False
if os.environ.get('PX_DEBUGMODE') is not None:
	DEBUGMODE = (os.environ['PX_DEBUGMODE'] == 'True')

if __os == 'Windows': # otherwise: assume linux
	__suf = '.dll' # Tested on Win10 1909 but should work on older Windows versions

if __cpu == 'aarch64': # otherwise: assume x86_64 / AMD64
	__lib += '_aarch64' # Tested NVIDIA Jetson TX1, but might work on other aarch64 systems
	__ext += '_aarch64' # Tested NVIDIA Jetson TX1, but might work on other aarch64 systems

if DEBUGMODE: # Warning: Windows debug core is not included in the pypi package!
	__lib += '_dbg'

pxpath = str( path.parent / (__lib + __suf) )

example_model_filename = str(path.parent / "data/5_14_F.mod")
example_data_filename  = str(path.parent / "data/sin44")

np_type = numpy.float32
ct_type = ctypes.c_float

USE64BIT = False
if os.environ.get('PX_USE64BIT') is not None:
	USE64BIT = os.environ['PX_USE64BIT'] == 'True'
	if USE64BIT:
		np_type = numpy.float64
		ct_type = ctypes.c_double
		example_model_filename = str(path.parent / "data/5_14.mod")

if os.environ.get('PX_EXTINF') is not None:
	extpath = Path(os.environ['PX_EXTINF'])
else:
	extpath = path.parent / (__ext + '_ext_culbp' + __suf) # Warning: Windows CUDA driver is not included in the pypi package!

EXTINF = 0
if extpath.exists():
	ext_lib = ctypes.cdll.LoadLibrary(str(extpath))
	ext_lib.external.restype = ctypes.c_uint64
	ext_lib.external.argtypes = [ctypes.c_uint8, ctypes.c_uint8]
	if not USE64BIT:
		EXTINF = ext_lib.external(4,4)
	else:
		EXTINF = ext_lib.external(3,5)

class disc_t(ctypes.Structure):
	_fields_ = [("num_intervals", ctypes.c_uint64), ("num_moments", ctypes.c_uint64), ("_intervals", ctypes.POINTER(ctypes.c_double)), ("_moments", ctypes.POINTER(ctypes.c_double)), ("mean", ctypes.c_double), ("sdev", ctypes.c_double)]

	__from_file = False
	__intervals = []
	__moments   = []

	@property
	def intervals(self):
		if not self.__from_file:
			return numpy.ctypeslib.as_array(self._intervals, shape = (self.num_intervals, 2))
		else:
			return self.__intervals

	@property
	def moments(self):
		if not self.__from_file:
			return numpy.ctypeslib.as_array(self._moments, shape = (self.num_moments, 5))
		else:
			return self.__moments
			
	def __init__(self, I, M, m, s):
		self.__from_file = True
		self.__intervals = I
		self.__moments = M
		self.mean = m
		self.sdev = s

lib = ctypes.cdll.LoadLibrary(pxpath)

lib.create_ctx.restype = ctypes.c_uint64

lib.version.restype = ctypes.c_uint64

lib.ctx_set_code.restype = ctypes.c_bool

lib.discretize.restype = disc_t
lib.discretize.argtypes = [ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64]

lib.discretize_precomputed.restype = None
lib.discretize_precomputed.argtypes = [ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, disc_t]

lib.reset_ctx.restype  = ctypes.c_bool
lib.reset_ctx.argtypes = [ctypes.c_uint64]

lib.run_ctx.restype  = ctypes.c_bool
lib.run_ctx.argtypes = [ctypes.c_uint64]

lib.destroy_ctx.restype  = None
lib.destroy_ctx.argtypes = [ctypes.c_uint64]

lib.ctx_write_reg.restype  = ctypes.c_bool
lib.ctx_write_reg.argtypes = [ctypes.c_uint64, ctypes.c_char_p, ctypes.c_uint64]

lib.ctx_read_reg.restype  = ctypes.c_uint64
lib.ctx_read_reg.argtypes = [ctypes.c_uint64, ctypes.c_char_p]

MISSING_VALUE = 65535

def array_check(a, name, dtype=None):
	if not isinstance(a, numpy.ndarray):
		raise TypeError(name,'must be of type numpy.ndarray')
	if isinstance(a, numpy.ndarray) and not a.flags['C_CONTIGUOUS']:
		raise TypeError(name,'must be a C-style contiguous numpy array')
	if dtype is not None:
		if isinstance(a, numpy.ndarray) and not a.dtype==dtype:
			raise TypeError('ERROR: type of',a,'must be',str(dtype))

class Graph(ctypes.Structure):
	_fields_ = [("__unused", ctypes.c_uint64), ("__itype", ctypes.c_uint8), ("_nodes", ctypes.c_uint64), ("_edges", ctypes.c_uint64), ("A", ctypes.POINTER(ctypes.c_uint64))]

	__edgelistref = None

	destroyed = False

	@property
	def nodes(self):
		if self.destroyed:
			return 0
		return self._nodes

	@property
	def edges(self):
		if self.destroyed:
			return 0
		return self._edges

	def __len__(self):
		if self.destroyed:
			return 0
		return self.nodes

	def delete(self):
		if not self.destroyed:
			self.destroyed = True
			L = ["GPT "+str(ctypes.addressof(self))+";", "DEL GPT;"]
			recode(L)
			run()

	@property
	def edgelist(self):
		if self.destroyed:
			return numpy.array([])
		res = numpy.ctypeslib.as_array(self.A, shape = (self.edges, 2))
		res.flags.writeable = False
		return res
		
	def add_node_to_dot(self, dot, i, nodenames=None):
		if nodenames is not None and i < len(nodenames):
			dot.node(str(i), nodenames[i])
		elif nodenames is not None and i >= len(nodenames):
			dot.node(str(i), "H"+str(i-len(nodenames)))
		else:
			dot.node(str(i))

	def draw(self,filename,nodenames=None):
		if self.destroyed:
			return
		import os
		from graphviz import Graph
		dot = Graph(comment="pxpy",engine="neato")
		dot.attr(overlap = 'false')
		dot.attr('node', shape='box')
		for i in range(0,self.nodes):
			self.add_node_to_dot(dot,i,nodenames)

		for e in self.edgelist:
			dot.edge(str(e[0]), str(e[1]), len='1.0')

		dot.render(os.path.splitext(filename)[0],format='pdf')
		
	def draw_neighbors(self,target,filename,nodenames=None):
		if self.destroyed:
			return
		import os
		from graphviz import Graph
		dot = Graph(comment="pxpy",engine="neato")
		dot.attr(overlap = 'false')
		dot.attr('node', shape='box')

		self.add_node_to_dot(dot,target,nodenames)
		
		for e in self.edgelist:
			if e[0] == target:
				self.add_node_to_dot(dot,e[1],nodenames)
				dot.edge(str(e[0]), str(e[1]), len='1.0')
			elif e[1] == target:
				self.add_node_to_dot(dot,e[0],nodenames)
				dot.edge(str(e[0]), str(e[1]), len='1.0')

		dot.render(os.path.splitext(filename)[0],format='pdf')

class STGraph(ctypes.Structure):
	_fields_ = [("__unused", ctypes.c_uint64), ("__itype", ctypes.c_uint8), ("T", ctypes.c_uint64), ("base0", ctypes.c_uint64), ("Tm1inv", ct_type)]

	__LOCAL_G = None

	@property
	def base(self):
		if self.__LOCAL_G is None:
			#print("CONSTRUCTING LOCAL_G IN STGraph.base()")
			self.__LOCAL_G = ctypes.cast(self.base0, ctypes.POINTER(Graph))
		return self.__LOCAL_G.contents

	destroyed = False

	def delete(self):
		if not self.destroyed:
			self.base.delete()

	@property
	def nodes(self):
		return self.base.nodes * self.T

	def __len__(self):
		return self.nodes

	@property
	def edges(self):
		return self.base.edges * self.T + (self.T-1) * ( self.base.nodes + 2 * self.base.edges )

	@property
	def edgelist(self):
		if not hasattr(self, 'E'):
			self.E = numpy.zeros((self.edges, 2), dtype = numpy.uint64)

			for v in range(self.base.nodes):
				for t in range(self.T-1):
					e = v * (self.T-1) + t
					self.E[e][0] = t * self.base.nodes + v
					self.E[e][1] = (t + 1) * self.base.nodes + v

			for f in range(self.base.edges):
				a = self.base.edgelist[f][0]
				b = self.base.edgelist[f][1]
				for t in range(self.T-1):
					e = (self.T-1) * self.base.nodes + f * 3 * (self.T-1) + t * 3
					self.E[e + 0][0] = t * self.base.nodes + a
					self.E[e + 0][1] = t * self.base.nodes + b
					self.E[e + 1][0] = t * self.base.nodes + a
					self.E[e + 1][1] = (t + 1) * self.base.nodes + b
					self.E[e + 2][0] = (t + 1) * self.base.nodes + a
					self.E[e + 2][1] = t * self.base.nodes + b

				e = (self.T-1) * self.base.nodes + (self.T-1) * 3 * self.base.edges + f
				self.E[e][0] = (self.T-1) * self.base.nodes + a
				self.E[e][1] = (self.T-1) * self.base.nodes + b

			self.E.flags.writeable = False

		return self.E

	def spatial_vertex(self, v):
		return v % self.base.nodes

	def time(self, v):
		return (v-self.spatial_vertex(v)) / self.base.nodes

	def is_spatial_edge(self, e):
		return self.time(self.edgelist[e][0]) == self.time(self.edgelist[e][1])

class Model(ctypes.Structure):
	"""
	Parameters
	----------
	weights : :class:`numpy.ndarray`
		Model weights
	graph : :py:class:`Graph`
		Undirected graph, representing the conditional independence structure
	states : Integer or 1-dimensional :class:`numpy.ndarray` of length at least :any:`graph.nodes`
		Vertex statespace sizes. Desired output data-type.
	stats : :class:`StatisticsType`, optional
		Determines wether the model's sufficient statistic is minimal or overcomplete (default). 
		For now, setting stats=StatisticsType.minimal requires states=2. 

	See Also
	--------
	:meth:`pxpy.train`, :meth:`pxpy.load_model`, :class:`StatisticsType`
	
	Notes
	-----
	The number of variables in the model is determinded by the number of nodes
	in the :any:`graph` (:any:`Graph.nodes`). Each variables's statespace size is controlled 
	via :any:`states`. If :any:`states` is an integer, all state spaces will be
	of that size. In case :any:`states` is a numpy.ndarray, statespace sizes for each variable
	are read from that array. This requires the user to set all the values in the array. 
	All numpy arrays which are passed to pxpy routines must be C-style contiguous. 
	
	Examples
	--------
	>>> import pxpy as px
	>>> import numpy as np
	>>> G = px.create_graph(px.GraphType.chain,nodes=32) # chain graph with 32 nodes
	>>> w = numpy.random.normal(size=G.nodes+G.edges) # random weight vector
	>>> P = px.Model(w, 2, G, StatisticsType.minimal)
	>>> P.predict()
	"""
	_fields_ = [("itype", ctypes.c_uint8), ("vtype", ctypes.c_uint8), ("from_file", ctypes.c_bool), ("from_python", ctypes.c_bool), ("G", ctypes.c_uint64), ("H", ctypes.c_uint64), ("w", ctypes.POINTER(ct_type)), ("empirical_stats", ctypes.POINTER(ct_type)), ("Y", ctypes.POINTER(ctypes.c_uint64)), ("woffsets", ctypes.POINTER(ctypes.c_uint64)), ("__Ynames", ctypes.POINTER(ctypes.c_uint64)), ("__Xnames", ctypes.POINTER(ctypes.c_uint64)), ("dimension", ctypes.c_uint64), ("offsetdimension", ctypes.c_uint64), ("fulldimension", ctypes.c_uint64), ("gtype", ctypes.c_uint64), ("T", ctypes.c_uint64), ("reparam", ctypes.c_uint64), ("K", ctypes.c_uint64), ("num_instances", ctypes.c_uint64), ("llist", ctypes.c_uint64), ("clist", ctypes.c_uint64)]

	__A         = None
	__observed  = None
	__marginals = None
	__woff      = None
	__voff      = None

	__ysum      = 0

	__weightsref = None
	__statesref  = None
	
	structure_score = 0;

	tree = False

	def __len__(self):
		if self.destroyed:
			return 0
		return self.dimension

	destroyed = False

	def delete(self):
		if not self.destroyed:
			self.__set_ctx_state()
			self.destroyed = True
			L = ["MPT"+str(ctypes.addressof(self))+";", "DEL MPT;"]
			recode(L)
			run()

	def __init__(self, weights, graph, states, stats = StatisticsType.overcomplete):

		super().__init__()

		if not isinstance(graph, Graph):
			raise TypeError('ERROR: graph must be an instance of Graph')

		array_check(weights, "weights")

		if isinstance(states, numpy.ndarray):
			array_check(states, "states", numpy.uint64)
			if len(states) < graph.nodes:
				raise TypeError('ERROR: states must contain one statespace size for each variable in the model')
		elif not isinstance(states, int):
			raise TypeError('ERROR: states must be an int or of type numpy.ndarray with dtype uint64')

		if not isinstance(stats, StatisticsType):
			raise TypeError('ERROR: model must have either covercomplete or minimal sufficient statistics')

		if stats == StatisticsType.minimal and ((isinstance(states, int) and states != 2) or (isinstance(states, numpy.ndarray) and not (numpy.unique(S)[0]==2 or len(numpy.unique(S))==1) )):
			raise TypeError('ERROR: models with minimal sufficient statistics are only supported with 2 states per variable')

		self.itype = 3
		self.vtype = 4
		global USE64BIT
		if USE64BIT == True:
			self.vtype = 5
		self.from_file = False
		self.from_python = True
		self.G = ctypes.addressof(graph)
		self.H = 0

		if isinstance(states, numpy.ndarray):
			self.Y = ctypes.cast(states.ctypes.data, ctypes.POINTER(ctypes.c_uint64))
			self.__statesref = states
		else:
			temp1 = states * numpy.ones(graph.nodes, dtype = numpy.uint64)
			self.Y = ctypes.cast(temp1.ctypes.data, ctypes.POINTER(ctypes.c_uint64))
			self.__statesref = temp1

		self._Model__Ynames = None
		self._Model__Xnames = None

		d = 0
		for e in range(graph.edges):
			d += self.states[graph.edgelist[e][0]] * self.states[graph.edgelist[e][1]]
		self.dimension = int(d)

		if stats == StatisticsType.minimal:
			self.reparam = 12
		else:
			self.reparam = 0

		if len(weights) < d:
			weights.resize(int(d), refcheck = False)
		self.w = ctypes.cast(weights.ctypes.data, ctypes.POINTER(ct_type))
		self.empirical_stats = None
		self.gtype = int(GraphType.other)
		#self.tree = is_tree
		self.T = 1
		self.K = 0
		self.num_instances = 1
		self.llist = 0
		self.clist = 0

		self.__A         = None
		self.__observed  = None
		self.__marginals = None

		self.__weightsref = weights # IMPORTANT! INCREASES REFCOUNT!

		self.prepare()

	def __set_ctx_state(self):
		write_register("MPT", ctypes.addressof(self))
		write_register("GPT", ctypes.addressof(self.graph))
		write_register("REP", self.reparam)
		write_register("GRA", self.gtype)
		#if self.tree:
		#	write_register("TREE", 1)
		#else:
		write_register("TREE", 0)

	def prepare(self):
		offset = 0
		self.obj = 0

		self.__woff = []
		for e in range(self.graph.edges):
			L = self.states[self.graph.edgelist[e][0]] * self.states[self.graph.edgelist[e][1]]
			self.__woff.append(offset)
			offset = offset + L
		self.__woff.append(offset)

		self.__voff = []
		for v in range(self.graph.nodes):
			self.__voff.append(offset)
			offset = offset + self.states[v]
			self.__ysum += self.states[v]
		self.__voff.append(offset)

	@property
	def dim(self):
		if self.destroyed:
			return 0
		if self.reparam == 12:
			return self.graph.nodes + self.graph.edges
		else:
			return self.dimension

	@property
	def time_frames(self):
		if self.destroyed:
			return 0
		return self.T

	@property
	def offsets(self):
		if self.destroyed:
			return numpy.array([])
		return numpy.ctypeslib.as_array(self.woffsets, shape = (self.offsetdimension, )).view(numpy.uint64)
		
	@property
	def weights(self):
		if self.destroyed:
			return numpy.array([])
		if self.vtype == 3:
			return numpy.ctypeslib.as_array(self.w, shape = (self.dim, )).view(numpy.uint64)
		elif self.vtype == 4:
			return numpy.ctypeslib.as_array(self.w, shape = (self.dim, )).view(numpy.float32)
		else:
			return numpy.ctypeslib.as_array(self.w, shape = (self.dim, ))

	def slice_edge(self, e, A):
		if self.destroyed:
			return numpy.array([])
		#if self.reparam == 12:
		#	raise TypeError('ERROR: Edge slicing is only supported for overcomplete models')

		array_check(A,"A")

		if len(A) < self.dimension:
			raise TypeError('ERROR: A must be (at least) ' + str(self.dimension) + ' dimensional')

		return A[int(self.__woff[e]):int(self.__woff[e + 1])]

	def slice_edge_state(self, e, x, y, A):
		if self.destroyed:
			return 0

		array_check(A,"A")

		w = self.slice_edge(e, A)

		s = self.graph.edgelist[e][0]
		t = self.graph.edgelist[e][1]

		idx = int(x * self.states[t] + y)

		return w[idx:(idx + 1)]

	@property
	def statistics(self):
		if self.destroyed:
			return numpy.array([])
		if self.empirical_stats is None:
			return None
		res = 0
		if self.vtype == 3:
			res = numpy.ctypeslib.as_array(self.empirical_stats, shape = (self.fulldimension, )).view(numpy.uint64) / self.num_instances
		elif self.vtype == 4:
			res = numpy.ctypeslib.as_array(self.empirical_stats, shape = (self.fulldimension, )).view(numpy.float32) / self.num_instances
		else:
			res = numpy.ctypeslib.as_array(self.empirical_stats, shape = (self.fulldimension, )) / self.num_instances
		res.flags.writeable = False
		return res[self.offsets[self.graph.nodes]:]

	def phi(self, x):
		if self.destroyed:
			return numpy.array([])
		array_check(x,"x")

		if len(x) != self.graph.nodes:
			raise TypeError('ERROR: x must be ' + str(self.graph.nodes) + ' dimensional')

		phi_x = numpy.zeros(shape = (self.dim, ))

		if self.reparam == 12:
			for v in range(self.graph.nodes):
				if x[v] >= self.states[v]:
					TypeError('ERROR: Some values of x exceed the state space')

				phi_x[v] = int(x[v])

			for e in range(self.graph.edges):

				s = self.graph.edgelist[e][0]
				t = self.graph.edgelist[e][1]

				if x[s] >= self.states[s] or x[t] >= self.states[t]:
					TypeError('ERROR: Some values of x exceed the state space')

				phi_x[int(self.graph.nodes + e)] = int(x[s] * x[v])
		else:
			for e in range(self.graph.edges):

				s = self.graph.edgelist[e][0]
				t = self.graph.edgelist[e][1]

				if x[s] >= self.states[s] or x[t] >= self.states[t]:
					TypeError('ERROR: Some values of x exceed the state space')

				idx = int(self.__woff[e] + x[s] * self.states[t] + x[t])

				phi_x[idx] = 1

		return phi_x

	def score(self, x):
		if self.destroyed:
			return 0
		return numpy.inner(self.weights, self.phi(x))

	def edge_statespace(self, e):
		if self.destroyed:
			return numpy.array([])
		Xs = self.states[self.graph.edgelist[e][0]]
		Xt = self.states[self.graph.edgelist[e][1]]
		return numpy.array(list(itertools.product(range(Xs), range(Xt))))

	def __select_types(self, L):
		L.append("idx_t UINT64;")
		if self.vtype == 3:
			L.append("val_t UINT64;")
		else:
			global USE64BIT
			if not USE64BIT:
				L.append("val_t FLT32;")
			else:
				L.append("val_t FLT64;")

	def save(self, filename):
		if self.destroyed:
			return
		self.__set_ctx_state()
		write_register("OVW", 1)
		L = []
		self.__select_types(L)
		L.append("MFN \"" + filename + "\";")
		L.append("STORE MPT;")
		recode(L)
		run()

	def __load_observed(self, observed, L):
		if observed is not None:
			array_check(observed,"observed")
			if len(observed.shape) == 1:
				observed = observed.reshape(1, len(observed))
			if len(observed.shape) != 2:
				raise ValueError('ERROR: observed must be 1 or 2 dimensional')

		data_ptr = ctypes.c_uint64(observed.ctypes.data)
		L.append("DEL DPT;")
		L.append("EDP " + str(data_ptr.value) + ";")
		L.append("NXX " + str(len(observed)) + ";")
		L.append("GPX " + str(len(observed) * len(observed[0]) * 2) + ";")
		L.append("LDX DPT;")

	def predict(self, observed, progress_hook = 0, iterations = None, inference = InferenceType.belief_propagation):
		if self.destroyed:
			return numpy.array([])
		if not isinstance(inference, InferenceType):
			raise TypeError('ERROR: inference must be an instance of InferenceType Enum')

		L = []
		self.__select_types(L)
		self.__set_ctx_state()
		self.__load_observed(observed, L)

		if progress_hook != 0:
			f3 = prg_func(progress_hook)
			write_register("CBP", ctypes.c_uint64.from_buffer(f3).value)
		else:
			write_register("CBP", 0)
			
		if iterations is None:
			iterations = self.graph.nodes

		write_register("PGX", 0)
		write_register("MIL", iterations)
		write_register("INF", int(inference))

		L.append("PREDICT;")

		recode(L)
		run()

		return observed

	def sample(self, observed = None, num_samples = None, sampler = SamplerType.apx_perturb_and_map, progress_hook = 0, iterations = None, perturbation = 0.1, burn = 100, inference = InferenceType.belief_propagation):
		if self.destroyed:
			return numpy.array([])
		if not isinstance(sampler, SamplerType):
			raise TypeError('ERROR: sampler must be an instance of SamplerType Enum')

		if not ((observed is None) != (num_samples is None)):
			raise ValueError('ERROR: either observed or num_samples must be set (and not both)')

		L = []
		L.append("idx_t UINT64;")
		self.__select_types(L)
		self.__set_ctx_state()

		if observed is None:
			observed = numpy.full(shape = (num_samples, self.graph.nodes), fill_value = MISSING_VALUE, dtype = numpy.uint16)

		self.__load_observed(observed, L)

		if progress_hook != 0:
			f3 = prg_func(progress_hook)
			write_register("CBP", ctypes.c_uint64.from_buffer(f3).value)
		else:
			write_register("CBP", 0)

		if iterations is None:
			iterations = self.graph.nodes

		if sampler == SamplerType.apx_perturb_and_map:
			write_register("PAM", integer_from_float(perturbation))
			write_register("MIL", iterations)
			write_register("INF", int(inference))

		elif sampler == SamplerType.gibbs:
			write_register("PAM", 0)
			write_register("GRE", burn) # unified burn-in and resamplings between two samples

		L.append("SAMPLE;")
		recode(L)
		run()

		return numpy.array(observed)


	def infer(self, observed = None, inference = InferenceType.belief_propagation, iterations = None, k = 3):
		if self.destroyed:
			return numpy.array([])
		if not isinstance(inference, InferenceType):
			raise TypeError('ERROR: inference must be an instance of InferenceType Enum')

		L = []
		self.__select_types(L)
		self.__set_ctx_state()

		if observed is not None:
			self.__load_observed(observed, L)
		else:
			L.append("DEL DPT;")
			L.append("DPT 0;")
			
		if iterations is None:
			iterations = self.graph.nodes

		write_register("KXX", k)
		write_register("MIL", iterations)
		write_register("INF", int(inference))

		L.append("INFER;")
		recode(L)
		run()

		P = ctypes.cast(int(read_register("PPT")), ctypes.POINTER(ctypes.c_double))

		res = numpy.array(numpy.ctypeslib.as_array(P, shape = (int(self.dimension + self.__ysum), )))
		#res.flags.writeable = False

		self.__observed  = observed
		self.__marginals = res
		self.__A         = float_from_integer(read_register("LNZ"))

		return self.__marginals, self.__A

	@property
	def MAP(self):
		if self.destroyed:
			return numpy.array([])
		x = numpy.full(shape = (1, self.graph.nodes), fill_value = MISSING_VALUE, dtype = numpy.uint16)
		self.predict(x)
		return x

	@property
	def LL(self):
		if self.destroyed:
			return 0
		N = self.num_instances

		P, A = self.infer()
		return N*(numpy.inner(self.weights, self.statistics) - A)

	@property
	def BIC(self):
		if self.destroyed:
			return 0
		N = self.num_instances
		k = numpy.linalg.norm(self.weights, ord=0)
		P, A = self.infer()
		lnL = N*(numpy.inner(self.weights, self.statistics) - A)
		return numpy.log(N)*k - 2*lnL

	@property
	def AIC(self):
		if self.destroyed:
			return 0
		N = self.num_instances
		k = numpy.linalg.norm(self.weights, ord=0)
		P, A = self.infer()
		lnL = N*(numpy.inner(self.weights, self.statistics) - A)
		return 2*k - 2*lnL

	__LOCAL_G = None
	__OLD_G = None

	@property
	def graph(self):
		if (self.__LOCAL_G is None) or (self.__OLD_G != self.G):
			self.__OLD_G = self.G
			#print("CONSTRUCTING LOCAL_G IN Model.graph()")
			if self.gtype == 11:
				self.__LOCAL_G = ctypes.cast(self.G, ctypes.POINTER(STGraph)).contents
			else:
				self.__LOCAL_G = ctypes.cast(self.G, ctypes.POINTER(Graph)).contents
		return self.__LOCAL_G

	@property
	def base_graph(self):
		if self.destroyed:
			return None
		self.__set_ctx_state()
		L = []
		self.__select_types(L)
		L.append("BASEGRAPH;")
		recode(L)
		run()
		G = ctypes.cast(read_register("RES"), ctypes.POINTER(Graph)).contents
		return G
		
	@property
	def states(self):
		if self.destroyed:
			return numpy.array([])
		res = numpy.ctypeslib.as_array(self.Y, shape = (self.graph.nodes, ))
		return res

	def probv(self, v, x):
		if self.destroyed:
			return 0
		if self.__marginals is None:
			raise RuntimeError('ERROR: you must call infer first')

		return self.__marginals[int(self.__voff[v]+x)]

	def prob(self, v, x, w = None, y = None):
		if self.destroyed:
			return 0
		if self.__marginals is None:
			raise RuntimeError('ERROR: you must call infer first')

		if w is None or y is None:
			return self.probv(v, x)

		a0 = numpy.bincount(numpy.where(self.graph.edgelist==[v,w])[0])
		a1 = numpy.bincount(numpy.where(self.graph.edgelist==[w,v])[0])

		b0 = numpy.max(a0)
		b1 = numpy.max(a1)

		if b0 != 2 and b1 != 2:
			return self.prob(v,x) * self.prob(w,y)

		v0 = v
		v1 = w
		x0 = x
		x1 = y

		if b0 == 2:
			e = numpy.argmax(a0)
		else:
			e = numpy.argmax(a1)
			v0 = w
			v1 = v
			x0 = y
			x1 = x

		return self.__marginals[int(self.__woff[e] + x0 * self.states[x1] + x1)]

class progress_t(ctypes.Structure):
	_fields_ = [("_obj", ct_type), ("norm", ct_type), ("stepsize", ct_type), ("min_stepsize", ct_type), ("lambda_proximal", ct_type), ("lambda_regularization", ct_type), ("iteration", ctypes.c_uint64), ("max_iterations", ctypes.c_uint64), ("dim", ctypes.c_uint64), ("_w", ctypes.POINTER(ct_type)), ("_g", ctypes.POINTER(ct_type)), ("_e", ctypes.POINTER(ct_type)), ("is_int", ctypes.c_bool), ("_best_obj", ct_type), ("best_norm", ct_type), ("_best_w", ctypes.POINTER(ct_type)), ("value_bytes", ctypes.c_uint64), ("_model", ctypes.POINTER(Model))]

	@property
	def obj(self):
		if self.is_int != 0:
			return self._obj / 255.0
		else:
			return self._obj

	@property
	def best_obj(self):
		if self.is_int != 0:
			return self._best_obj / 255.0
		else:
			return self._best_obj

	@property
	def model(self):
		mod = self._model.contents
		mod.prepare()
		mod.obj = self.obj
		return mod

	@property
	def weights(self):
		if self.is_int != 0:
			return numpy.ctypeslib.as_array(self._w, shape = (self.dim, )).view(numpy.uint64)
		else:
			return numpy.ctypeslib.as_array(self._w, shape = (self.dim, ))

	@property
	def weights_extrapolation(self):
		if self.is_int != 0:
			return numpy.ctypeslib.as_array(self._e, shape = (self.dim, )).view(numpy.uint64)
		else:
			return numpy.ctypeslib.as_array(self._e, shape = (self.dim, ))

	@property
	def best_weights(self):
		if self.is_int != 0:
			return numpy.ctypeslib.as_array(self._best_w, shape = (self.dim, )).view(numpy.uint64)
		else:
			return numpy.ctypeslib.as_array(self._best_w, shape = (self.dim, ))

	@property
	def gradient(self):
		if self.is_int != 0:
			return numpy.ctypeslib.as_array(self._g, shape = (self.dim, )).view(numpy.uint64)
		else:
			return numpy.ctypeslib.as_array(self._g, shape = (self.dim, ))

if platform == "win32":
	opt_func = ctypes.WINFUNCTYPE(None, ctypes.POINTER(progress_t))
	prg_func = ctypes.WINFUNCTYPE(None, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_char_p)
else:
	opt_func = ctypes.CFUNCTYPE(None, ctypes.POINTER(progress_t))
	prg_func = ctypes.CFUNCTYPE(None, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_char_p)


ctx = ctypes.c_uint64(lib.create_ctx())

def write_register(name, val):
	l = len(name)
	buff = ctypes.create_string_buffer(l + 1)
	buff.value = name.encode('utf-8')
	ptr = (ctypes.c_char_p)(ctypes.addressof(buff))
	return lib.ctx_write_reg(ctx, ptr, val)

write_register("SEED", int(round(time.time() * 1000)))
write_register("EXT0", EXTINF)

def squared_l2_regularization(state_p):
	state = state_p.contents
	numpy.copyto(state.gradient, state.gradient + 2.0 * state.lambda_regularization * state.weights)
	state.norm = numpy.linalg.norm(state.gradient, ord=numpy.inf)

	if state.iteration == 0:
		state.min_stepsize = 1.0/(1.0/state.min_stepsize + 2.0 * state.lambda_regularization) # TODO: Add this fact to the book!

def prox_l1(state_p):
	state = state_p.contents
	l = state.lambda_proximal * state.stepsize

	x = state.weights_extrapolation - state.stepsize * state.gradient

	numpy.copyto(state.weights, 0, where=numpy.absolute(x)<l)
	numpy.copyto(state.weights, x-l, where=x>l)
	numpy.copyto(state.weights, x+l, where=-x>l)

def version():
	return lib.version()

def discretize(data, num_states = None, targets = None, discretization = None, progress_hook = None):
	array_check(data,"data")
	
	if numpy.issubdtype(data.dtype, numpy.integer):
		print("WARN: Discretization might fail on non-floating-point types!")

	if num_states is None and discretization is None:
		raise ValueError('ERROR: either a desired number of states or a precomputed discretization must be provided')

	columns = len(data[0])

	R = numpy.zeros(shape = (len(data), columns), dtype = numpy.uint16)
	M = []

	if targets is None:
		targets = range(columns)

	for t in range(columns):
		col_data = numpy.ascontiguousarray(data[:, t])
		distinct = len(numpy.unique(col_data))

		if t in targets:# and distinct > num_states:
			result = numpy.zeros(shape = (len(data), ), dtype = numpy.uint16)
			
			# interpret NaN-values as missing values and filter them out before discretization
			mask = (numpy.isnan(col_data))
			temp = numpy.delete(col_data,mask)
			
			if progress_hook is not None:
				progress_hook(t+1,columns,"DSCRT")

			if len(temp) == 0:
				disc_info = None
			elif discretization is None and num_states is not None:
				disc_info = lib.discretize(ctypes.c_uint64(result.ctypes.data), ctypes.c_uint64(temp.ctypes.data), ctypes.c_uint64(len(temp)), ctypes.c_uint64(num_states))
			else:
				disc_info = discretization[t]
				lib.discretize_precomputed(ctypes.c_uint64(result.ctypes.data), ctypes.c_uint64(temp.ctypes.data), ctypes.c_uint64(len(temp)), disc_info)
				
			# restore missing values
			j = 0
			col_data = numpy.array([], dtype = numpy.uint16)
			for i in range(0,len(mask)):
				if mask[i]:
					col_data = numpy.append(col_data, MISSING_VALUE)
				else:
					col_data = numpy.append(col_data, result[j])
					j = j+1
					
			if len(col_data) != len(mask):
				raise TypeError('ERROR: this cannot happen!')
					
			M.append(disc_info)
			R[:, t] = col_data
		else:
			M.append(None)
			R[:, t] = col_data
			
	if progress_hook is not None and columns not in targets:
		progress_hook(columns,columns,"DSCRT")

	return R, M

def undiscretize(data, M, progress_hook = None, lower_tail_factor = 0.0, upper_tail_factor = 0.0, deterministic = False):
	array_check(data,"data")

	R = numpy.zeros(shape = (len(data), len(data[0])))
	
	i = 0
	r,c = data.shape
	N = r*c
	
	with numpy.nditer(data, flags = ['multi_index']) as it:
		while not it.finished:
			if progress_hook is not None:
				progress_hook(i+1,N,"UDISC")
				i=i+1
			row = it.multi_index[0]
			col = it.multi_index[1]
			if data[row,col] == MISSING_VALUE:
				R[row, col] = numpy.nan
			elif col < len(M) and M[col] is not None:

				state = it[0]
				
				m = M[col].moments[state][0]
				s = numpy.sqrt(M[col].moments[state][1])
				
				l = M[col].intervals[state][0]
				u = M[col].intervals[state][1]
				
				Y = len(M[col].intervals)
				if state == Y-1: # upper bound is infty
					u += (u-m) * upper_tail_factor
					
				if state == 0: # lower bound is -infty
					l -= (m-l) * lower_tail_factor

				if deterministic:
					val = m
				else:
					val = numpy.random.default_rng().normal(m,s)

				while val < l or val > u: # truncated normal
					val = numpy.random.default_rng().normal(m,s)

				R[row, col] = val * M[col].sdev + M[col].mean
			it.iternext()
			
	if progress_hook is not None:
		progress_hook(N,N,"UDISC")
	return R

def destroy():
	if ctx is None:
		assert False
	lib.destroy_ctx(ctx)

def read_register(name):
	l = len(name)
	buff = ctypes.create_string_buffer(l + 1)
	buff.value = name.encode('utf-8')
	ptr = (ctypes.c_char_p)(ctypes.addressof(buff))
	return lib.ctx_read_reg(ctx, ptr)

def recode(code):
	n = len(code)
	l = 0
	for stmt in code:
		if len(stmt) > l:
			l = len(stmt)
	buffs = [ctypes.create_string_buffer(l + 1) for i in range(len(code))]
	for index, stmt in enumerate(code):
		buffs[index].value = code[index].encode('utf-8')
	ptrs = (ctypes.c_char_p * n)( * map(ctypes.addressof, buffs))
	lib.ctx_set_code(ctx, ptrs, n)
	return n
	
def run(code=None):
	if ctx is None:
		assert False
	if code is not None:
		recode(code)
	lib.run_ctx(ctx)

def set_seed(s):
	write_register("SEED", s)

def float_from_integer(val):
#	global USE64BIT
#	if not USE64BIT:
#		return struct.unpack('f', struct.pack('I', val))[0]
#	else:
	return struct.unpack('d', struct.pack('N', val))[0]		

def integer_from_float(val):
#	global USE64BIT
#	if not USE64BIT:
#		return struct.unpack('N', struct.pack('xxxxf', val))[0]
#	else:
	return struct.unpack('N', struct.pack('d', val))[0]

def KL(p, q):
	array_check(p,"p")
	array_check(q,"q")

	#if len(p) != len(q):
	#	raise TypeError('ERROR: p and q must have same length')

	res = 0
	for i in range(min(len(p),len(q))):
		res = res + p[i] * (numpy.log(p[i]) - numpy.log(q[i]))

	return res
	
def save_discretization(fn, U):
	temp = dict()
	for i in range(0,len(U)):
		temp['ints'+str(i)] = U[i].intervals
		temp['moms'+str(i)] = U[i].moments
		temp['mean'+str(i)] = U[i].mean
		temp['sdev'+str(i)] = U[i].sdev
	numpy.savez_compressed(fn,**temp)

def load_discretization(fn):
	U = []
	temp = numpy.load(fn, allow_pickle = True)
	n = int(len(temp)/4)
	for i in range(0,n):
		I = temp['ints'+str(i)]
		M = temp['moms'+str(i)]
		m = temp['mean'+str(i)]
		s = temp['sdev'+str(i)]
		U.append(disc_t(I,M,m,s))
	return U

# TODO: howto load integer model?
def load_model(filename):
	L = []
	L.append("idx_t UINT64;")
	global USE64BIT
	if not USE64BIT:
		L.append("val_t FLT32;")
	else:
		L.append("val_t FLT64;")
	L.append("MFN \"" + filename + "\";")
	L.append("LDX MPT;")
	L.append("DEL MFN;")
#	L.append("DEL LPT;")
#	L.append("DEL IGN;")
	recode(L)
	run()
	mod = ctypes.cast(read_register("MPT"), ctypes.POINTER(Model)).contents
	mod.prepare()
	return mod

def create_graph(G, nodes=None, target=None):
	if isinstance(G, numpy.ndarray) and len(G[0]) != 2:
		array_check(G,"G",dtype=numpy.uint64)
	elif isinstance(G, GraphType) and nodes is None:
		raise TypeError('ERROR: G must be an instance of GraphType or numpy.ndarray with dtype uint64')

	if isinstance(G, GraphType) and  G==3 and target is None:
		raise ValueError('ERROR: Star graph requires a target node')

	if target is not None:
		write_register("CEN", int(target))		

	write_register("DPT", 0)
	write_register("MPT", 0)
	write_register("GPT", 0)
	lib.reset_ctx(ctx)
	write_register("EXT0", EXTINF) # TODO: lib.reset_ctx should not delete value of EXTI

	L = []
	L.append("idx_t UINT64;")

	if isinstance(G, GraphType):
		L.append("GVX " + str(nodes) + ";")
		L.append("GRA " + str(int(G)) + ";")
	else:
		M = numpy.amax(G)
		V = numpy.unique(G)
		n = len(V)
		m = len(G)
		s = numpy.sum(V)

		if (n != M + 1) or (s != (M * (M + 1))/2):
			raise ValueError('ERROR: GraphType is invalid')

		data_ptr = ctypes.c_uint64(G.ctypes.data)

		L.append("EAP " + str(data_ptr.value) + ";")
		L.append("GVX " + str(n) + ";")
		L.append("GEX " + str(m) + ";")
		L.append("GRA " + str(int(GraphType.custom)) + ";")

	L.append("LDX GPT;")
	recode(L)
	run()

	G = ctypes.cast(read_register("GPT"), ctypes.POINTER(Graph)).contents
	G._Graph__edgelistref = G # IMPORTANT! INCREASES REFCOUNT!

	return G

def train(data=None, graph=None, mode = ModelType.mrf, inference = InferenceType.belief_propagation, iters = 1000, seed = 0, k = 3, input_model = None, initial_stepsize = 0.1, opt_progress_hook = 0, progress_hook = 0, regularization = 0, proximal_operator = 0, T = 1, threshold = 0.0, lambda_proximal = 0, lambda_regularization = 0, shared_states = False, optimizer = Optimizer.accelerated_proximal_gradient, zero_init=False, clique_size = 3):
	"""Return a new matrix of given shape and type, without initializing entries.

	Parameters
	----------
	shape : int or tuple of int
		Shape of the empty matrix.
	dtype : data-type, optional
		Desired output data-type.
	order : {'C', 'F'}, optional
		Whether to store multi-dimensional data in row-major
		(C-style) or column-major (Fortran-style) order in
		memory.

	See Also
	--------
	empty_like, zeros

	Notes
	-----
	`empty`, unlike `zeros`, does not set the matrix values to zero, 
	and may therefore be marginally faster. On the other hand, it requires
	the user to manually set all the values in the array, and should be
	used with caution.

	Examples
	--------
	>>> import numpy.matlib
	>>> numpy.matlib.empty((2, 2))	# filled with random data
	matrix([[  6.76425276e-320,   9.79033856e-307], # random
			[  7.39337286e-309,   3.22135945e-309]])
	>>> numpy.matlib.empty((2, 2), dtype = int)
	matrix([[ 6600475, 		0], # random
			[ 6586976, 22740995]])

	"""

	if input_model is None and graph is None:
		raise TypeError('ERROR: either input_model or graph must be defined')

	if graph is not None and (not (isinstance(graph, GraphType) or isinstance(graph, Graph))):
		raise TypeError('ERROR: graph must be an instance of GraphType enum or Graph class')

	if input_model is not None and not isinstance(input_model, Model):
		raise TypeError('ERROR: input_model must be an instance of Model class')

	if not isinstance(mode, ModelType):
		raise TypeError('ERROR: mode must be an instance of ModelType enum')

	if not isinstance(inference, InferenceType):
		raise TypeError('ERROR: inference must be an instance of InferenceType enum')

	write_register("MPT", 0)
	write_register("GPT", 0)
	lib.reset_ctx(ctx)
	write_register("EXT0", EXTINF) # TODO: lib.reset_ctx should not delete value of EXTI

	if opt_progress_hook != 0:
		f1 = opt_func(opt_progress_hook)
		write_register("CBO", ctypes.c_uint64.from_buffer(f1).value)
	else:
		write_register("CBO", 0)

	if regularization != 0:
		f2 = opt_func(regularization)
		write_register("CBU", ctypes.c_uint64.from_buffer(f2).value)
	else:
		write_register("CBU", 0)

	if progress_hook != 0:
		f3 = prg_func(progress_hook)
		write_register("CBP", ctypes.c_uint64.from_buffer(f3).value)
	else:
		write_register("CBP", 0)

	if proximal_operator != 0:
		f4 = opt_func(proximal_operator)
		write_register("CPR", ctypes.c_uint64.from_buffer(f4).value)
	else:
		write_register("CPR", 0)

	L = []
	L.append("DEL MPT;");

	if mode == ModelType.integer:
		L.append("idx_t UINT64;")
		L.append("val_t UINT64;")
		L.append("ALG IGD;")
	else:
		write_register("STP", integer_from_float(initial_stepsize))
		L.append("idx_t UINT64;")
		if not USE64BIT:
			L.append("val_t FLT32;")
		else:
			L.append("val_t FLT64;")
		L.append("ALG "+str(int(optimizer))+";")

	if seed != 0:
		write_register("SEED", seed)
	write_register("MIS", ord('?'))
	write_register("SEP", ord(','))
	write_register("OVW", 1)
	write_register("HED", 0)
	write_register("LSN", 2)

	write_register("INF", int(inference))
	write_register("MIO", iters)
	write_register("EPO", 0)
	write_register("LAM", integer_from_float(lambda_proximal))
	write_register("ELAM", integer_from_float(lambda_regularization))

	if mode >= ModelType.strf_linear and mode <= ModelType.strf_inv_exponential:
		write_register("TXX", T)
		write_register("YYC", 1)
	else:
		write_register("TXX", 1)
		write_register("YYC", 0)
		write_register("REP", 0)

	if shared_states:
		write_register("YYC", 1)

	if data is not None:
		array_check(data,"data",dtype=numpy.uint16)

		data_ptr = ctypes.c_uint64(data.ctypes.data)

		l = len(data[0])

		L.append("EDP " + str(data_ptr.value) + ";")
		L.append("NXX " + str(len(data)) + ";")
		L.append("GPX " + str(len(data) * l * 2) + ";")
		L.append("LDX DPT;")
		
		L.append("MIL " + str(l) +";") # len(data[0]) is number of columns

	if input_model is None:
		if isinstance(graph, Graph):
			L.append("GRA " + str(int(GraphType.custom)) + ";")
			L.append("GPT " + str(ctypes.addressof(graph)) + ";")
		else:
			L.append("GRA " + str(int(graph)) + ";")
			#if graph == GraphType.chain or graph == GraphType.auto_tree:
			#	L.append("TREE 1;")				
			#else:
			#	L.append("TREE 0;")
			L.append("TREE 0;")
			L.append("KXX "+str(clique_size)+";")
			L.append("LDX GPT;")
			
			L.append("MOV MIL GVX;") # GVX is number of vertices

		write_register("PEL", integer_from_float(threshold))
			
		L.append("MODEL;")
		L.append("MOV GP1 RES;")

		if mode == ModelType.dbt:
			L.append("DEL MPT;")
			L.append("GRA DBT;")
			L.append("BOLTZMANNTREE;")
			L.append("INITLATENT;")
			L.append("MODEL;")

		elif mode >= ModelType.strf_linear and mode <= ModelType.strf_inv_exponential and T>1:
			L.append("DEL MPT;")
			L.append("GRA OTHER;")
			L.append("STGRAPH;")
			L.append("TREE 0;")
			L.append("REP " + str(int(mode)) + ";")
			L.append("MODEL;")

		if not zero_init and mode != ModelType.integer: # and regularization == 0 and proximal_operator == 0:
			L.append("CLOSEDFORM;")

	else:
		L.append("MPT " + str(ctypes.addressof(input_model)) + ";")
		L.append("GPT " + str(ctypes.addressof(input_model.graph)) + ";")
		L.append("REP " + str(input_model.reparam) + ";")
		L.append("GRA " + str(input_model.gtype) + ";")
		
		L.append("MOV MIL GVX;") # GVX is number of vertices
		
		L.append("TREE 0;")
		
	L.append("KXX "+str(k)+";")

#		if input_model is not None and data.shape[1] != input_model.graph.nodes:
#			raise TypeError('ERROR: dimension mismatch in data and input_model')

#		L.append("STATS;")

	L.append("ESTIMATE;")

	recode(L)
	run()
	#import pdb; pdb.set_trace()
	mod = ctypes.cast(read_register("MPT"), ctypes.POINTER(Model)).contents
	mod.prepare()

	res = read_register("RES")
	if mode != ModelType.integer:
		res = float_from_integer(res)

	mod.obj = res
	
	sts = read_register("GP1")
	if mode != ModelType.integer:
		sts = float_from_integer(sts)

	mod.structure_score = sts

	return mod
