# License: MIT
#
# Adopted from Steven Van Vaerenbergh's MATLAB Package 'KMBOX'
# https://github.com/steven2358/kmbox

from .base import BaseEmbed
from ..utils.utils import check_Xs

import numpy as np
import numpy.matlib
from scipy import linalg
from scipy.stats import f, chi2
from sklearn.metrics.pairwise import euclidean_distances


class KCCA(BaseEmbed):
    r"""
    The kernel canonical correlation analysis (KCCA) is a method
    that generalizes the classical linear canonical correlation
    analysis (CCA) to nonlinear setting.  It allows us to depict the
    nonlinear relation of two sets of variables and enables
    applications of classical multivariate data analysis
    originally constrained to linearity relation (CCA).

    If the linear kernel is used, this is equivalent to CCA.

    Parameters
    ----------
    n_components : int, default = 2
        Number of canonical dimensions to keep
    ktype : string, default = 'linear'
        Type of kernel. If 'linear', KCCA is equivalent to CCA.
        - value can be 'linear', 'gaussian' or 'poly'
    constant : float, default = 1.0
        Balances impact of lower-degree terms in Polynomial kernel
    sigma : float, default = 1.0
        Standard deviation of Gaussian kernel
    degree : float, default = 2.0
        Degree of Polynomial kernel
    reg : float, default = 0.1
        Regularization parameter
    decomp : string, default = 'full'
        Decomposition type. Incomplete Cholesky Decomposition (ICD)
        can reduce computation times and storage
        - value can be 'full' or 'icd'
    method : string, default = 'kettenring-like'
        Decomposition method
        - value can be only be 'kettenring-like'
    mrank : int, default = 2
        The rank of the ICD approximated kernel matrix
    precision: float, default = 0.000001
        Precision of computing the ICD kernel matrix

    Attributes
    ----------
    weights_ : list of array-likes
        Canonical weights for each view.

    Notes
    -----
    This class implements kernel canonical correlation analysis
    as described in [#1KCCA]_ and [#2KCCA]_.

    Traditional CCA aims to find useful projections of the
    high- dimensional variable sets onto the compact
    linear representations, the canonical components (components_).

    Each resulting canonical variate is computed from
    the weighted sum of every original variable indicated
    by the canonical weights (weights_).

    The canonical correlation quantifies the linear
    correspondence between the two views of data
    based on Pearson’s correlation between their
    canonical components.

    Canonical correlation can be seen as a metric of
    successful joint information reduction between two views
    and, therefore, routinely serves as a performance measure for CCA.

    CCA may not extract useful descriptors of the data because of
    its linearity. kCCA offers an alternative solution by first
    projecting the data onto a higher dimensional feature space.

    .. math::
        \phi: \mathbf{x} = (x_1,...,x_m) \mapsto
        \phi(\mathbf{x}) = (\phi(x_1),...,\phi(x_N)),
        (m < N)

    before performing CCA in the new feature space.

    Kernels are methods of implicitly mapping data into a higher
    dimensional feature space, a method known as the kernel trick.
    A kernel function K, such that for all :math:`\mathbf{x},
    \mathbf{z} \in X`,

    .. math::
        K(\mathbf{x}, \mathbf{z}) = \langle\phi(\mathbf{x})
        \cdot \phi(\mathbf{z})\rangle,

    where :math:`\phi` is a mapping from X to feature space F.

    The directions :math:`\mathbf{w_x}` and :math:`\mathbf{w_y}`
    (of length N) can be rewritten as the projection of the data
    onto the direction :math:`\alpha` and :math:`\beta`
    (of length m):

    .. math::
        \mathbf{w_x} = X'\alpha

    .. math::
        \mathbf{w_y} = Y'\beta

    Letting :math:`K_x = XX'` and :math:`K_x = XX'` be the kernel
    matrices and adding a regularization term (:math:`\kappa`)
    to prevent overfitting, we are effectively solving for:

    .. math::
        \rho = \underset{\alpha,\beta}{\text{max}}
        \frac{\alpha'K_xK_y\beta}
        {\sqrt{(\alpha'K_x^2\alpha+\kappa\alpha'K_x\alpha)
        \cdot (\beta'K_y^2\beta + \kappa\beta'K_y\beta)}}

    Kernel matrices grow exponentially with the size of data. They not only
    have to store :math:`n^2` elements, but also face the complexity of matrix
    eigenvalue problems. In a Cholesky decomposition a positive definite
    matrix A is decomposed to a lower triangular matrix :math:`L` :
    :math:`A = LL'`.

    The Incomplete Cholesky Decomposition (ICD) looks for a low rank
    approximation of :math:`L` to reduce the cost of operations of the matrix
    such that :math:`A $\approx$ $\tilde{L}$$\tilde{L}$'`. The algorithm skips
    a column if its diagonal element is small. The diagonal elements to the
    right of the column being updated are also updated. To select a column to
    update, it finds the largest diagonal element and pivots the element to
    the current diagonal by exchanging the corresponding rows and columns. The
    algorithm ends when all diagonal elemnts are below a specified accuracy.

    ICD with rank :math:`m` yields storage requirements of :math:`O(mn)`
    instead of :math:`O(n^2)` and becomes :math:`O(nm^2)` instead of
    :math:`O(n^3)` [#3KCCA]_. Unlike full decomposition, ICD cannot be
    performed out of sample i.e you must fit and transform on the same data.

    References
    ----------
    .. [#1KCCA] D. R. Hardoon, S. Szedmak and J. Shawe-Taylor,
            "Canonical Correlation Analysis: An Overview with
            Application to Learning Methods", Neural Computation,
            Volume 16 (12), Pages 2639--2664, 2004.
    .. [#2KCCA] J. R. Kettenring, “Canonical analysis of several sets of
            variables,”Biometrika, vol.58, no.3, pp.433–451,1971.
    .. [#3KCCA] M. I. Jordan, "Regularizing KCCA, Cholesky Decomposition",
            Lecture 9 Notes: CS281B/Stat241B, University of California,
            Berkeley.


    Examples
    --------
    >>> import numpy as np
    >>> from mvlearn.embed.kcca import KCCA
    >>> np.random.seed(1)
    >>> # Define two latent variables
    >>> N = 100
    >>> latvar1 = np.random.randn(N, )
    >>> latvar2 = np.random.randn(N, )
    >>> # Define independent components for each dataset
    >>> indep1 = np.random.randn(N, 3)
    >>> indep2 = np.random.randn(N, 4)
    >>> x = 0.25*indep1 + 0.75*np.vstack((latvar1, latvar2, latvar1)).T
    >>> y = 0.25*indep2 + 0.75*np.vstack((latvar1, latvar2,
    ...                                   latvar1, latvar2)).T
    >>> Xs = [x, y]
    >>> Xs_train = [Xs[0][:80], Xs[1][:80]]
    >>> Xs_test = [Xs[0][80:], Xs[1][80:]]
    >>> kcca = KCCA(ktype ="linear", n_components = 3,  reg = 0.01)
    >>> kcca.fit(Xs_train)
    >>> linear_transform = kcca.transform(Xs_test)
    >>> stats = kcca.get_stats()
    >>> # Print the correlations of first 3 transformed variates
    >>> # from the testing data
    >>> print(stats['r'])
    [0.85363047 0.91171037 0.06029391]

    """

    def __init__(
        self,
        n_components=2,
        ktype='linear',
        constant=0.1,
        sigma=1.0,
        degree=2.0,
        reg=0.1,
        decomp='full',
        method='kettenring-like',
        mrank=2,
        precision=0.000001
    ):
        self.n_components = n_components
        self.ktype = ktype
        self.constant = constant
        self.sigma = sigma
        self.degree = degree
        self.reg = reg
        self.decomp = decomp
        self.method = method
        self.mrank = mrank
        self.precision = precision

        # Error Handling
        if self.n_components < 0 or not type(self.n_components) == int:
            raise ValueError("n_components must be a positive integer")
        if ((self.ktype != "linear") and (self.ktype != "poly")
                and (self.ktype != "gaussian")):
            raise ValueError("ktype must be 'linear', 'gaussian', or 'poly'.")
        if self.sigma < 0 or not (type(self.sigma) == float
                                  or type(self.sigma) == int):
            raise ValueError("sigma must be positive int/float")
        if not (type(self.degree) == float or type(self.sigma) == int):
            raise ValueError("degree must be int/float")
        if self.reg < 0 or self.reg > 1 or not type(self.reg) == float:
            raise ValueError("reg must be positive float")
        if self.constant < 0 or not (type(self.constant) == float
                                     or type(self.constant) == int):
            raise ValueError("constant must be a positive integer")
        if self.decomp == "icd":
            if self.mrank < 0 or not (type(self.mrank) == int):
                raise ValueError("mrank must be a positive integer")
            if self.precision < 0 or not type(self.precision) == float:
                raise ValueError("precision must be a positive float")
        if not self.method == "kettenring-like":
            raise ValueError("method must be 'kettenring-like'")

    def fit(self, Xs, y=None):
        r"""
        Creates kcca mapping by determining
        canonical weghts from Xs.

        Parameters
        ----------
        Xs : list of array-likes or numpy.ndarray
             - Xs length: n_views
             - Xs[i] shape: (n_samples, n_features_i)
            The data for kcca to fit to.
            Each sample will receive its own embedding.

        y : ignored
            Included for API compliance.

        Returns
        -------
        self : returns an instance of self

        """
        Xs = check_Xs(Xs, multiview=True)

        self.X = _center_norm(Xs[0])
        self.Y = _center_norm(Xs[1])

        N = len(self.X)

        if self.decomp == "full":
            N1 = N
            Nl = len(self.X)
            Nr = len(self.Y)
            N0l = np.eye(Nl) - 1 / Nl * np.ones(Nl)
            N0r = np.eye(Nr) - 1 / Nr * np.ones(Nr)

            # Compute kernel matrices
            Kx = _make_kernel(self.X, self.X, self.ktype, self.constant,
                              self.degree, self.sigma)
            Ky = _make_kernel(self.Y, self.Y, self.ktype, self.constant,
                              self.degree, self.sigma)
            Kx = N0l @ Kx @ N0r
            Ky = N0l @ Ky @ N0r

            Id = np.eye(N)
            Z = np.zeros((N, N))

            # Method: Kettenring-like generalizable formulation
            if self.method == "kettenring-like":
                R = 0.5*np.r_[np.c_[Kx, Ky], np.c_[Kx, Ky]]
                D = np.r_[np.c_[Kx+self.reg*Id, Z], np.c_[Z, Ky+self.reg*Id]]

        elif self.decomp == "icd":

            # Compute the ICD kernel matrices
            G1 = _make_icd_kernel(self.X, self.ktype, self.constant,
                                  self.degree, self.sigma, self.mrank)

            G2 = _make_icd_kernel(self.Y, self.ktype, self.constant,
                                  self.degree, self.sigma, self.mrank)

            # Remove mean
            G1 = G1 - numpy.matlib.repmat(np.mean(G1, axis=0), N, 1)
            G2 = G2 - numpy.matlib.repmat(np.mean(G2, axis=0), N, 1)

            # Ones and Zeros
            N1 = len(G1[0])
            N2 = len(G2[0])
            Z12 = np.zeros((N1, N2))
            I11 = np.eye(N1)
            I22 = np.eye(N2)

            minrank = min(N1, N2)
            self.n_components = min(minrank, self.n_components)

            # Method: Kettenring-like generalizable formulation
            if self.method == "kettenring-like":
                R = 0.5*np.r_[np.c_[G1.T@G1, G1.T@G2],
                              np.c_[G2.T@G1, G2.T@G2]]
                D = np.r_[np.c_[G1.T@G1+self.reg*I11, Z12],
                          np.c_[Z12.T, G2.T@G2+self.reg*I22]]

        # Solve eigenvalue problem
        betas, alphas = linalg.eig(R, D)

        # Top eigenvalues
        ind = np.argsort(betas)[::-1][:self.n_components]

        # Extract relevant coordinates and normalize to unit length
        weight1 = alphas[:N1, ind]
        weight2 = alphas[N1:, ind]

        weight1 /= np.linalg.norm(weight1, axis=0)
        weight2 /= np.linalg.norm(weight2, axis=0)

        self.weights_ = np.real([weight1, weight2])

        return self

    def transform(self, Xs):
        r"""
        Uses KCCA weights to transform Xs into canonical components
        and calculates correlations.

        Parameters
        ----------
        Xs : list of array-likes or numpy.ndarray
             - Xs length: 2
             - Xs[i] shape: (n_samples, n_features_i)
            The data for kcca to fit to.
            Each sample will receive its own embedding.

        Returns
        -------
        components_ : returns Xs_transformed, a list of numpy.ndarray
             - Xs length: 2
             - Xs[i] shape: (n_samples, n_samples)
        """

        if not hasattr(self, "weights_"):
            raise NameError("kCCA has not been trained.")

        Xs = check_Xs(Xs, multiview=True)

        self.matrix_ranks_ = [np.linalg.matrix_rank(Xs[i])
                              for i in range(len(Xs))]
        self.n_samples_ = Xs[0].shape[0]

        weight1 = self.weights_[0]
        weight2 = self.weights_[1]

        comp1 = []
        comp2 = []

        if self.decomp == "full":
            Kx_transform = _make_kernel(_center_norm(Xs[0]),
                                        _center_norm(self.X),
                                        self.ktype,
                                        self.constant,
                                        self.degree,
                                        self.sigma)
            Ky_transform = _make_kernel(_center_norm(Xs[1]),
                                        _center_norm(self.Y),
                                        self.ktype,
                                        self.constant,
                                        self.degree,
                                        self.sigma)

            for i in range(weight1.shape[1]):
                comp1.append(Kx_transform@weight1[:, i])
                comp2.append(Ky_transform@weight2[:, i])

        elif self.decomp == "icd":
            Kx_t_icd = _make_icd_kernel(_center_norm(Xs[0]),
                                        self.ktype,
                                        self.constant,
                                        self.degree,
                                        self.sigma,
                                        self.mrank,
                                        self.precision)
            Ky_t_icd = _make_icd_kernel(_center_norm(Xs[1]),
                                        self.ktype,
                                        self.constant,
                                        self.degree,
                                        self.sigma,
                                        self.mrank,
                                        self.precision)

            for i in range(weight1.shape[1]):
                comp1.append(Kx_t_icd@weight1[:, i])
                comp2.append(Ky_t_icd@weight2[:, i])

        comp1 = np.transpose(np.asarray(comp1))
        comp2 = np.transpose(np.asarray(comp2))

        self.components_ = [comp1, comp2]

        return self.components_

    def get_stats(self):
        r"""
        Compute relevant statistics for the KCCA model after fitting
        and transforming.

        Implementations of the statistics generally follow the code in
        the Matlab implementation of the function canoncorr.

        Note: most statistics are only available if the linear kernel is
        used and decomposition method is full,
        i.e. self.ktype=='linear' and self.decomp='full'.

        Parameters
        ----------

        Returns
        -------
        stats : dict
            Dict containing the statistics, with the following keys:

            - 'r' : numpy.ndarray of shape (n_components,)
                Canonical correlations of each component.
            - 'Wilks' : numpy.ndarray of shape (n_components,)
                Wilks' Lambda likelihood ratio statistic.
                Only available if self.ktype == 'linear'.
            - 'df1' : numpy.ndarray of shape (n_components,)
                Degrees of freedom for the chi-squared statistic, and
                the numerator degrees of freedom for the F statistic.
                Only available if self.ktype == 'linear'.
            - 'df2' : numpy.ndarray of shape (n_components,)
                Denominator degrees of freedom for the F statistic.
                Only available if self.ktype == 'linear'.
            - 'F' : numpy.ndarray of shape (n_components,)
                Rao's approximate F statistic for H_0(k).
                Only available if self.ktype == 'linear'.
            - 'pF' : numpy.ndarray of shape (n_components,)
                Right-tail significance level for stats['F'].
                Only available if self.ktype == 'linear'.
            - 'chisq' : numpy.ndarray of shape (n_components,)
                Bartlett's approximate chi-squared statistic for H_0(k)
                with Lawley's modification.
                Only available if self.ktype == 'linear'.
            - 'pChisq' : numpy.ndarray of shape (n_components,)
                Right-tail significance level for stats['chisq'].
                Only available if self.ktype == 'linear'.

        """
        if not hasattr(self, "weights_"):
            raise NameError("KCCA has not been trained or fitted. Call"
                            " .fit() and .transform() or .fit_transform()"
                            " before getting statistics.")
        if not hasattr(self, "components_"):
            raise NameError("KCCA has not been fitted. Call .fit()"
                            " and .transform() or .fit_transform() before"
                            " getting statistics.")

        stats = {}
        r = np.array([np.corrcoef(self.components_[0][:, i],
                                  self.components_[1][:, i])[0, 1]
                      for i in range(self.n_components)]).squeeze()
        stats['r'] = r

        # Compute stats that are only defined for linear CCA. These follow
        # the format and computation of the stats in Matlab's canoncorr
        # function
        if self.ktype == 'linear' and self.decomp == 'full':

            # Wilks' Lambda test statistic
            d = min([self.n_components, min(self.matrix_ranks_)])
            k = np.arange(d)
            rank1_k = self.matrix_ranks_[0] - k
            rank2_k = self.matrix_ranks_[1] - k
            if r.size > 1:
                nondegen = np.argwhere(r < 1 - 2 *
                                       np.finfo(float).eps).squeeze()
            elif r < 1 - 2 * np.finfo(float).eps:
                nondegen = np.array(0, dtype=int)
            else:
                nondegen = np.array([], dtype=int)

            log_lambda = np.NINF * np.ones(self.n_components,)

            if nondegen.size > 0:
                if r.size > 1:
                    log_lambda[nondegen] = np.cumsum(
                                            (np.log(1 - r[nondegen]**2))[::-1])
                    log_lambda[nondegen] = log_lambda[nondegen][::-1]
                else:
                    log_lambda[nondegen] = np.cumsum(
                                            (np.log(1 - r**2)))

            stats['Wilks'] = np.exp(log_lambda)

            # Rao's approximation to F distribution.
            # default value for cases where the exponent formula fails
            s = np.ones(d,)
            # cases where (d1k,d2k) not one of (1,2), (2,1), or (2,2)
            okCases = np.argwhere(rank1_k*rank2_k > 2).squeeze()
            snumer = rank1_k*rank1_k*rank2_k*rank2_k - 4
            sdenom = rank1_k*rank1_k + rank2_k*rank2_k - 5
            s[okCases] = np.sqrt(np.divide(snumer[okCases], sdenom[okCases]))

            # Degrees of freedom for null hypothesis H_0k
            stats['df1'] = rank1_k * rank2_k
            stats['df2'] = (self.n_samples_ - .5 * (self.matrix_ranks_[0] +
                            self.matrix_ranks_[1] + 3)) * s - (.5 *
                                                               rank1_k *
                                                               rank2_k) + 1

            # Rao's F statistic
            pow_lambda = stats['Wilks']**(1 / s)
            ratio = np.inf * np.ones(d,)
            ratio[nondegen] = ((1 - pow_lambda[nondegen]) /
                               pow_lambda[nondegen])
            stats['F'] = ratio * stats['df2'] / stats['df1']
            stats['pF'] = 1 - f.cdf(stats['F'], stats['df1'], stats['df2'])

            # Lawley's modification to Bartlett's chi-squared statistic
            if r.size == 1:
                r = np.array([r])
            stats['chisq'] = -(self.n_samples_ - k - .5 *
                               (self.matrix_ranks_[0] +
                                self.matrix_ranks_[1] + 3) +
                               np.cumsum(np.hstack((np.zeros(1,),
                                                    1 / r[:d-1]))**2)) *\
                log_lambda

            stats['pChisq'] = 1 - chi2.cdf(stats['chisq'], stats['df1'])

        return stats


def _center_norm(x):
    x = x - x.mean(0)
    return x


def _make_kernel(X, Y, ktype, constant=0.1, degree=2.0, sigma=1.0):
    # Linear kernel
    if ktype == "linear":
        return (X @ Y.T)

    # Polynomial kernel
    elif ktype == "poly":
        return (X @ Y.T + constant) ** degree

    # Gaussian kernel
    elif ktype == "gaussian":
        distmat = euclidean_distances(X, Y, squared=True)
        return np.exp(-distmat / (2 * sigma ** 2))

    # Linear diagonal kernel
    elif ktype == "linear-diag":
        return (X @ Y.T).diagonal()

    # Polynomial diagonal kernel
    elif ktype == "poly-diag":
        return ((X @ Y.T + constant) ** degree).diagonal()

    # Gaussian diagonal kernel
    elif ktype == "gaussian-diag":
        return np.exp(-np.sum(np.power((X-Y), 2), axis=1)/(2*sigma**2))


def _make_icd_kernel(X, ktype="linear", constant=0.1, degree=2.0, sigma=1.0,
                     mrank=2, precision=0.000001):
    N = len(X)
    mrank = min(mrank, N)

    perm = np.arange(N)  # Permutation vector
    d = np.zeros(N)  # Diagonal of the residual kernel matrix
    G = np.zeros((N, mrank))
    subset = np.zeros(mrank)

    for i in range(mrank):
        x_new = X[perm[i:N], :]
        if i == 0:
            # Diagonal of kernel matrix
            d[i:N] = _make_kernel(x_new, x_new, ktype + "-diag",
                                  constant, degree).T
        else:
            # Update diagonal of residual kernel matrix
            d[i:N] = (_make_kernel(x_new, x_new, ktype + "-diag",
                                   constant, degree).T -
                      np.sum(np.power(G[i:N, :i], 2), axis=1).T)

        dtrace = sum(d[i:N])
        if dtrace <= 0:
            print("Warning: negative diagonal entry")

        if dtrace <= precision:
            G = G[:, :i]
            subset = subset[:i]
            break

        # Find new best element
        j = np.argmax(d[i:N])
        m2 = np.max(d[i:N])
        j = j+i  # Take into account the offset i
        m1 = np.sqrt(m2)
        subset[i] = j

        perm[[i, j]] = perm[[j, i]]  # Permute elements i and j
        G[[i, j], :i] = G[[j, i], :i]  # Permute rows i and j
        G[i, i] = m1  # New diagonal elemtn

        # Calculate the ith columnn- introduces some numerical error
        z1 = _make_kernel([X[perm[i], :]], X[perm[i+1:N], :],
                          ktype, sigma)
        z2 = (G[i+1:N, :i]@(G[i, :i].T))
        G[i+1:N, i] = (z1 - z2)/m1
    return G[np.argsort(perm), :]
