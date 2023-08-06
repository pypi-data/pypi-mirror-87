# import numpy as np 
import autograd.numpy as np
import autograd.numpy.random as npr
from autograd.scipy.stats import multivariate_normal

def test_flows():
	from vi_families import RealNVP
	q = RealNVP(5, 16, 2, 0.1, 3)

	ϕ = q.initial_params()

	z = q.sample(ϕ, (4,2))
	lq = q.log_prob(ϕ, z)
	ε, _ = q.inverse_transform(ϕ, z)
	ζ, _ = q.forward_transform(ϕ, ε)

	results = {
		"z" : z,
		"ζ" : ζ,
		"ε" : ε,
		"lq" : lq,
		"δ" : np.linalg.norm((ζ - z))/np.linalg.norm(z),
	}

	[print(f"{k}: {v}") for k,v in results.items()];

def test_gaussian():

	from vi_families import Gaussian

	q = Gaussian(3)

	ϕ = q.initial_params()

	z = q.sample(ϕ, (4,2))
	lq = q.log_prob(ϕ, z)

	lg = multivariate_normal.logpdf(z, np.zeros(3), np.eye(3))
	# lg = g.pdf(z)

	results = {
		"z" : z,
		"lq" : lq,
		"lg" : lg,
		"δ" : np.linalg.norm((lq - lg))/np.linalg.norm(lq),
	}
	[print(f"{k}: {v}") for k,v in results.items()];

def test_diagonal():

	from vi_families import Diagonal

	q = Diagonal(3)

	ϕ = q.initial_params()
	z = q.sample(ϕ, (4,2))
	lq = q.log_prob(ϕ, z)

	lg = multivariate_normal.logpdf(z, np.zeros(3), np.eye(3))
	# lg = g.pdf(z)

	results = {
		"δ" : np.linalg.norm((lq - lg))/np.linalg.norm(lq),
		"δ_abs" : np.linalg.norm((lq - lg)),
	}
	[print(f"{k}: {v}") for k,v in results.items()];


# test_diagonal()
