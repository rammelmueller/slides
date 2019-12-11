"""-----------------------------------------------------------------------------

	defs_noninteracting.py - LR, May 2018

-----------------------------------------------------------------------------"""
import numpy as np
from scipy.integrate import quad
from functools import reduce
import collections


lambda_t = lambda beta: np.sqrt(2*np.pi*beta)


def N0(mu, beta, nx, dim=3):
    """ Non-interacting particle number on the lattice for a *single* species.
        and a single datapoint (i.e. non-vectorized).
    """
    # Fugacity.
    z = np.exp(mu*beta)

    # Momentum axis [-nx/2, nx/2])
    k = (np.arange(nx) - int(nx/2)) * 2.*np.pi/nx

    # Span the d-dimensional grid.
    k_mesh = np.meshgrid(*([k]*dim))

    # All squared values in a flat list.
    k_squ = reduce(lambda x, y: x + y, map(lambda x: x**2, k_mesh)).flatten()

    # Sum everything and return.
    return sum(z*np.exp(-beta*k_squ/2.)/(z*np.exp(-beta*k_squ/2.) + 1.))


def n0(mu, beta, nx, dim=3):
    """ Particle density of a single species on the lattice, vecotrized for mu.
    """
    if isinstance(mu, collections.Iterable):
        return np.array(list(map(lambda x: N0(x, beta, nx, dim=dim), mu))) / nx**dim
    else:
        return N0(x, beta, nx, dim=dim) / nx**dim


def _n0_kernel_3D(k, z, beta):
    """ Momentum dependent integration kernel for the continuum density.
    """
    xk = np.exp(-beta*k**2/2)
    return 1./(2*np.pi**2) * k**2*xk*z/(1+xk*z)


def n0_FT_continuum(mu, beta, dim=3):
    """ Non-interacting density at finite temperature in the continuum for a *single* species. Can
        be caled with mu as an array.
    """
    if dim == 3:
        if isinstance(mu, collections.Iterable):
            res = np.zeros(shape=(len(mu)))
            for i in range(len(mu)):
                res[i] = quad(_n0_kernel_3D, 0, np.inf, args=(np.exp(beta*mu[i]), beta))[0]
            return res
        return quad(_n0_kernel_3D, 0, np.inf, args=(np.exp(beta*mu), beta))[0]
                           
    raise NotImplementedError('Dimension not done (yet)!')
                           
  

# Momentum dependent integration kernel for the 3D magnetization.
_m0_kernel_3D = lambda k, mu, h, beta: _n0_kernel_3D(k, np.exp((mu+h)*beta), beta) - _n0_kernel_3D(k, np.exp((mu-h)*beta), beta)
            
    
def m0_FT_continuum(mu, h, beta, dim=3):
    """ Non-interacting magnetization at finite temperature in the continuum. Can be called with
        mu and/or h as an array.
    """
    if dim == 3:
        if isinstance(mu, collections.Iterable) and isinstance(h, collections.Iterable):
            res = np.zeros(shape=(len(mu),len(h)))
            for i in range(len(mu)):
                for j in range(len(h)):
                    res[i,j] = quad(_m0_kernel_3D, 0, np.inf, args=(mu[i], h[j], beta))[0]
            return res
        
        if isinstance(mu, collections.Iterable):
            res = np.zeros(shape=(len(mu)))        
            for i in range(len(mu)):
                res[i] = quad(_m0_kernel_3D, 0, np.inf, args=(mu[i], h, beta))[0]
            return res
                           
        elif isinstance(h, collections.Iterable):
            res = np.zeros(shape=(len(h)))
            for j in range(len(h)):
                res[j] = quad(_m0_kernel_3D, 0, np.inf, args=(mu, h[j], beta))[0]
            return res
                           
        else:
            return quad(_m0_kernel_3D, 0, np.inf, args=(mu, h, beta))[0]
                           
    raise NotImplementedError('Dimension not done (yet)!')

    

def _chi0_kernel_3D(k, mu, h, beta):
    """ Momentum dependent integration kernel for the continuum density.
    """
    z = np.exp(beta*mu)
    xk = np.exp(-beta*k**2/2)
    return 4*np.pi*k**2 * (2*xk*np.cosh(beta*h)*(1+xk**2*z**2) + 4*xk**2*z**2) / (1 + xk**2*z**2 + 2*xk*np.cosh(beta*h))**2


def chi0_FT_continuum(mu, h, beta, dim=3):
    """ Non-interacting magnetization at finite temperature in the continuum. Can be called with
        mu and/or h as an array.
    """
    if dim == 3:
        if isinstance(mu, collections.Iterable) and isinstance(h, collections.Iterable):
            res = np.zeros(shape=(len(mu),len(h)))
            for i in range(len(mu)):
                for j in range(len(h)):
                    res[i,j] = quad(_chi0_kernel_3D, 0, np.inf, args=(mu[i], h[j], beta))[0]
            return res
        
        if isinstance(mu, collections.Iterable):
            res = np.zeros(shape=(len(mu)))        
            for i in range(len(mu)):
                res[i] = quad(_chi0_kernel_3D, 0, np.inf, args=(mu[i], h, beta))[0]
            return res
                           
        elif isinstance(h, collections.Iterable):
            res = np.zeros(shape=(len(h)))
            for j in range(len(h)):
                res[j] = quad(_chi0_kernel_3D, 0, np.inf, args=(mu, h[j], beta))[0]
            return res
                           
        else:
            return quad(_chi0_kernel_3D, 0, np.inf, args=(mu, h, beta))[0]
                           
    raise NotImplementedError('Dimension not done (yet)!')


def eF_GS(n, dim=3):
    """ Takes the density and returns the *ground-state* Fermi energy..
    """
    if dim == 3:
        return 0.5*(3*np.pi**2*n)**(2./3.)
    raise NotImplementedError('Dimension not done (yet)!')


def kappa0_GS(n, dim=3):
    if dim == 3:
        return 1.5 / (n*eF_GS(n, dim))
    raise NotImplementedError('Dimension not done (yet)!')


def p0_GS(n, dim=3):
    if dim == 3:
        return 0.4*n*eF_GS(n, dim)
    raise NotImplementedError('Dimension not done (yet)!')
    
    
def chi_pauli(n, beta=np.inf):
    """ Calculates the temperature-dependent Pauli susceptibility. If beta is np.inf (default) the GS
        value is returned.
    """
    return 1.5 * n / (eF_GS(n)) * (1 - np.pi**2/12. * (1./(beta*eF_GS(n)))**2) 

def chi0_GS(n):
    """ Returns the magnetic susceptibility of a non-interacting Fermi gas at zero temperature.
    """
    return kF(n)/(np.pi**2)
    

def kF(n):
    """ Returns the Fermi wavenumber for a given density.
    """
    return (3*np.pi**2*n)**(1./3)

def N0_cloryx(mu, beta, nx, dim=3):
    """ Noninteracting density on the lattice for a single species.
        This is the version that is implemented in CLOryx, the summation is wrong, a bug
        that will be most pronounced at small volumes but will go away at (very) large ones.
        
        IMPORTANT: used solely to re-normalize, should never be used again!
    """
    z = np.exp(mu*beta)
    n0 = 0.

    if dim == 2:
        for i in range(1,nx+1):
            for j in range(1,nx+1):
                ee  = 0.5 * (2*np.pi*(i-nx/2.)/nx)**2
                ee += 0.5 * (2*np.pi*(j-nx/2.)/nx)**2
                n0 += z*np.exp(-beta*ee)/(1. + z*np.exp(-beta*ee))

    if dim == 3:
        for i in range(1,nx+1):
            for j in range(1,nx+1):
                for k in range(1,nx+1):
                    ee  = 0.5 * (2*np.pi*(i-nx/2.)/nx)**2
                    ee += 0.5 * (2*np.pi*(j-nx/2.)/nx)**2
                    ee += 0.5 * (2*np.pi*(k-nx/2.)/nx)**2
                    n0 += z*np.exp(-beta*ee)/(1. + z*np.exp(-beta*ee))
    return n0

