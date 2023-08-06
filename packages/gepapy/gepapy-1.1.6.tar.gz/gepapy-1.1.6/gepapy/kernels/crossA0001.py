from __future__ import division
from numba import cuda  # type: ignore
import cupy as cp  # type: ignore
import math


class CrossA0001:
    """CrossA0001."""

    def __init__(self) -> None:
        """__init__.

        :rtype: None
        """
        pass

    def _crossA0001(
        self,
        X: cp.core.core.ndarray,
        digits: int,
        repetitions: int,
        n_samples: int,
        percent_c: float,
    ) -> cp.core.core.ndarray:
        """_crossA0001.

        :param X:
        :type X: cp.core.core.ndarray
        :param digits:
        :type digits: int
        :param repetitions:
        :type repetitions: int
        :param n_samples:
        :type n_samples: int
        :param percent_c:
        :type percent_c: float
        :rtype: cp.core.core.ndarray
        """

        def crossAC0001() -> cp.core.core.ndarray:
            """crossAC0001.

            :rtype: cp.core.core.ndarray
            """

            @cuda.jit
            def kernel(
                X: cp.core.core.ndarray,
                X_AUX: cp.core.core.ndarray,
                x_dim_1: int,
                percent_c: float,
            ) -> None:
                """kernel.

                :param X:
                :type X: cp.core.core.ndarray
                :param X_AUX:
                :type X_AUX: cp.core.core.ndarray
                :param x_dim_1:
                :type x_dim_1: int
                :param percent_c:
                :type percent_c: float
                :rtype: None
                """
                row = cuda.grid(1)
                if row < n_samples:
                    if row % 2 == 0:
                        for i in range(0, int(math.ceil(x_dim_1 * percent_c)), 1):
                            X_AUX[row, i] = X[row, i]

                    else:
                        for i in range(int(math.ceil(x_dim_1 * percent_c)), x_dim_1, 1):
                            X_AUX[row, i] = X[row, i]

            x_dim_1 = digits * repetitions
            X_AUX = cp.zeros([n_samples, x_dim_1])

            threadsperblock = 16
            blockspergrid_x = int(math.ceil((n_samples) / threadsperblock))
            blockspergrid = blockspergrid_x

            cuda.synchronize()
            kernel[blockspergrid, threadsperblock](X, X_AUX, x_dim_1, percent_c)
            cuda.synchronize()

            return X_AUX

        def crossAC0002() -> cp.core.core.ndarray:
            """crossAC0002.

            :rtype: cp.core.core.ndarray
            """

            @cuda.jit
            def kernel(
                X_AUX: cp.core.core.ndarray,
                C_M: cp.core.core.ndarray,
                digits: int,
                repetitions: int,
                x_dim_1: int,
                percent_c: float,
            ) -> None:
                """kernel.

                :param X_AUX:
                :type X_AUX: cp.core.core.ndarray
                :param C_M:
                :type C_M: cp.core.core.ndarray
                :param digits:
                :type digits: int
                :param repetitions:
                :type repetitions: int
                :param x_dim_1:
                :type x_dim_1: int
                :param percent_c:
                :type percent_c: float
                :rtype: None
                """
                row = cuda.grid(1)
                if row < n_samples:
                    if row % 2 == 0:
                        for i in range(digits):
                            count = 0
                            for j in range(0, int(math.ceil(x_dim_1 * percent_c)), 1):
                                if X_AUX[row, j] == i:
                                    count = count + 1
                                C_M[row, i] = count

                    else:
                        for i in range(digits):
                            count = 0
                            for j in range(
                                int(math.ceil(x_dim_1 * percent_c)), x_dim_1, 1
                            ):
                                if X_AUX[row, j] == i:
                                    count = count + 1
                                C_M[row, i] = count

            C_M = cp.zeros([n_samples, digits], dtype=cp.float32)
            x_dim_1 = digits * repetitions

            threadsperblock = 16
            blockspergrid_x = int(math.ceil((n_samples) / threadsperblock))
            blockspergrid = blockspergrid_x

            cuda.synchronize()
            kernel[blockspergrid, threadsperblock](
                X_AUX, C_M, digits, repetitions, x_dim_1, percent_c
            )
            cuda.synchronize()

            return C_M

        def crossAC0003() -> cp.core.core.ndarray:
            """crossAC0003.

            :rtype: cp.core.core.ndarray
            """

            @cuda.jit
            def kernel(
                X: cp.core.core.ndarray,
                X_AUX: cp.core.core.ndarray,
                C_M: cp.core.core.ndarray,
                digits: int,
                repetitions: int,
                x_dim_1: int,
                percent_c: float,
            ):
                """kernel.

                :param X:
                :type X: cp.core.core.ndarray
                :param X_AUX:
                :type X_AUX: cp.core.core.ndarray
                :param C_M:
                :type C_M: cp.core.core.ndarray
                :param digits:
                :type digits: int
                :param repetitions:
                :type repetitions: int
                :param x_dim_1:
                :type x_dim_1: int
                :param percent_c:
                :type percent_c: float
                """
                row = cuda.grid(1)
                if row < n_samples:
                    if row % 2 == 0:
                        discount = x_dim_1 - 1
                        for i in range(x_dim_1 - 1, -1, -1):
                            if discount >= int(math.ceil(x_dim_1 * percent_c)):
                                if (
                                    C_M[row, int(math.ceil(X[row + 1, i]))]
                                    < repetitions
                                ):
                                    X_AUX[row, discount] = X[row + 1, i]
                                    C_M[row, int(X[row + 1, i])] += 1
                                    discount -= 1

                    else:
                        count = 0
                        for i in range(0, x_dim_1, 1):
                            if count < int(math.ceil(x_dim_1 * percent_c)):
                                if (
                                    C_M[row, int(math.ceil(X[row - 1, i]))]
                                    < repetitions
                                ):
                                    X_AUX[row, count] = X[row - 1, i]
                                    C_M[row, int(X[row - 1, i])] += 1
                                    count += 1

            x_dim_1 = digits * repetitions

            threadsperblock = 16
            blockspergrid_x = int(math.ceil((n_samples) / threadsperblock))
            blockspergrid = blockspergrid_x

            cuda.synchronize()
            kernel[blockspergrid, threadsperblock](
                X, X_AUX, C_M, digits, repetitions, x_dim_1, percent_c
            )
            cuda.synchronize()

            return X_AUX

        X_AUX = crossAC0001()
        C_M = crossAC0002()
        X_AUX = crossAC0003()

        return X_AUX
