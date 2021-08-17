import numpy as np


class FellegiSunterEM:

    def __init__(self, dfA, dfB):

        self.k = 0;
        if dfA.shape[1] == dfB.shape[1]:
            self.k = dfA.shape[1] - 1  # id-field
        else:
            raise ValueError("Shape of frames must be the same")

        self.dfA = dfA
        self.dfB = dfB
        self.n1 = dfA.shape[0]
        self.n2 = dfB.shape[0]

    def e_step(self, agree_matrix, p, m, u):
        n, k = agree_matrix.shape
        res = np.zeros((n, 2))

        disagree_matrix = 1.0 - agree_matrix

        v1_exp_term = np.log(p) + np.dot(agree_matrix, np.log(m)) + np.dot(disagree_matrix, np.log(1.0 - m))
        v2_exp_term = np.log(1.0 - p) + np.dot(agree_matrix, np.log(u)) + np.dot(disagree_matrix, np.log(1.0 - u))

        v1 = np.exp(v1_exp_term)
        v2 = np.exp(v2_exp_term)

        return {"g_m": v1 / (v1 + v2), "g_u": v2 / (v1 + v2)}

    def run_em(self, agree_matrix, tolerance=0.01, max_iter=1000, verbose=True):

        N = agree_matrix.shape[0]
        p = 0.5
        m = np.repeat(0.9, self.k)  # empirical priors
        u = np.repeat(0.1, self.k)  # empirical priors

        conv_flag = -1

        for i in range(max_iter):
            print("Iteration: ", i)

            _p = p
            _m = m
            _u = u

            expect = self.e_step(agree_matrix, p, m, u)
            g_m = expect.get("g_m")
            g_u = expect.get("g_u")

            sigma_gm = np.sum(g_m)
            sigma_gu = np.sum(g_u)

            # M step

            # p: proportion of matched pairs
            p = sigma_gm / N

            m = np.dot(g_m, agree_matrix / sigma_gm)
            u = np.dot(g_u, agree_matrix / sigma_gu)

            if np.any(m > 0.99999):
                m[m > 0.99999] = 0.99999
            if np.any(m < 0.00001):
                m[m < 0.00001] = 0.00001  # 1e-05

            if np.any(u > 0.99999):
                u[u > 0.99999] = 0.99999
            if np.any(u < 0.00001):
                u[u < 0.00001] = 0.00001  # 1e-05

            if np.any(p > 0.99999):
                p[p > 0.99999] = 0.99999
            if np.any(p < 0.00001):
                p[p < 0.00001] = 0.00001  # 1e-05

            if verbose:
                print("p :", p)
                print("m :", m)
                print("u :", u)

            covergence_flag = np.abs(_p - p) < tolerance and np.all(np.abs(_m - m) < tolerance) and np.all(
                np.abs(_u - u) < tolerance)

            if np.any(np.isnan(covergence_flag)):
                p = _p
                m = _m
                u = _u
                conv_flag = 0
                break;

            if covergence_flag:
                conv_flag = 1
                break;

            if i == max_iter:
                conv_flag = 2

        print("Run completed.")

        return {
            "agree-score": m,
            "disagree-score": u,
            "prob": p,
            "convergence-flag": conv_flag
        }
