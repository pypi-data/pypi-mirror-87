"""
Collection of scientific constants

Notes
----------
Can easily be expanded by using https://docs.scipy.org/doc/scipy/reference/constants.html .
Those are just ones that I used more often while developing.
"""
import scipy.constants as con
from error_analysis.evar import *


# TODO add option for including errors where appropriate
c = evar(con.c, name="c")
""" Speed of light """
mu_0 = evar(con.mu_0, name=r"\mu_{0}")
""" Vacuum permeability """
epsilon_0 = evar(con.epsilon_0, name=r"\epsilon_{0}")
""" Vacuum permittivity """
k_B = evar(con.k, name="k_{B}")
""" Boltzmann constant """
e = evar(con.e, name="e")
""" Elementary charge """
N_A = evar(con.N_A, name="N_{A}")
""" Avogadro constant"""
u = evar(1.66054 * 10 ** -27, name="u")
""" 1 atomic mass unit"""
pi = evar(np.pi, name="\pi")
""" 1 atomic mass unit"""
