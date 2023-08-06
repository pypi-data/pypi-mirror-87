"""Commonly used math tools.
"""


import numpy as np
import scipy as sp
import scipy.linalg as sla
import numpy.linalg as nla
import scipy.stats as ss

from scipy.linalg import svd
from numpy.linalg import eig
# eig() of scipy.linalg necessitates using np.real_if_close().
from scipy.linalg import sqrtm, inv, eigh

from numpy import \
    pi, nan, \
    log, log10, exp, sin, cos, tan, \
    sqrt, floor, ceil, \
    mean, prod, \
    diff, cumsum, \
    array, asarray, asmatrix, \
    linspace, arange, reshape, \
    eye, zeros, ones, diag, trace \
    # Don't shadow builtins: sum, max, abs, round, pow

np.set_printoptions(suppress=True,threshold=200,precision=6)
# Instead of set_np_linewidth, just let terminal do wrapping:
np.set_printoptions(linewidth=9999)


# NB: These are not equal to np.random.rand{,s},
#     which follow Matlab syntax.
# NB: Subject to change.
rand  = lambda shape: np.random.uniform(size=shape)
randn = np.random.standard_normal
