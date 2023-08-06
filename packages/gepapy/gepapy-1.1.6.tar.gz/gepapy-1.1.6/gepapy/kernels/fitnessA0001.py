from __future__ import division
from numba import cuda  # type: ignore
import numpy as np  # type: ignore
import cupy as cp  # type: ignore
import math


class FitnessA0001:
    """FitnessA0001."""

    def __init__(self) -> None:
        """__init__.

        :rtype: None
        """
        pass

    def _fitnessA0001(
        self,
        x: cp.core.core.ndarray,
        d: cp.core.core.ndarray,
        w: cp.core.core.ndarray,
        T: cp.core.core.ndarray,
        M: cp.core.core.ndarray,
        digits: int,
        n_samples: int,
        n_machines: int,
    ) -> cp.core.core.ndarray:
        """_fitnessA0001.

        :param x:
        :type x: cp.core.core.ndarray
        :param d:
        :type d: cp.core.core.ndarray
        :param w:
        :type w: cp.core.core.ndarray
        :param T:
        :type T: cp.core.core.ndarray
        :param M:
        :type M: cp.core.core.ndarray
        :param digits:
        :type digits: int
        :param n_samples:
        :type n_samples: int
        :param n_machines:
        :type n_machines: int
        :rtype: cp.core.core.ndarray
        """

        def fitnessAC0001():
            """fitnessAC0001."""

            @cuda.jit
            def kernel(x, T, M, digits, n_samples, n_machines, c_o, t_j, t_m):
                row = cuda.grid(1)
                if row < n_samples:
                    for i in range(x.shape[1]):
                        idx = int(math.ceil(x[row, i]))
                        t_aux = int(
                            math.ceil(T[row, idx, int(math.ceil(c_o[row, idx]))])
                        )
                        m_aux = int(
                            math.ceil(M[row, idx, int(math.ceil(c_o[row, idx]))])
                        )
                        c_o[row, idx] = c_o[row, idx] + 1

                        if t_m[row, m_aux] > t_j[row, idx]:
                            t_m[row, m_aux] = t_m[row, m_aux] + t_aux
                            t_j[row, idx] = t_m[row, m_aux]

                        else:
                            t_j[row, idx] = t_j[row, idx] + t_aux
                            t_m[row, m_aux] = t_j[row, idx]

            T_expand = cp.array(
                cp.repeat(cp.expand_dims(T, axis=0), n_samples, axis=0),
                dtype=cp.float32,
            )
            M_expand = cp.array(
                cp.repeat(cp.expand_dims(M, axis=0), n_samples, axis=0),
                dtype=cp.float32,
            )
            c_o_expand = cp.array(cp.zeros([n_samples, digits]), dtype=cp.float32)
            t_j_expand = cp.array(cp.zeros([n_samples, digits]), dtype=cp.float32)
            t_m_expand = cp.array(cp.zeros([n_samples, n_machines]), dtype=cp.float32)
            threadsperblock = 16
            blockspergrid_x = int(math.ceil(n_samples / threadsperblock))
            blockspergrid = blockspergrid_x

            cuda.synchronize()
            kernel[blockspergrid, threadsperblock](
                x,
                T_expand,
                M_expand,
                digits,
                n_samples,
                n_machines,
                c_o_expand,
                t_j_expand,
                t_m_expand,
            )
            cuda.synchronize()

            return t_j_expand

        C = fitnessAC0001()

        def fitnessAC0002() -> dict:
            """fitnessAC0002.

            :rtype: dict
            """
            d_expand = cp.array(
                cp.repeat(cp.expand_dims(d, axis=0), n_samples, axis=0),
                dtype=cp.float32,
            )
            w_expand = cp.array(
                cp.repeat(cp.expand_dims(w, axis=0), n_samples, axis=0),
                dtype=cp.float32,
            )
            L = C - d_expand
            LT = cp.where(L > 0, L, 0)
            U = cp.where(L > 0, L, 0)
            Lw = L * w_expand
            LTw = LT * w_expand
            Uw = U * w_expand
            E_C = cp.sum(C, axis=1)
            E_L = cp.sum(L, axis=1)
            E_LT = cp.sum(LT, axis=1)
            E_U = cp.sum(U, axis=1)
            E_Lw = cp.sum(Lw, axis=1)
            E_LTw = cp.sum(LTw, axis=1)
            E_Uw = cp.sum(Uw, axis=1)
            max_C = cp.max(C, axis=1)

            return {
                "E_C": E_C,
                "E_L": E_L,
                "E_LT": E_LT,
                "E_U": E_U,
                "E_Lw": E_Lw,
                "E_LTw": E_LTw,
                "E_Uw": E_Uw,
                "max_C": max_C,
            }

        return fitnessAC0002()

    def _get_planA0001(
        self,
        row: int,
        X: cp.core.core.ndarray,
        T: cp.core.core.ndarray,
        M: cp.core.core.ndarray,
        digits: int,
        n_machines: int,
        fact_conv: float,
        start_time: int,
    ) -> list:
        """_get_planA0001.

        :param row:
        :type row: int
        :param X:
        :type X: cp.core.core.ndarray
        :param T:
        :type T: cp.core.core.ndarray
        :param M:
        :type M: cp.core.core.ndarray
        :param digits:
        :type digits: int
        :param n_machines:
        :type n_machines: int
        :param fact_conv:
        :type fact_conv: float
        :param start_time:
        :type start_time: int
        :rtype: list
        """

        x = cp.asnumpy(X[row].copy())
        T = cp.asnumpy(T)
        M = cp.asnumpy(M)
        c_o = np.zeros(digits, dtype=int)
        t_m = np.zeros(n_machines, dtype=int)
        t_j = np.zeros(digits, dtype=int)

        plan = []

        for i in range(x.shape[0]):
            idx = int(math.ceil(x[i]))
            t_aux = int(math.ceil(T[idx, int(math.ceil(c_o[idx]))]))
            m_aux = int(math.ceil(M[idx, int(math.ceil(c_o[idx]))]))
            c_o[idx] = c_o[idx] + 1

            if t_m[m_aux] > t_j[idx]:
                plan.append(
                    {
                        "Finish": (t_m[m_aux] + t_aux) * fact_conv + start_time,
                        "Resource": "Job {}".format(idx),
                        "Start": (t_m[m_aux]) * fact_conv + start_time,
                        "Task": "Machine {}".format(m_aux),
                    }
                )
                t_m[m_aux] = t_m[m_aux] + t_aux
                t_j[idx] = t_m[m_aux]

            else:
                plan.append(
                    {
                        "Finish": (t_j[idx] + t_aux) * fact_conv + start_time,
                        "Resource": "Job {}".format(idx),
                        "Start": (t_j[idx]) * fact_conv + start_time,
                        "Task": "Machine {}".format(m_aux),
                    }
                )
                t_j[idx] = t_j[idx] + t_aux
                t_m[m_aux] = t_j[idx]
        return plan
