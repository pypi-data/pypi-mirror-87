import numpy as np

from cirq import ops


def RXX(theta: float) -> ops.XXPowGate:
    """The XX Ising coupling gate, a native two-qubit operation in ion traps.

    A rotation around the XX axis in the two-qubit bloch sphere.

    The gate implements the following unitary:

        exp(-i θ XX) = [ cos(θ)   0        0       -isin(θ)]
                       [ 0        cos(θ)  -isin(θ)  0      ]
                       [ 0       -isin(θ)  cos(θ)   0      ]
                       [-isin(θ)  0        0        cos(θ) ]

    Args:
        rads: float, sympy.Basic
        	The rotation angle in radians.

    Returns:
        RXX gate with a rotation of `theta` angle.
    """
    return ops.XXPowGate(exponent=theta * 2 / np.pi, global_shift=-0.5)

def RYY(rads: float) -> ops.YYPowGate:
    """The YY Ising coupling gate

    A rotation around the YY axis in the two-qubit bloch sphere.

    The gate implements the following unitary:

        exp(-i θ YY) = [ cos(θ)   0        0       sin(θ)]
                       [ 0        cos(θ)  -isin(θ)  0      ]
                       [ 0       -isin(θ)  cos(θ)   0      ]
                       [sin(θ)  0        0        cos(θ) ]

    Args:
        rads: float, sympy.Basic
        	The rotation angle in radians.

    Returns:
        RYY gate with a rotation of `theta` angle.
    """
    return ops.YYPowGate(exponent=theta * 2 / np.pi, global_shift=-0.5)

def RZZ(rads: float) -> ops.ZZPowGate:
    """The ZZ Ising coupling gate

    A rotation around the ZZ axis in the two-qubit bloch sphere.

    The gate implements the following unitary:

        exp(-i θ ZZ) = [ exp(iθ/2)     0        0           0     ]
                       [    0      exp(-iθ/2)   0           0     ]
                       [    0          0     exp(-iθ/2)     0     ]
                       [    0          0        0       exp(iθ/2) ]

    Args:
        rads: float, sympy.Basic
        	The rotation angle in radians.

    Returns:
        RZZ gate with a rotation of `theta` angle.
    """
    return ops.ZZPowGate(exponent=theta * 2 / np.pi, global_shift=-0.5)    