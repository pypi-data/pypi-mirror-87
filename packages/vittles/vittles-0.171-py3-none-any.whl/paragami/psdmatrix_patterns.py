from .base_patterns import Pattern

import autograd.numpy as np

import math

from autograd.core import primitive, defvjp, defjvp


def _sym_index(k1, k2):
    """
    Get the index of an entry in a folded symmetric array.

    Parameters
    ------------
    k1, k2: int
        0-based indices into a symmetric matrix.

    Returns
    --------
    int
        Return the linear index of the (k1, k2) element of a symmetric
        matrix where the triangular part has been stacked into a vector.
    """
    def ld_ind(k1, k2):
        return int(k2 + k1 * (k1 + 1) / 2)

    if k2 <= k1:
        return ld_ind(k1, k2)
    else:
        return ld_ind(k2, k1)


def _vectorize_ld_matrix(mat):
    """
    Linearize the lower diagonal of a square matrix.

    Parameters:
    mat
        A square matrix.

    Returns:
    1-d vector
        The lower diagonal of `mat` stacked into a vector.

    Specifically, we map the matrix

    [ x11 x12 ... x1n ]
    [ x21 x22     x2n ]
    [...              ]
    [ xn1 ...     xnn ]

    to the vector

    [ x11, x21, x22, x31, ..., xnn ].

    The entries above the diagonal are ignored.
    """
    nrow, ncol = np.shape(mat)
    if nrow != ncol:
        raise ValueError('mat must be square')
    return mat[np.tril_indices(nrow)]


@primitive
def _unvectorize_ld_matrix(vec):
    """
    Invert the mapping of `_vectorize_ld_matrix`.

    Parameters
    -----------
    vec: A 1-d vector.

    Returns
    ----------
    A symmetric matrix.

    Specifically, we map a vector

    [ v1, v2, ..., vn ]

    to the symmetric matrix

    [ v1 ...          ]
    [ v2 v3 ...       ]
    [ v4 v5 v6 ...    ]
    [ ...             ]

    where the values above the diagonal are determined by symmetry.
    """
    mat_size = int(0.5 * (math.sqrt(1 + 8 * vec.size) - 1))
    if mat_size * (mat_size + 1) / 2 != vec.size:
        raise ValueError('Vector is an impossible size')
    mat = np.zeros((mat_size, mat_size))
    for k1 in range(mat_size):
        for k2 in range(k1 + 1):
            mat[k1, k2] = vec[_sym_index(k1, k2)]
    return mat

# Because we cannot use autograd with array assignment, define the
# vector jacobian product and jacobian vector products of
# _unvectorize_ld_matrix.


def _unvectorize_ld_matrix_vjp(g):
    assert g.shape[0] == g.shape[1]
    return _vectorize_ld_matrix(g)


defvjp(_unvectorize_ld_matrix,
       lambda ans, vec: lambda g: _unvectorize_ld_matrix_vjp(g))


def _unvectorize_ld_matrix_jvp(g):
    return _unvectorize_ld_matrix(g)


defjvp(_unvectorize_ld_matrix,
       lambda g, ans, x: _unvectorize_ld_matrix_jvp(g))


def _exp_matrix_diagonal(mat):
    assert mat.shape[0] == mat.shape[1]
    # NB: make_diagonal() is only defined in the autograd version of numpy
    mat_exp_diag = np.make_diagonal(
        np.exp(np.diag(mat)), offset=0, axis1=-1, axis2=-2)
    mat_diag = np.make_diagonal(np.diag(mat), offset=0, axis1=-1, axis2=-2)
    return mat_exp_diag + mat - mat_diag


def _log_matrix_diagonal(mat):
    assert mat.shape[0] == mat.shape[1]
    # NB: make_diagonal() is only defined in the autograd version of numpy
    mat_log_diag = np.make_diagonal(
        np.log(np.diag(mat)), offset=0, axis1=-1, axis2=-2)
    mat_diag = np.make_diagonal(np.diag(mat), offset=0, axis1=-1, axis2=-2)
    return mat_log_diag + mat - mat_diag


def _pack_posdef_matrix(mat, diag_lb=0.0):
    k = mat.shape[0]
    mat_lb = mat - np.make_diagonal(
        np.full(k, diag_lb), offset=0, axis1=-1, axis2=-2)
    return _vectorize_ld_matrix(
        _log_matrix_diagonal(np.linalg.cholesky(mat_lb)))


def _unpack_posdef_matrix(free_vec, diag_lb=0.0):
    mat_chol = _exp_matrix_diagonal(_unvectorize_ld_matrix(free_vec))
    mat = np.matmul(mat_chol, mat_chol.T)
    k = mat.shape[0]
    return mat + np.make_diagonal(
        np.full(k, diag_lb), offset=0, axis1=-1, axis2=-2)


# Convert a vector containing the lower diagonal portion of a symmetric
# matrix into the full symmetric matrix.
def _unvectorize_symmetric_matrix(vec_val):
    ld_mat = _unvectorize_ld_matrix(vec_val)
    mat_val = ld_mat + ld_mat.transpose()
    # We have double counted the diagonal.  For some reason the autograd
    # diagonal functions require axis1=-1 and axis2=-2
    mat_val = mat_val - \
        np.make_diagonal(np.diagonal(ld_mat, axis1=-1, axis2=-2),
                         axis1=-1, axis2=-2)
    return mat_val


class PSDSymmetricMatrixPattern(Pattern):
    """
    A pattern for a symmetric, positive-definite matrix parameter.

    Attributes
    -------------
    validate: Bool
        Whether or not the matrix is automatically checked for symmetry
        positive-definiteness, and the diagonal lower bound.
    """
    def __init__(self, size, diag_lb=0.0, default_validate=True):
        """
        Parameters
        --------------
        size: int
            The length of one side of the square matrix.
        diag_lb: float
            A lower bound for the diagonal entries.  Must be >= 0.
        default_validate: bool
            Whether or not to check for legal (i.e., symmetric
            positive-definite) folded values by default.
        """
        self.__size = int(size)
        self.__diag_lb = diag_lb
        self.default_validate = default_validate
        if diag_lb < 0:
            raise ValueError(
                'The diagonal lower bound diag_lb must be >-= 0.')

        super().__init__(self.__size ** 2, int(size * (size + 1) / 2))

    def __str__(self):
        return 'PDMatrix {}x{} (diag_lb = {})'.format(
            self.__size, self.__size, self.__diag_lb)

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return \
            (self.size() == other.size()) & \
            (self.diag_lb() == other.diag_lb())

    def size(self):
        """
        Returns the matrix size.
        """
        return self.__size

    def shape(self):
        """
        Returns the matrix shape, i.e., (size, size).
        """
        return (self.__size, self.__size)

    def diag_lb(self):
        """
        Returns the diagonal lower bound.
        """
        return self.__diag_lb

    def empty(self, valid):
        if valid:
            return np.eye(self.__size) * (self.__diag_lb + 1)
        else:
            return np.empty((self.__size, self.__size))

    def check_folded(self, folded_val, validate=None):
        """
        Check that the folded value is valid.

        If `validate = True`, checks that `folded_val` is a symmetric,
        positive-definite matrix of the correct shape with diagonal entries
        greater than the specified lower bound.  If `validate = False`,
        only the shape is checked.

        .. note::
            This method does not currently check for positive-definiteness.

        Parameters
        -----------
        folded_val: A numpy array
            A candidate value for a positive definite matrix.
        validate: Boolean
            Whether to check the matrix for attributes other than shape.

        Raises
        ----------
        If `folded_val` is not a valid matrix, raises a `ValueError`.
        """
        if folded_val.shape != (self.__size, self.__size):
            raise ValueError('Wrong shape for PDMatrix.')

        if validate is None:
            validate = self.default_validate
        if validate:
            if np.any(np.diag(folded_val) < self.__diag_lb):
                error_string = \
                    'Diagonal is less than the lower bound {}.'.format(
                        self.__diag_lb)
                raise ValueError(error_string)
            if not (folded_val.transpose() == folded_val).all():
                raise ValueError('Matrix is not symmetric')
            # TODO: check for positive definiteness?
            # try:
            #     chol = onp.linalg.cholesky(folded_val)
            # except LinAlgError:
            #     raise ValueError('Matrix is not positive definite.')

    def flatten(self, folded_val, free, validate=None):
        self.check_folded(folded_val, validate)
        if free:
            return _pack_posdef_matrix(folded_val, diag_lb=self.__diag_lb)
        else:
            return folded_val.flatten()

    def fold(self, flat_val, free, validate=None):
        flat_val = np.atleast_1d(flat_val)
        if len(flat_val.shape) != 1:
            raise ValueError('The argument to fold must be a 1d vector.')
        if flat_val.size != self.flat_length(free):
            raise ValueError(
                'Wrong length for PSDSymmetricMatrix flat value.')
        if free:
            return _unpack_posdef_matrix(flat_val, diag_lb=self.__diag_lb)
        else:
            folded_val = np.reshape(flat_val, (self.__size, self.__size))
            self.check_folded(folded_val, validate)
            return folded_val
