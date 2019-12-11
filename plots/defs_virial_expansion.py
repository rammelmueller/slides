"""-----------------------------------------------------------------------------

	defs_virial_expansion.py - LR, June 2018

-----------------------------------------------------------------------------"""
import numpy as np
from defs_noninteracting import n0
from functools import reduce
import collections
from scipy.integrate import quad


# Virial coefficients.
b2 = 1./np.sqrt(2.)
b3 = -0.3551


def _Q1(beta, nx, dim=3):

    # Momentum axis [-nx/2, nx/2])
    k = (np.arange(nx) - int(nx/2)) * 2.*np.pi/nx

    # Span the d-dimensional grid.
    k_mesh = np.meshgrid(*([k]*dim))

    # All squared values in a flat list.
    k_squ = reduce(lambda x, y: x + y, map(lambda x: x**2, k_mesh)).flatten()

    # Sum everything and return.
    return 2*sum(np.exp(-beta*k_squ/2.))


def ve_density(mu, h, beta, nx, order=3, norm=None):
    """ Virial expansion for the particle density of a single species, unnormalized.
    """
    zu, zd = np.exp(beta*(mu+h)), np.exp(beta*(mu-h))
    nu = n0(mu+h, beta, nx, dim=3)
    nd = n0(mu-h, beta, nx, dim=3)

    q1 = _Q1(beta, nx) / nx**3
    
    # First order contribution: non-interacting values.
    n_ve = nu + nd    
    
    # Add contributions order-by-order.
    if order >= 2:
        n_ve += q1 * b2 * 2*zu*zd
    
    if order >= 3:
        n_ve += q1 * b3 * 1.5*(zu**2*zd + zu*zd**2)
    
    # There's an end to everything.
    if order > 3 or order < 1:
        raise NotImplementedError('Order of virial expansion unknown.')

    if norm is None:
        return n_ve
    if norm == 'mean':
        return n_ve / (2*n0(mu, beta, nx, dim=3))
    if norm == 'pol':
        return n_ve / (nu + nd)
    


def ve_magnetization(mu, h, beta, nx, order=3, norm=None):
    """ Virial expansion for the particle density of a single species, unnormalized.
    """
    zu, zd = np.exp(beta*(mu+h)), np.exp(beta*(mu-h))
    nu = n0(mu+h, beta, nx, dim=3)
    nd = n0(mu-h, beta, nx, dim=3)

    q1 = _Q1(beta, nx) / nx**3

    # First order: non-interacting values.
    m_ve = nu - nd

    # Add contribution order by order, starting at n=3 since there is no second order
    # for the magnetization.
    if order >= 3:
        m_ve += q1*b3*(zu**2*zd - zu*zd**2)
    
    if order > 3 or order < 1:
        raise NotImplementedError('Order of virial expansion unkown.')

    if norm is None:
        return m_ve
    if norm == 'mean':
        return m_ve / (2*n0(mu, beta, nx, dim=3))
    if norm == 'pol':
        return m_ve / (nu + nd)

    
    
_vechi_kernel_3D = lambda t, mu, beta: np.sqrt(t)*np.exp(beta*mu - t)/(1+np.exp(beta*mu - t))**2
def ve_chi_m(mu, beta, dim=3):
    """ Virial expansion for the magnetic susceptibility.
        Taken from page 62 of [1]
        
        [1] Liu, Phys. Rep. 524:37-83, 2013.
    """
    if dim == 3:
        if isinstance(mu, collections.Iterable):
            res = np.zeros(shape=(len(mu)))        
            for i in range(len(mu)):
                res[i] = 2*beta/np.sqrt(2*np.pi*beta)**3 * (2./np.sqrt(np.pi)*quad(_vechi_kernel_3D, 0, np.inf, args=(mu[i], beta))[0] + np.exp(beta*mu[i])**3 * b3)
            return res
                           
        else:
            return 2*beta/np.sqrt(2*np.pi*beta)**3 * (2./np.sqrt(np.pi)*quad(_vechi_kernel_3D, 0, np.inf, args=(mu, beta))[0] + np.exp(beta*mu)**3 * b3)
                           
    raise NotImplementedError('Dimension not done (yet)!')