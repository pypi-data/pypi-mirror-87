# -*- coding: utf-8 -*-
import numpy as np
from qibo import matrices, K
from qibo.config import BACKEND_NAME, DTYPES, raise_error
from qibo.base.hamiltonians import Hamiltonian as BaseHamiltonian
from qibo.base.hamiltonians import _SymbolicHamiltonian
if BACKEND_NAME == "tensorflow":
    from qibo.tensorflow import hamiltonians
    from qibo.tensorflow.hamiltonians import TensorflowTrotterHamiltonian as TrotterHamiltonian
else: # pragma: no cover
    # case not tested because backend is preset to TensorFlow
    raise raise_error(NotImplementedError,
                      "Only Tensorflow backend is implemented.")


class Hamiltonian(BaseHamiltonian):
    """"""

    def __new__(cls, nqubits, matrix, numpy=False):
        if isinstance(matrix, np.ndarray):
            if not numpy:
                matrix = K.cast(matrix, dtype=DTYPES.get('DTYPECPX'))
        elif isinstance(matrix, K.Tensor):
            if numpy:
                matrix = matrix.numpy()
        else:
            raise raise_error(TypeError, "Invalid type {} of Hamiltonian "
                                         "matrix.".format(type(matrix)))
        if numpy:
            return hamiltonians.NumpyHamiltonian(nqubits, matrix)
        else:
            return hamiltonians.TensorflowHamiltonian(nqubits, matrix)

    @classmethod
    def from_symbolic(cls, symbolic_hamiltonian, symbol_map, numpy=False):
        """See :class:`qibo.base.hamiltonians.Hamiltonian` for docs."""
        ham = _SymbolicHamiltonian(symbolic_hamiltonian, symbol_map)
        return cls(ham.nqubits, ham.dense_matrix(), numpy=numpy)


def _build_spin_model(nqubits, matrix, condition):
    """Helper method for building nearest-neighbor spin model Hamiltonians."""
    h = sum(_SymbolicHamiltonian._multikron(
      (matrix if condition(i, j) else matrices.I for j in range(nqubits)))
            for i in range(nqubits))
    return h


def XXZ(nqubits, delta=0.5, numpy=False, trotter=False):
    """Heisenberg XXZ model with periodic boundary conditions.

    .. math::
        H = \\sum _{i=0}^N \\left ( X_iX_{i + 1} + Y_iY_{i + 1} + \\delta Z_iZ_{i + 1} \\right ).

    Args:
        nqubits (int): number of quantum bits.
        delta (float): coefficient for the Z component (default 0.5).
        numpy (bool): If ``True`` the Hamiltonian is created using numpy as the
            calculation backend, otherwise TensorFlow is used.
            Default option is ``numpy = False``.
        trotter (bool): If ``True`` it creates the Hamiltonian as a
            :class:`qibo.base.hamiltonians.TrotterHamiltonian` object, otherwise
            it creates a :class:`qibo.base.hamiltonians.Hamiltonian` object.

    Example:
        ::

            from qibo.hamiltonians import XXZ
            h = XXZ(3) # initialized XXZ model with 3 qubits
    """
    if trotter:
        hx = np.kron(matrices.X, matrices.X)
        hy = np.kron(matrices.Y, matrices.Y)
        hz = np.kron(matrices.Z, matrices.Z)
        term = Hamiltonian(2, hx + hy + delta * hz, numpy=True)
        terms = {(i, i + 1): term for i in range(nqubits - 1)}
        terms[(nqubits - 1, 0)] = term
        return TrotterHamiltonian.from_dictionary(terms)

    condition = lambda i, j: i in {j % nqubits, (j+1) % nqubits}
    hx = _build_spin_model(nqubits, matrices.X, condition)
    hy = _build_spin_model(nqubits, matrices.Y, condition)
    hz = _build_spin_model(nqubits, matrices.Z, condition)
    matrix = hx + hy + delta * hz
    return Hamiltonian(nqubits, matrix, numpy=numpy)


def _OneBodyPauli(nqubits, matrix, numpy=False, trotter=False,
                  ground_state=None):
    """Helper method for constracting non-interacting X, Y, Z Hamiltonians."""
    if not trotter:
        condition = lambda i, j: i == j % nqubits
        ham = -_build_spin_model(nqubits, matrix, condition)
        return Hamiltonian(nqubits, ham, numpy=numpy)

    term = Hamiltonian(1, -matrix, numpy=True)
    terms = {(i,): term for i in range(nqubits)}
    return TrotterHamiltonian.from_dictionary(terms, ground_state=ground_state)


def X(nqubits, numpy=False, trotter=False):
    """Non-interacting Pauli-X Hamiltonian.

    .. math::
        H = - \\sum _{i=0}^N X_i.

    Args:
        nqubits (int): number of quantum bits.
        numpy (bool): If ``True`` the Hamiltonian is created using numpy as the
            calculation backend, otherwise TensorFlow is used.
            Default option is ``numpy = False``.
        trotter (bool): If ``True`` it creates the Hamiltonian as a
            :class:`qibo.base.hamiltonians.TrotterHamiltonian` object, otherwise
            it creates a :class:`qibo.base.hamiltonians.Hamiltonian` object.
    """
    def ground_state():
        n = K.cast(2 ** nqubits, dtype=DTYPES.get('DTYPEINT'))
        state = K.ones(n, dtype=DTYPES.get('DTYPECPX'))
        return state / K.math.sqrt(K.cast(n, dtype=state.dtype))
    return _OneBodyPauli(nqubits, matrices.X, numpy, trotter, ground_state)


def Y(nqubits, numpy=False, trotter=False):
    """Non-interacting Pauli-Y Hamiltonian.

    .. math::
        H = - \\sum _{i=0}^N Y_i.

    Args:
        nqubits (int): number of quantum bits.
        numpy (bool): If ``True`` the Hamiltonian is created using numpy as the
            calculation backend, otherwise TensorFlow is used.
            Default option is ``numpy = False``.
        trotter (bool): If ``True`` it creates the Hamiltonian as a
            :class:`qibo.base.hamiltonians.TrotterHamiltonian` object, otherwise
            it creates a :class:`qibo.base.hamiltonians.Hamiltonian` object.
    """
    return _OneBodyPauli(nqubits, matrices.Y, numpy, trotter)


def Z(nqubits, numpy=False, trotter=False):
    """Non-interacting Pauli-Z Hamiltonian.

    .. math::
        H = - \\sum _{i=0}^N Z_i.

    Args:
        nqubits (int): number of quantum bits.
        numpy (bool): If ``True`` the Hamiltonian is created using numpy as the
            calculation backend, otherwise TensorFlow is used.
            Default option is ``numpy = False``.
        trotter (bool): If ``True`` it creates the Hamiltonian as a
            :class:`qibo.base.hamiltonians.TrotterHamiltonian` object, otherwise
            it creates a :class:`qibo.base.hamiltonians.Hamiltonian` object.
    """
    return _OneBodyPauli(nqubits, matrices.Z, numpy, trotter)


def TFIM(nqubits, h=0.0, numpy=False, trotter=False):
    """Transverse field Ising model with periodic boundary conditions.

    .. math::
        H = - \\sum _{i=0}^N \\left ( Z_i Z_{i + 1} + h X_i \\right ).

    Args:
        nqubits (int): number of quantum bits.
        h (float): value of the transverse field.
        numpy (bool): If ``True`` the Hamiltonian is created using numpy as the
            calculation backend, otherwise TensorFlow is used.
            Default option is ``numpy = False``.
        trotter (bool): If ``True`` it creates the Hamiltonian as a
            :class:`qibo.base.hamiltonians.TrotterHamiltonian` object, otherwise
            it creates a :class:`qibo.base.hamiltonians.Hamiltonian` object.
    """
    if trotter:
        term_matrix = -np.kron(matrices.Z, matrices.Z)
        term_matrix -= h * np.kron(matrices.X, matrices.I)
        term = Hamiltonian(2, term_matrix, numpy=True)
        terms = {(i, i + 1): term for i in range(nqubits - 1)}
        terms[(nqubits - 1, 0)] = term
        return TrotterHamiltonian.from_dictionary(terms)

    condition = lambda i, j: i in {j % nqubits, (j+1) % nqubits}
    ham = -_build_spin_model(nqubits, matrices.Z, condition)
    if h != 0:
        condition = lambda i, j: i == j % nqubits
        ham -= h * _build_spin_model(nqubits, matrices.X, condition)
    return Hamiltonian(nqubits, ham, numpy=numpy)
