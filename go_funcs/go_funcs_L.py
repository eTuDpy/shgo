# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

from numpy import sum, cos, exp, pi, arange, sin
from .go_benchmark import Benchmark


class Langermann(Benchmark):

    r"""
    Langermann objective function.

    This class defines the Langermann [1]_ global optimization problem. This
    is a multimodal minimization problem defined as follows:

    .. math::

        f_{\text{Langermann}}(x) = - \sum_{i=1}^{5} 
        \frac{c_i \cos\left\{\pi \left[\left(x_{1}- a_i\right)^{2}
        + \left(x_{2} - b_i \right)^{2}\right]\right\}}{e^{\frac{\left( x_{1}
        - a_i\right)^{2} + \left( x_{2} - b_i\right)^{2}}{\pi}}}


    Where:

    .. math::

        \begin{matrix}
        a = [3, 5, 2, 1, 7]\\
        b = [5, 2, 1, 4, 9]\\
        c = [1, 2, 5, 2, 3] \\
        \end{matrix}


    Here :math:`x_i \in [0, 10]` for :math:`i = 1, 2`.

    *Global optimum*: :math:`f(x) = -5.1621259`
    for :math:`x = [2.00299219, 1.006096]`

    .. [1] Gavana, A. Global Optimization Benchmarks and AMPGO retrieved 2015

    TODO: Langermann from Gavana is _not the same_ as Jamil #68.
    """

    def __init__(self, dimensions=2):
        Benchmark.__init__(self, dimensions)

        self._bounds = list(zip([0.0] * self.N, [10.0] * self.N))

        self.global_optimum = [[2.00299219, 1.006096]]
        self.fglob = -5.1621259

    def fun(self, x, *args):
        self.nfev += 1

        a = [3, 5, 2, 1, 7]
        b = [5, 2, 1, 4, 9]
        c = [1, 2, 5, 2, 3]

        return (-sum(c * exp(-(1 / pi) * ((x[0] - a) ** 2 +
                    (x[1] - b) ** 2)) * cos(pi * ((x[0] - a) ** 2
                                            + (x[1] - b) ** 2))))


class LennardJones(Benchmark):

    r"""
    LennardJones objective function.

    This class defines the Lennard-Jones global optimization problem. This
    is a multimodal minimization problem defined as follows:

    .. math::

        f_{\text{LennardJones}}(\mathbf{x}) = \sum_{i=0}^{n-2}\sum_{j>1}^{n-1}
        \frac{1}{r_{ij}^{12}} - \frac{1}{r_{ij}^{6}}


    Where, in this exercise:

    .. math::

        r_{ij} = \sqrt{(x_{3i}-x_{3j})^2 + (x_{3i+1}-x_{3j+1})^2)
        + (x_{3i+2}-x_{3j+2})^2}


    Valid for any dimension, :math:`n = 3*k, k=2 , 3, 4, ..., 20`. :math:`k`
    is the number of atoms in 3-D space constraints: unconstrained type:
    multi-modal with one global minimum; non-separable

    Value-to-reach: :math:`minima[k-2] + 0.0001`. See array of minima below;
    additional minima available at the Cambridge cluster database:

    http://www-wales.ch.cam.ac.uk/~jon/structures/LJ/tables.150.html

    Here, :math:`n` represents the number of dimensions and
    :math:`x_i \in [-4, 4]` for :math:`i = 1 ,..., n`.

    *Global optimum*:

    .. math::

        \text{minima} = [-1.,-3.,-6.,-9.103852,-12.712062,-16.505384,\\
                         -19.821489, -24.113360, -28.422532,-32.765970,\\
                         -37.967600,-44.326801, -47.845157,-52.322627,\\
                         -56.815742,-61.317995, -66.530949, -72.659782,\\
                         -77.1777043]\\


    """

    def __init__(self, dimensions=6):
        # dimensions is in [6:60]
        # max dimensions is going to be 60.
        if dimensions not in range(6, 61):
            raise ValueError("LJ dimensions must be in (6, 60)")

        Benchmark.__init__(self, dimensions)

        self._bounds = list(zip([-4.0] * self.N, [4.0] * self.N))

        self.global_optimum = [[]]

        self.minima = [-1.0, -3.0, -6.0, -9.103852, -12.712062,
                       -16.505384, -19.821489, -24.113360, -28.422532,
                       -32.765970, -37.967600, -44.326801, -47.845157,
                       -52.322627, -56.815742, -61.317995, -66.530949,
                       -72.659782, -77.1777043]

        k = int(dimensions / 3)
        self.fglob = self.minima[k - 2]
        self.change_dimensionality = True

    def change_dimensions(self, ndim):
        if ndim not in range(6, 61):
            raise ValueError("LJ dimensions must be in (6, 60)")

        Benchmark.change_dimensions(self, ndim)
        self.fglob = self.minima[int(self.N / 3) - 2]

    def fun(self, x, *args):
        self.nfev += 1

        k = int(self.N / 3)
        s = 0.0

        for i in range(k - 1):
            for j in range(i + 1, k):
                a = 3 * i
                b = 3 * j
                xd = x[a] - x[b]
                yd = x[a + 1] - x[b + 1]
                zd = x[a + 2] - x[b + 2]
                ed = xd * xd + yd * yd + zd * zd
                ud = ed * ed * ed
                if ed > 0.0:
                    s += (1.0 / ud - 2.0) / ud

        return s

class LennardJonesN(Benchmark):

    r"""
    LennardJones objective function evaluated for a LennardJones cluster
    composed of P types of particles, namely A, B, ... Z.

    This class defines a Lennard-Jones global optimization problem. This
    is a multimodal minimization problem defined as follows:

    .. math::

        f_{\text{LennardJones}}(\mathbf{x}) = \sum_{i=0}^{n-2}\sum_{j>1}^{n-1}
        \epsilon_{ij}\frac{\sigma_{ij}}{r_{ij}^{12}} - \frac{\sigma_{ij}}{r_{ij}^{6}}


    Where, in this exercise:

    .. math::

        r_{ij} = \sqrt{(x_{3i}-x_{3j})^2 + (x_{3i+1}-x_{3j+1})^2)
        + (x_{3i+2}-x_{3j+2})^2}


    Valid for any dimension, :math:`n = 3 * \sum p_i, k_i = 1, 2, 3, ....`. :math:`p_i`
    is the number of particles of the p-th type.

    Value-to-reach: Should be given as an input for the system at hand

    *Global optimum*: Should be given as an input for the system at hand

    References:
    Chill, S.T., Stevenson, J., Ruehle, V., Shang, C.,  Xiao, P., Farrell, J.D., Wales, D.J., and Henkelman, G. (2014)
    "Benchmarks for Characterization of Minima, Transition States, and Pathways in Atomic, Molecular, and Condensed Matter Systems"
    J. Chem. Theory Comput., 2014, 10 (12), 5476–5482.
    """

    def __init__(self, p, fglob=None, global_optimum=[[]], epsilon=[[]], sigma=[[]], bounds = [()]):
        """Initialises Class
	
	Parameters
	----------
	p : [int]
		Array of the number of particles of each particle type.
        P = len(p)
    fglob : float
		value of the global minimum
	global_optimum : [[float]]
		List of x_lists, containing coordinates at which the
		objective function evaluates to fglob
	Either fglob or global_optimum must be specified. 
	elsilon : [[float]]
        A PxP 2D array of binary epsilon values between two types of particles.
        Please note that behaviour is not defined if the matrix is not symmetric.
        Takes the form:
		.. math::

        [   [\epsilon_{AA}, \epsilon_{AB} ... \epsilon_{AZ}]
            [\epsilon_{BA}, \epsilon_{BB} ... \epsilon_{BZ}]
            .
            .
            .
            [\epsilon_{ZA}, \epsilon_{ZB} ... \epsilon_{ZZ}]
        ]
        Defaults to all 1's.
	sigma : [[float]]
		A PxP 2D array of binary sigma values between two types of particles.
        Please note that behaviour is not defined if the matrix is not symmetric.
        Takes the form:
		.. math::

        [   [\sigma_{AA}, \sigma_{AB} ... \sigma_{AZ}]
            [\sigma_{BA}, \sigma_{BB} ... \sigma_{BZ}]
            .
            .
            .
            [\sigma_{ZA}, \sigma_{ZB} ... \sigma_{ZZ}]
        ]
        Defaults to all 1's.
	bounds : [(float, float)]
    List of bounds for each dimension. Defaults to all lower bounds = -10 and all upper bounds = 10.
	"""
        self.p = [int(p_i) for p_i in p]
        if 0 in p:
            raise ValueError("LJ must have at least one of each atom type specified")

        dimensions = 3 * sum(p)

        Benchmark.__init__(self, dimensions)

        if epsilon == [[]]:
            self.epsilon = [ [1 for i in range(len(p))] for j in range(len(p)) ]
        else:
            self.epsilon = epsilon

        if sigma == [[]]:
            self.sigma = [ [1 for i in range(len(p))] for j in range(len(p)) ]
        else:
            self.sigma = sigma 

        if bounds == [()]:
            self._bounds = list(zip([-10.0] * self.N, [10.0] * self.N))
        else:
            self._bounds = bounds

        if global_optimum != [[]]:
            self.global_optimum = global_optimum
            self.fglob = self.fun(global_optimum[0])
            if fglob !=None and abs(self.fglob - fglob) > 1e-5:
                raise ValueError("Global optimum does not correspond to supposed global minimum. {0} != {1}".format(self.fglob, fglob))
        elif fglob != None:
            self.fglob = fglob
        else:
            raise ValueError("Either fglob or global_optimim must be specified")
	
        self.change_dimensionality = False

    def fun(self, x, *args):
        """Objective function
	
	Parameters
	----------
	x : [float]
		Coordinates at which to evaluate objective function
		The values are semantically grouped into groups of three
		where each group represent the Euclidian coordinates of a
		particle. From the list p which has the form: [p_1, p_2 ... ]
        the first p_1 particles are of type 1, the next p_2 particles
        are of type 2, etc.

	Returns
	-------
	t : float
		Value of the LJ potential
	"""
        self.nfev += 1
        k = int(self.N / 3)
        t = 0.0
        ij = [count for p_i, count in zip(self.p,range(len(self.p))) for q in range(p_i)]
        for i, A in zip( range(k), ij ):
            for j,B in zip( range(k), ij ):
                if(i>=j):
                    continue

                a = 3 * i
                b = 3 * j
                xd = x[a] - x[b]
                yd = x[a + 1] - x[b + 1]
                zd = x[a + 2] - x[b + 2]
                r2 = xd**2 + yd**2 + zd**2
                e = self.epsilon[A][B]
                s = self.sigma[A][B]
                t +=  e * ( s**12 / r2**6 - s**6 / r2**3 ) 

        return 4 * t


class Leon(Benchmark):

    r"""
    Leon objective function.

    This class defines the Leon [1]_ global optimization problem. This
    is a multimodal minimization problem defined as follows:

    .. math::

        f_{\text{Leon}}(\mathbf{x}) = \left(1 - x_{1}\right)^{2} 
        + 100 \left(x_{2} - x_{1}^{2} \right)^{2}


    with :math:`x_i \in [-1.2, 1.2]` for :math:`i = 1, 2`.

    *Global optimum*: :math:`f(x) = 0` for :math:`x = [1, 1]`

    .. [1] Jamil, M. & Yang, X.-S. A Literature Survey of Benchmark Functions
    For Global Optimization Problems Int. Journal of Mathematical Modelling
    and Numerical Optimisation, 2013, 4, 150-194.
    """

    def __init__(self, dimensions=2):
        Benchmark.__init__(self, dimensions)

        self._bounds = list(zip([-1.2] * self.N, [1.2] * self.N))

        self.global_optimum = [[1 for _ in range(self.N)]]
        self.fglob = 0.0

    def fun(self, x, *args):
        self.nfev += 1

        return 100. * (x[1] - x[0] ** 2.0) ** 2.0 + (1 - x[0]) ** 2.0


class Levy03(Benchmark):

    r"""
    Levy 3 objective function.

    This class defines the Levy 3 [1]_ global optimization problem. This
    is a multimodal minimization problem defined as follows:

    .. math::

        f_{\text{Levy03}}(\mathbf{x}) = \sin^2(\pi y_1)+\sum_{i=1}^{n-1}(y_i-1)^2[1+10\sin^2(\pi y_{i+1})]+(y_n-1)^2

    Where, in this exercise:

    .. math::

        y_i=1+\frac{x_i-1}{4}


    Here, :math:`n` represents the number of dimensions and :math:`x_i \in [-10, 10]` for :math:`i=1,...,n`.

    *Global optimum*: :math:`f(x_i) = 0` for :math:`x_i = 1` for :math:`i=1,...,n`

    .. [1] Mishra, S. Global Optimization by Differential Evolution and
    Particle Swarm Methods: Evaluation on Some Benchmark Functions.
    Munich Personal RePEc Archive, 2006, 1005

    TODO: not clear what the Levy function definition is.  Gavana, Mishra,
    Adorio have different forms. Indeed Levy 3 docstring from Gavana
    disagrees with the Gavana code!  The following code is from the Mishra
    listing of Levy08.
    """

    def __init__(self, dimensions=2):
        Benchmark.__init__(self, dimensions)

        self._bounds = list(zip([-10.0] * self.N, [10.0] * self.N))
        self.custom_bounds = [(-5, 5), (-5, 5)]

        self.global_optimum = [[1 for _ in range(self.N)]]
        self.fglob = 0.0

    def fun(self, x, *args):
        self.nfev += 1

        y = 1 + (x - 1) / 4
        v = sum((y[:-1] - 1) ** 2 * (1 + 10 * sin(pi * y[1:]) ** 2))
        z = (y[-1] - 1) ** 2
        return sin(pi * y[0]) ** 2 + v + z


class Levy05(Benchmark):

    r"""
    Levy 5 objective function.

    This class defines the Levy 5 [1]_ global optimization problem. This
    is a multimodal minimization problem defined as follows:

    .. math::

        f_{\text{Levy05}}(\mathbf{x}) = \sum_{i=1}^{5} i \cos \left[(i-1)x_1 + i \right] \times \sum_{j=1}^{5} j \cos \left[(j+1)x_2 + j \right] + (x_1 + 1.42513)^2 + (x_2 + 0.80032)^2

    Here, :math:`n` represents the number of dimensions and :math:`x_i \in [-10, 10]` for :math:`i=1,...,n`.

    *Global optimum*: :math:`f(x_i) = -176.1375779` for :math:`\mathbf{x} = [-1.30685, -1.42485]`.

    .. [1] Mishra, S. Global Optimization by Differential Evolution and
    Particle Swarm Methods: Evaluation on Some Benchmark Functions.
    Munich Personal RePEc Archive, 2006, 1005
    """

    def __init__(self, dimensions=2):
        Benchmark.__init__(self, dimensions)

        self._bounds = list(zip([-10.0] * self.N, [10.0] * self.N))
        self.custom_bounds = ([-2.0, 2.0], [-2.0, 2.0])

        self.global_optimum = [[-1.30685, -1.42485]]
        self.fglob = -176.1375779

    def fun(self, x, *args):
        self.nfev += 1

        i = arange(1, 6)
        a = i * cos((i - 1) * x[0] + i)
        b = i * cos((i + 1) * x[1] + i)

        return sum(a) * sum(b) + (x[0] + 1.42513) ** 2 + (x[1] + 0.80032) ** 2


class Levy13(Benchmark):

    r"""
    Levy13 objective function.

    This class defines the Levy13 [1]_ global optimization problem. This is a
    multimodal minimization problem defined as follows:

    .. math::

        f_{\text{Levy13}}(x) = \left(x_{1} -1\right)^{2} \left[\sin^{2}
        \left(3 \pi x_{2}\right) + 1\right] + \left(x_{2} 
        - 1\right)^{2} \left[\sin^{2}\left(2 \pi x_{2}\right)
        + 1\right] + \sin^{2}\left(3 \pi x_{1}\right)


    with :math:`x_i \in [-10, 10]` for :math:`i = 1, 2`.

    *Global optimum*: :math:`f(x) = 0` for :math:`x = [1, 1]`

    .. [1] Mishra, S. Some new test functions for global optimization and
    performance of repulsive particle swarm method.
    Munich Personal RePEc Archive, 2006, 2718
    """

    def __init__(self, dimensions=2):
        Benchmark.__init__(self, dimensions)

        self._bounds = list(zip([-10.0] * self.N, [10.0] * self.N))
        self.custom_bounds = [(-5, 5), (-5, 5)]

        self.global_optimum = [[1 for _ in range(self.N)]]
        self.fglob = 0.0

    def fun(self, x, *args):
        self.nfev += 1

        u = sin(3 * pi * x[0]) ** 2
        v = (x[0] - 1) ** 2 * (1 + (sin(3 * pi * x[1])) ** 2)
        w = (x[1] - 1) ** 2 * (1 + (sin(2 * pi * x[1])) ** 2)
        return u + v + w
