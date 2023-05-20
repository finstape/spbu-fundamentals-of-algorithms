import numpy as np
from numpy.typing import NDArray


def lu(A: NDArray, permute: bool) -> tuple[NDArray, NDArray, NDArray]:
    n = A.shape[0]
    L, U, P = np.eye(n), np.copy(A), np.eye(n)

    for i in range(n - 1):
        if permute:
            k = np.argmax(np.abs(U[i:, i])) + i  # Find the index of the row with the maximum element in column k
            U[[i, k]] = U[[k, i]]  # Swap rows i and k in matrix U
            P[[i, k]] = P[[k, i]]  # Swap rows i and k in matrix P
            L[[i, k], :i] = L[[k, i], :i]  # Swap elements in columns 0 to i-1 in rows i and k in matrix L

        # Calculate the values of the elements of column i under the main diagonal in the matrix L by dividing the
        # corresponding elements of column i of the matrix U by the element U[i, i]
        L[i + 1:, i] = U[i + 1:, i] / U[i, i]
        # Subtract the product of row i in matrix L and column i in matrix U from the corresponding submatrix U
        U[i + 1:, i:] -= L[i + 1:, i].reshape(-1, 1) * U[i, i:]

    return L, U, P


def solve(L: NDArray, U: NDArray, P: NDArray, b: NDArray) -> NDArray:
    n = L.shape[0]
    x, y = np.zeros(n), np.zeros(n)
    b = P @ b

    for i in range(n):
        y[i] = b[i] - L[i, :i] @ y[:i]

    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - U[i, i + 1:] @ x[i + 1:]) / U[i, i]

    return x


def get_A_b(a_11: float, b_1: float) -> tuple[NDArray, NDArray]:
    A = np.array([[a_11, 1.0, -3.0], [6.0, 2.0, 5.0], [1.0, 4.0, -3.0]])
    b = np.array([b_1, 12.0, -39.0])
    return A, b


if __name__ == "__main__":
    # Let's implement the LU decomposition with and without pivoting
    # and check its stability depending on the matrix elements
    p = 8  # modify from 7 to 16 to check instability
    a_11 = 3 + 10 ** (-p)  # add/remove 10**(-p) to check instability
    b_1 = -16 + 10 ** (-p)  # add/remove 10**(-p) to check instability
    A, b = get_A_b(a_11, b_1)
    # With pivoting
    L, U, P = lu(A, permute=True)
    x = solve(L, U, P, b)
    assert np.all(np.isclose(x, [1, -7, 4])), f"The answer {x} is not accurate enough"
    # Without pivoting
    L, U, P = lu(A, permute=False)
    x_ = solve(L, U, P, b)
    assert np.all(np.isclose(x_, [1, -7, 4])), f"The answer {x_} is not accurate enough"
