import numpy as np


def eTL_bethe_strongAttractive(gamma, norm="efg"):
	"""	Strong coupling expansion for the ground-state energy of a Fermi gas in
		the thermodynamic limit (TL) normalized to E_FG in the continuum.

		Taken from Wadati/Iida [http://dx.doi.org/10.1016/j.physleta.2006.07.068].

		Attention: attractive coupling is positive.
	"""
	return -3*gamma**2./np.pi**2  +  (-gamma/(1.-2*gamma))**2 * (1 + 4*np.pi**2/(15*(1.-2*gamma)**3))


def eTL_bethe_weakCoupling(gamma):
	""" Weak coupling expansion for the ground-state energy of a Fermi gas in
		the thermodynamic limit (TL) normalized to E_FG in the continuum.

		Taken from Tracy/Widom [arXiv:1609.07793].

		Attention: attractive coupling is positive.
	"""
	return 1. - 6*gamma/np.pi**2 - gamma**2/np.pi**2
