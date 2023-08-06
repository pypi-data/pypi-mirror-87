import hashlib
import numpy as np
import pxpy as px
from pxpy import *

##############################################################################################################

def test_init():
	assert px.version() == 10055

def test_recode():
	code = []
	ret = px.recode(code)

	assert ret == 0

	px.run()
	code = ['GPS \"THIS IS PX\";', 'DEL GPS;']
	ret = px.recode(code)
	px.run()

	assert ret == 2

def test_register():
	px.write_register("LSN", 4)

	assert px.read_register("LSN") == 4
	
def test_discretization():
	A = np.array([np.arange(10.0)]).reshape(10,1)
	
	eps = 0.00000001
	
	_,U1 = px.discretize(A,32) # bins > distinct values

	assert U1[0].num_intervals == 10
	assert U1[0].num_intervals == U1[0].num_moments

	m = U1[0].mean
	s = U1[0].sdev

	for i in range(0,10):
		assert np.abs(U1[0].moments[i][0] * s + m - i * 1.0) < eps

	_,U2 = px.discretize(A,3)

	m = U2[0].mean
	s = U2[0].sdev

	assert U2[0].num_intervals == 3
	assert U2[0].num_intervals == U2[0].num_moments

	assert np.abs(U2[0].moments[0][0] * s + m - (0+1+2) / 3)   < eps
	assert np.abs(U2[0].moments[1][0] * s + m - (3+4+5) / 3)   < eps
	assert np.abs(U2[0].moments[2][0] * s + m - (6+7+8+9) / 4) < eps

	assert np.abs(U2[0].moments[0][1] * s * s - 1)   < eps
	assert np.abs(U2[0].moments[1][1] * s * s - 1)   < eps
	assert np.abs(U2[0].moments[2][1] * s * s - 5/3) < eps

def test_train_strf():
	D = np.genfromtxt(px.example_data_filename, delimiter=',', skip_header=1, dtype=np.uint16)

	model = px.train(data=D, iters=100, T=4, lambda_proximal=0.5, lambda_regularization=0.1, graph=GraphType.chain, mode=ModelType.strf_rational, proximal_operator=px.prox_l1, regularization=px.squared_l2_regularization)

	assert hashlib.sha1(model.graph.edgelist).hexdigest() == "305f3755d5e5e8926ed18f2727a2c97faec8d92d"
	assert abs(model.obj - 6.2408) < 0.0001

	model.graph.delete()
	model.delete()

def test_train_mrf():
	D = np.genfromtxt(px.example_data_filename, delimiter=',', skip_header=1, dtype=np.uint16)

	model = px.train(data=D, iters=100, graph=GraphType.auto_tree, mode=ModelType.mrf)

	x = np.zeros(shape=(model.graph.nodes, ))
	score = np.dot(model.weights, model.phi(x))

	if not px.USE64BIT:
		assert hashlib.sha1(model.slice_edge(e=model.graph.edges-1, A=model.statistics)).hexdigest() == "c255515b5fa926d5659ad3fad969414fb1ba22b0"
	else:
		assert hashlib.sha1(model.slice_edge(e=model.graph.edges-1, A=model.statistics)).hexdigest() == "01d5b81d412908717198f197de24d3e1e39a800a"	
	assert hashlib.sha1(model.graph.edgelist).hexdigest() == "d3a50e11e1d42a530968179054b2dd4f77b40d46"
	assert abs(model.obj - 3.8664) < 0.0001
	assert abs(score - -41.3515) < 0.0001

	model.graph.delete()
	model.delete()

def test_train_intmrf():
	D = np.genfromtxt(px.example_data_filename, delimiter=',', skip_header=1, dtype=np.uint16)
	model = px.train(data=D, iters=100, graph=GraphType.auto_tree, k=6, mode=ModelType.integer)

	probs, A = model.infer()

	assert hashlib.sha1(model.graph.edgelist).hexdigest() == "d3a50e11e1d42a530968179054b2dd4f77b40d46"
	assert px.KL(model.statistics, probs)/model.graph.edges < 0.1
	assert model.obj == 9

	model.graph.delete()
	model.delete()

def test_train_dbt():
	D = np.genfromtxt(px.example_data_filename, delimiter=',', skip_header=1, dtype=np.uint16)
	model = px.train(data=D, iters=1000, graph=GraphType.auto, clique_size=3, mode=ModelType.dbt)

	assert hashlib.sha1(model.graph.edgelist).hexdigest() == "ced4afd5864e2e4bebec94f4015e0cb388c65b5e"

	if px.USE64BIT:
		assert abs(model.obj - 11.3746) < 0.0001
	else:
		assert abs(model.obj - 11.3737) < 0.0001
		
	model.graph.delete()
	model.delete()

def test_infer():
	D = np.genfromtxt(px.example_data_filename, delimiter=',', skip_header=1, dtype=np.uint16)
	model = px.train(data=D, iters=100, inference=InferenceType.junction_tree, lambda_proximal=10, graph=GraphType.grid, mode=ModelType.mrf, proximal_operator=px.prox_l1)

	probs,  A_jt  = model.infer(inference=InferenceType.junction_tree)
	probs_jt = probs
	probs, A_lbp = model.infer(inference=InferenceType.belief_propagation)
	probs_lbp = probs
	probs, A_sqm = model.infer(inference=InferenceType.stochastic_quadrature, iterations=10000)
	probs_sqm = probs

	print(probs_jt)
	print(probs_lbp)
	print(probs_sqm)

	assert px.KL(probs_jt, probs_lbp)/model.graph.edges < 0.1
	assert px.KL(probs_jt, probs_sqm)/model.graph.edges < 0.1

	model.graph.delete()
	model.delete()

	#print("Average KL of estimated edge marginals:")
	#print("KL[jt || lbp] = "+str(px.KL(probs_jt, probs_lbp)/model.graph.edges))
	#print("KL[jt || sqm] = "+str(px.KL(probs_jt, probs_sqm)/model.graph.edges))
	#print("Log-partition function values:")
	#print("A_jt="+str(A_jt) + ", A_lbp=" + str(A_lbp) + ", A_sqm=" + str(A_sqm))

def test_load_model():
	model = px.load_model(px.example_model_filename)

	assert model.graph.nodes == 784
	assert model.graph.edges == 783
	assert model.dim == 1567 # minimal dim

	assert len(model) == 3132 # overcomplete dim
	assert len(model.graph) == model.graph.nodes

	model.graph.delete()
	model.delete()

def test_optimization_hooks():
	D = np.genfromtxt(px.example_data_filename, delimiter=',', skip_header=1, dtype=np.uint16)

	model = px.train(data=D, iters=100, graph=GraphType.chain, mode=ModelType.mrf)
	l1_ml = np.linalg.norm(model.weights, ord=1)
	l2_ml = np.linalg.norm(model.weights, ord=2)

	model.graph.delete()
	model.delete()

	model = px.train(data=D, iters=100, graph=GraphType.chain, mode=ModelType.mrf, regularization=px.squared_l2_regularization, lambda_regularization=0.1)
	l1_sl2reg = np.linalg.norm(model.weights, ord=1)
	l2_sl2reg = np.linalg.norm(model.weights, ord=2)

	model.graph.delete()
	model.delete()

	model = px.train(data=D, iters=100, graph=GraphType.chain, mode=ModelType.mrf, proximal_operator=px.prox_l1, lambda_proximal=10)
	l1_l1reg = np.linalg.norm(model.weights, ord=1)
	l2_l1reg = np.linalg.norm(model.weights, ord=2)

	model.graph.delete()
	model.delete()

	assert l1_ml > l1_sl2reg and l1_sl2reg > l1_l1reg
	assert l2_ml > l2_sl2reg and l2_sl2reg > l2_l1reg

def test_predict():
	model = px.load_model(px.example_model_filename)
	model.tree = False

	x = -np.ones(shape=(1, model.graph.nodes), dtype=np.uint16)
	model.predict(x)

	assert hashlib.sha1(x).hexdigest() == "ebe4aa3730d88aa9b336b4ad4e0e00e6c5262ed9"

	model.graph.delete()
	model.delete()

def test_sampler():
	model = px.load_model(px.example_model_filename)
	model.tree = False

	px.set_seed(1337)
	
	# TODO: sample many, compute average, and assert that distance to sufficient statistic is small

	A = model.sample(sampler=SamplerType.apx_perturb_and_map, num_samples=2)
	B = model.sample(sampler=SamplerType.gibbs, num_samples=2)

	assert hashlib.sha1(A).hexdigest() == "7a35262c84843b21e1bdac1a686503c07b793af1"
	assert hashlib.sha1(B).hexdigest() == "a7e736f9de2513fb9fc11e582ec127ff7044d787"

	model.graph.delete()
	model.delete()

def test_custom_graph():
	D = np.genfromtxt(px.example_data_filename, delimiter=',', skip_header=1, dtype=np.uint16)

	E = np.array([0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 0, 7, 0, 8, 0, 9, 0, 10, 0, 11, 0, 12, 0, 13, 0, 14, 0, 15], dtype = np.uint64).reshape(15, 2)
	G = px.create_graph(E)

	model = px.train(data=D, iters=100, graph=G, mode=ModelType.mrf)

	assert hashlib.sha1(model.graph.edgelist).hexdigest() == hashlib.sha1(E).hexdigest()

	model.delete()
	G.delete()

def test_custom_model():
	A = np.array([0, 1], dtype = np.uint64).reshape(1, 2)
	G = px.create_graph(A)
	#G = px.create_graph(GraphType.chain, nodes=2)

	a1 = np.array([0.5, 0.6, 0.6, -0.3], dtype = px.np_type)
	a2 = np.array([0.1, 0.1, -1.0], dtype = px.np_type)

	m1 = px.Model(a1, G, states = 2, stats = StatisticsType.overcomplete) # overcomplete is the default
	m2 = px.Model(a2, G, states = 2, stats = StatisticsType.minimal)

	P1, A1 = m1.infer()
	P2, A2 = m2.infer()

	assert px.KL(P1, P2) < 0.000001

	m1.delete()
	m2.delete()
	G.delete()

def test_observations():
	model = px.load_model(px.example_model_filename)
	model.tree = False

	px.set_seed(1337)
	X = model.MAP

	X[0][int(784/2):] = px.MISSING_VALUE
	A = model.sample(sampler=SamplerType.apx_perturb_and_map, observed=X, perturbation=2)
	X[0][int(784/2):] = px.MISSING_VALUE
	B = model.sample(sampler=SamplerType.gibbs, observed=X)

	assert hashlib.sha1(A).hexdigest() == "0fceac37247e1f1bf86756a166302d968c324213"
	assert hashlib.sha1(B).hexdigest() == "989999d608a91e5cd773759bb93fd5207c137cdf"

	X[0][int(784/2):] = px.MISSING_VALUE
	P, _ = model.infer(observed=X)
	Q, _ = model.infer()

	assert abs(np.sum(Q) - (model.graph.edges + model.graph.nodes)) < 0.00001
	assert abs(np.sum(P) - (model.graph.edges + model.graph.nodes)) < 0.00001

	model.graph.delete()
	model.delete()

def test_vertex_marginals():
	model = px.load_model(px.example_model_filename)
	model.tree = False

	model.infer()

	assert abs(model.prob(300,0) - 0.84414402991237100) < 0.00001
	assert abs(model.prob(300,1) - 0.15585597008762903) < 0.00001

	model.graph.delete()
	model.delete()

def test_edge_marginals():
	model = px.load_model(px.example_model_filename)
	model.tree = False

	P, _ = model.infer()

	ii = np.where(model.graph.edgelist == 300)
	e = ii[0][0]
	Q = model.slice_edge(e,P)

	s = model.graph.edgelist[e][0]
	t = model.graph.edgelist[e][1]

	assert Q[0] == model.prob(s,0,t,0)
	assert model.prob(300,0,500,1) == model.prob(300,0) * model.prob(500,1)

	model.graph.delete()
	model.delete()

	#TODO: test a non-independent joint marginal explicitly! (value)

def test_resume_training():
	D = np.genfromtxt(px.example_data_filename, delimiter=',', skip_header=1, dtype=np.uint16)
	m1 = px.train(data=D, iters=10, initial_stepsize=0.00001, graph=GraphType.chain, mode=ModelType.mrf, zero_init=True, optimizer=Optimizer.gradient_descent)
	m2 = px.train(data=D, iters=10, initial_stepsize=0.00001, optimizer=Optimizer.gradient_descent, input_model=m1, mode=ModelType.mrf)
	m3 = px.train(data=D, iters=20, initial_stepsize=0.00001, graph=GraphType.chain, mode=ModelType.mrf, optimizer=Optimizer.gradient_descent, zero_init=True)

	assert hashlib.sha1(m1.weights).hexdigest() == hashlib.sha1(m3.weights).hexdigest()
