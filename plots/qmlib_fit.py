import sys
import numpy as np
from scipy.optimize import curve_fit

DERIVATIVE_PRECISION = 0.00001

def confidenceBands(data, func, popt, pcov, cl=0.95):
    """    Calculates symmetric confidence bands for a fit with the DELTA METHOD.

            c(x) = (grad f |x)^T * COV * (grad f |x)
            d(x) = sqrt(c(x)) * z

        where z determines the confidence level, and COV the covariance matrix.
        d(x) determines half the width of the
        confidence band at a given position x.
        
        Returns upper and lower bands, as well as the standard deviation.
    """
    #FIXME Lazy, assuming normal distribution and 0.95
    z = 1.96
    if cl != 0.95:
        raise NotImplementedError("Currently not implemented, only a CI of 95% works.")

    x, y = zip(*data)
    x = np.array(x)
    y = np.array(y)
    
    npopt = np.array(popt)
    #fit = func(x, popt)
    fit = func(x, *popt)

    # Caluclate the gradients.
    shift = np.diag(np.zeros(len(popt)) + DERIVATIVE_PRECISION)
    c = []
    for xp in x:
        gradx = [(func(xp, *(npopt + h)) - func(xp, *(npopt - h))) / (2.*DERIVATIVE_PRECISION) for h in shift]
        c.append(np.dot(gradx, np.dot(pcov, gradx)))

    d = z*np.sqrt(np.array(c))
    return fit+d, fit-d, d/z