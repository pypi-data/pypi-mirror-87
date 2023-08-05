import numpy as np
from functools import reduce
import gc
import logging
from scipy.sparse import hstack


def pxem_mme(y, xmat, zmat_lst, gmat_inv_lst, init=None, maxiter=100, cc_par=1.0e-8):
    """
    Estimate variance parameters with mme based em
    :param y:
    :param xmat:
    :param gmat_inv_lst:
    :param init:
    :param maxiter:
    :param cc_par:
    :param cc_gra:
    :return:
    """
    num_varcom = len(gmat_inv_lst) + 1
    var_com = np.ones(num_varcom)
    if init is not None:
        var_com = np.array(init)
    var_com_new = np.array(var_com)
    logging.info("Prepare the coef matrix without variance parameters")
    xmat_df = xmat.shape[1]
    zmat_concat = hstack(zmat_lst)
    xzmat = hstack([xmat, zmat_concat])
    coef_null = xzmat.T.dot(xzmat)
    rhs_null = xzmat.T.dot(y)
    logging.info("Start iteration")
    iter = 0
    cc_par_val = 10000.0
    while iter < maxiter:
        iter += 1
        logging.info('Round: {:d}'.format(iter))
        # coef matrix
        coef = coef_null.toarray() / var_com[-1]
        df_sum = xmat_df
        for k in range(len(gmat_inv_lst)):
            indexa = df_sum
            df_sum += gmat_inv_lst[k].shape[0]
            indexb = df_sum
            coef[indexa:indexb, indexa:indexb] = coef[indexa:indexb, indexa:indexb] + gmat_inv_lst[k]/var_com[k]
        # right hand
        rhs_mat = rhs_null/var_com[-1]
        coef_inv = np.linalg.inv(coef)
        eff = np.dot(coef_inv, rhs_mat)
        # error variance
        e_hat = y - xzmat.dot(eff)
        var_com_new[-1] = np.sum(np.dot(e_hat.T, e_hat)) + np.sum((xzmat.T.dot(xzmat)).toarray() * coef_inv) # fast trace calculation
        var_com_new[-1] /= y.shape[0]
        # random variances
        y_xb = y - np.dot(xmat, eff[:xmat_df, :])
        df_sum = xmat_df
        gamma_mat = np.zeros((len(gmat_inv_lst), len(gmat_inv_lst)))
        gamma_vec = np.zeros(len(gmat_inv_lst))
        for k in range(len(gmat_inv_lst)):
            indexa = df_sum
            df_sum += gmat_inv_lst[k].shape[0]
            indexb = df_sum
            var_com_new[k] = np.sum(coef_inv[indexa:indexb, indexa:indexb]*gmat_inv_lst[k]) \
                             + np.sum(reduce(np.dot, [eff[indexa:indexb, :].T, gmat_inv_lst[k], eff[indexa:indexb, :]]))
            qk = gmat_inv_lst[k].shape[0]
            var_com_new[k] /= qk
            zu1 = zmat_lst[k].dot(eff[indexa:indexb, :])
            gamma1 = np.sum(np.dot(zu1.T, y_xb)) - \
                     np.sum(zmat_lst[k].T.dot(xmat) * coef_inv[indexa:indexb, :xmat_df])
            gamma_vec[k] = gamma1/var_com[-1]
            df_sum2 = xmat_df
            for m in range(len(gmat_inv_lst)):
                indexc = df_sum2
                df_sum2 += gmat_inv_lst[k].shape[0]
                indexd = df_sum2
                zu2 = zmat_lst[m].dot(eff[indexc:indexd, :])
                gamma2 = np.sum(np.dot(zu1.T, zu2)) + \
                         np.sum((zmat_lst[k].T.dot(zmat_lst[m])).toarray() * coef_inv[indexa:indexb, indexc:indexd])
                gamma_mat[k, m] = gamma2/var_com[-1]
        # print(gamma_mat, gamma_vec)
        gamma = np.dot(np.linalg.inv(gamma_mat), gamma_vec)
        var_com_new[:-1] = var_com_new[:-1] * gamma * gamma
        # cc
        delta = np.array(var_com_new) - np.array(var_com)
        cc_par_val = np.sum(delta*delta)/np.sum(np.array(var_com_new)*np.array(var_com_new))
        cc_par_val = np.sqrt(cc_par_val)
        var_com = np.array(var_com_new)
        logging.info('Norm of update vector: {:e}'.format(cc_par_val))
        var_com_str = ' '.join(np.array(var_com, dtype=str))
        logging.info('Updated variances: {}'.format(var_com_str))
        if cc_par_val < cc_par:
            break
    if cc_par_val < cc_par:
        logging.info('Variances converged.')
    else:
        logging.info('Variances not converged.')
    return var_com


def pxem_vmat(y, xmat, zmat_lst, gmat_lst, init=None, maxiter=100, cc_par=1.0e-8):
    """
    :param y:
    :param xmat:
    :param zmat_lst:
    :param gmat_lst:
    :param init:
    :param maxiter:
    :param cc_par:
    :return:
    """
    logging.info("#####Prepare#####")
    var_com = [1.0] * (len(gmat_lst) + 1)
    if init is not None:
        var_com = init[:]
    var_com = np.array(var_com)
    var_com_new = np.array(var_com)*100
    y = np.array(y).reshape(-1, 1)
    n = y.shape[0]
    xmat = np.array(xmat).reshape(n, -1)
    zgzmat_lst = []
    for val in range(len(gmat_lst)):
        zgzmat_lst.append(zmat_lst[val].dot((zmat_lst[val].dot(gmat_lst[val])).T))
    logging.info('Initial variances: ' + ' '.join(list(np.array(var_com, dtype=str))))
    logging.info("#####Start the iteration#####\n\n")
    iter = 0
    cc_par_val = 1000.0
    while iter < maxiter:
        iter += 1
        logging.info('###Round: ' + str(iter) + '###')
        # V, the inverse of V and P
        vmat = np.diag([var_com[-1]] * n)
        for val in range(len(zgzmat_lst)):
            vmat += zgzmat_lst[val] * var_com[val]
        vmat = np.linalg.inv(vmat)
        vxmat = np.dot(vmat, xmat)
        xvxmat = np.dot(xmat.T, vxmat)
        pmat = vmat - reduce(np.dot, [vxmat, np.linalg.inv(xvxmat), vxmat.T])
        pymat = np.dot(pmat, y)
        # Updated variances
        var_com_new[-1] = var_com[-1] - var_com[-1] * var_com[-1] * np.trace(pmat)/n + \
                          var_com[-1] * var_com[-1] * np.sum(np.dot(pymat.T, pymat))/n
        # random
        y_xb = y - reduce(np.dot, [xmat, np.linalg.inv(xvxmat), vxmat.T, y])
        gamma_mat = np.zeros((len(gmat_lst), len(gmat_lst)))
        gamma_vec = np.zeros(len(gmat_lst))
        for val in range(len(gmat_lst)):
            var_com_new[val] = var_com[val] - \
                var_com[val] * var_com[val] * np.sum(zgzmat_lst[val]*pmat) / gmat_lst[val].shape[0] + \
                var_com[val] * var_com[val] * np.sum(reduce(np.dot, [pymat.T, zgzmat_lst[val], pymat])) / gmat_lst[val].shape[0]
            zu1 = np.dot(zgzmat_lst[val], pymat) * var_com[val]
            gamma1 = np.sum(np.dot(zu1.T, y_xb)) + \
                     np.sum(zmat_lst[val].T.dot(xmat) * reduce(np.dot, [(zmat_lst[val].dot(gmat_lst[val])).T, vxmat, np.linalg.inv(xvxmat)])) * var_com[val]
            gamma_vec[val] = gamma1/var_com[-1]
            for m in range(len(gmat_lst)):
                zu2 = np.dot(zgzmat_lst[m], pymat) * var_com[m]
                zjgizi = zmat_lst[m].dot((zmat_lst[val].dot(gmat_lst[val])).T) * var_com[val]
                zjgjzi = zmat_lst[m].dot((zmat_lst[val].dot(gmat_lst[m])).T) * var_com[m]
                if val == m:
                    gamma2_trace = np.trace(zjgizi) - np.sum(zjgizi * np.dot(zjgjzi.T, pmat))
                else:
                    gamma2_trace = -np.sum(zjgizi * np.dot(zjgjzi.T, pmat))
                gamma2 = np.sum(np.dot(zu1.T, zu2)) + gamma2_trace
                gamma_mat[val, m] = gamma2 / var_com[-1]
        # print(gamma_mat, gamma_vec)
        gamma = np.dot(np.linalg.inv(gamma_mat), gamma_vec)
        var_com_new[:-1] = var_com_new[:-1] * gamma * gamma
        delta = var_com_new - var_com
        cc_par_val = np.sum(delta * delta) / np.sum(var_com_new * var_com_new)
        cc_par_val = np.sqrt(cc_par_val)
        var_com = np.array(var_com_new)
        logging.info('Norm of update vector: ' + str(cc_par_val))
        logging.info('Updated variances: ' + ' '.join(list(np.array(var_com_new, dtype=str))))
        if cc_par_val < cc_par:
            break
    if cc_par_val < cc_par:
        logging.info('Variances converged.')
    else:
        logging.info('Variances not converged.')
    return var_com


def pxem_mme2(y, xmat, zmat_lst, gmat_inv_lst, init=None, maxiter=100, cc_par=1.0e-8):
    """
    Estimate variance parameters with mme based em
    :param y:
    :param xmat:
    :param gmat_inv_lst:
    :param init:
    :param maxiter:
    :param cc_par:
    :param cc_gra:
    :return:
    """
    num_varcom = len(gmat_inv_lst) + 1
    var_com = np.ones(num_varcom)
    if init is not None:
        var_com = np.array(init)
    var_com_new = np.array(var_com)
    logging.info("Prepare the coef matrix without variance parameters")
    xmat_df = xmat.shape[1]
    zmat_concat = hstack(zmat_lst)
    xzmat = hstack([xmat, zmat_concat])
    coef_null = xzmat.T.dot(xzmat)
    rhs_null = xzmat.T.dot(y)
    smat_null = np.eye(xmat.shape[0]) - reduce(np.dot, [xmat, np.linalg.inv(np.dot(xmat.T, xmat)), xmat.T])
    logging.info("Start iteration")
    iter = 0
    cc_par_val = 10000.0
    while iter < maxiter:
        iter += 1
        logging.info('Round: {:d}'.format(iter))
        # coef matrix
        coef = coef_null.toarray() / var_com[-1]
        df_sum = xmat_df
        for k in range(len(gmat_inv_lst)):
            indexa = df_sum
            df_sum += gmat_inv_lst[k].shape[0]
            indexb = df_sum
            coef[indexa:indexb, indexa:indexb] = coef[indexa:indexb, indexa:indexb] + gmat_inv_lst[k]/var_com[k]
        # right hand
        rhs_mat = rhs_null/var_com[-1]
        coef_inv = np.linalg.inv(coef)
        eff = np.dot(coef_inv, rhs_mat)
        smat = smat_null / var_com[-1]
        # error variance
        e_hat = y - xzmat.dot(eff)
        var_com_new[-1] = np.sum(np.dot(e_hat.T, e_hat)) + np.sum((xzmat.T.dot(xzmat)).toarray() * coef_inv) # fast trace calculation
        var_com_new[-1] /= y.shape[0]
        # random variances
        symat = np.dot(smat, y)
        df_sum = xmat_df
        gamma_mat = np.zeros((len(gmat_inv_lst), len(gmat_inv_lst)))
        gamma_vec = np.zeros(len(gmat_inv_lst))
        for k in range(len(gmat_inv_lst)):
            indexa = df_sum
            df_sum += gmat_inv_lst[k].shape[0]
            indexb = df_sum
            var_com_new[k] = np.sum(coef_inv[indexa:indexb, indexa:indexb]*gmat_inv_lst[k]) \
                             + np.sum(reduce(np.dot, [eff[indexa:indexb, :].T, gmat_inv_lst[k], eff[indexa:indexb, :]]))
            qk = gmat_inv_lst[k].shape[0]
            var_com_new[k] /= qk
            zu1 = zmat_lst[k].dot(eff[indexa:indexb, :])
            gamma1 = np.sum(np.dot(zu1.T, symat)) - \
                     np.sum(zmat_lst[k].T.dot(np.dot(smat, xmat)) * coef_inv[indexa:indexb, :xmat_df])
            gamma_vec[k] = gamma1
            df_sum2 = xmat_df
            for m in range(len(gmat_inv_lst)):
                indexc = df_sum2
                df_sum2 += gmat_inv_lst[k].shape[0]
                indexd = df_sum2
                zu2 = zmat_lst[m].dot(eff[indexc:indexd, :])
                gamma2 = np.sum(reduce(np.dot, [zu1.T, smat, zu2])) + \
                         np.sum(zmat_lst[k].T.dot((zmat_lst[m].T.dot(smat)).T) * coef_inv[indexa:indexb, indexc:indexd])
                gamma_mat[k, m] = gamma2
        # print(gamma_mat, gamma_vec)
        gamma = np.dot(np.linalg.inv(gamma_mat), gamma_vec)
        var_com_new[:-1] = var_com_new[:-1] * gamma * gamma
        # cc
        delta = np.array(var_com_new) - np.array(var_com)
        cc_par_val = np.sum(delta*delta)/np.sum(np.array(var_com_new)*np.array(var_com_new))
        cc_par_val = np.sqrt(cc_par_val)
        var_com = np.array(var_com_new)
        logging.info('Norm of update vector: {:e}'.format(cc_par_val))
        var_com_str = ' '.join(np.array(var_com, dtype=str))
        logging.info('Updated variances: {}'.format(var_com_str))
        if cc_par_val < cc_par:
            break
    if cc_par_val < cc_par:
        logging.info('Variances converged.')
    else:
        logging.info('Variances not converged.')
    return var_com


def pxem_vmat2(y, xmat, zmat_lst, gmat_lst, init=None, maxiter=100, cc_par=1.0e-8):
    """
    :param y:
    :param xmat:
    :param zmat_lst:
    :param gmat_lst:
    :param init:
    :param maxiter:
    :param cc_par:
    :return:
    """
    logging.info("#####Prepare#####")
    var_com = [1.0] * (len(gmat_lst) + 1)
    if init is not None:
        var_com = init[:]
    var_com = np.array(var_com)
    var_com_new = np.array(var_com)*100
    y = np.array(y).reshape(-1, 1)
    n = y.shape[0]
    xmat = np.array(xmat).reshape(n, -1)
    h_mat = np.eye(xmat.shape[0]) - reduce(np.dot, [xmat, np.linalg.inv(np.dot(xmat.T, xmat)), xmat.T])
    zgzmat_lst = []
    for val in range(len(gmat_lst)):
        zgzmat_lst.append(zmat_lst[val].dot((zmat_lst[val].dot(gmat_lst[val])).T))
    logging.info('Initial variances: ' + ' '.join(list(np.array(var_com, dtype=str))))
    logging.info("#####Start the iteration#####\n\n")
    iter = 0
    cc_par_val = 1000.0
    while iter < maxiter:
        iter += 1
        logging.info('###Round: ' + str(iter) + '###')
        # V, the inverse of V and P
        vmat = np.diag([var_com[-1]] * n)
        for val in range(len(zgzmat_lst)):
            vmat += zgzmat_lst[val] * var_com[val]
        zgzmat = vmat - np.diag([var_com[-1]] * n)
        vmat = np.linalg.inv(vmat)
        vxmat = np.dot(vmat, xmat)
        xvxmat = np.dot(xmat.T, vxmat)
        xvxmat = np.linalg.inv(xvxmat)
        vxxvxxv_mat = reduce(np.dot, [vxmat, xvxmat, vxmat.T])
        pmat = vmat - vxxvxxv_mat
        pymat = np.dot(pmat, y)
        # Updated variances
        trace_term = np.trace(h_mat) * var_com[-1] - np.sum(h_mat*pmat) * var_com[-1] * var_com[-1]
        y_zu = y - np.dot(zgzmat, pymat)
        var_com_new[-1] = trace_term + np.sum(reduce(np.dot, [y_zu.T, h_mat, y_zu]))
        var_com_new[-1] /= n - xmat.shape[1]
        # random
        smat = h_mat / var_com[-1]
        symat = np.dot(smat, y)
        sxmat = np.dot(smat, xmat)
        gamma_mat = np.zeros((len(gmat_lst), len(gmat_lst)))
        gamma_vec = np.zeros(len(gmat_lst))
        for val in range(len(gmat_lst)):
            var_com_new[val] = var_com[val] - \
                               var_com[val] * var_com[val] * np.sum(zgzmat_lst[val] * pmat) / gmat_lst[val].shape[0] + \
                               var_com[val] * var_com[val] * np.sum(reduce(np.dot, [pymat.T, zgzmat_lst[val], pymat])) / \
                               gmat_lst[val].shape[0]
            zu1 = np.dot(zgzmat_lst[val], pymat) * var_com[val]
            gamma1 = np.sum(np.dot(zu1.T, symat)) + \
                     np.sum(zmat_lst[val].T.dot(sxmat) * reduce(np.dot, [(zmat_lst[val].dot(gmat_lst[val])).T, vxmat,
                                                                        xvxmat])) * var_com[val]
            gamma_vec[val] = gamma1
            for m in range(len(gmat_lst)):
                zu2 = np.dot(zgzmat_lst[m], pymat) * var_com[m]
                zjgizi = zmat_lst[m].dot((zmat_lst[val].dot(gmat_lst[val])).T) * var_com[val]
                zjgjzi = zmat_lst[m].dot((zmat_lst[val].dot(gmat_lst[m])).T) * var_com[m]
                if val == m:
                    gamma2_trace = np.sum(smat * zjgizi.T) - np.sum(np.dot(smat, zjgizi) * np.dot(zjgjzi.T, pmat))
                else:
                    gamma2_trace = - np.sum(np.dot(smat, zjgizi) * np.dot(zjgjzi.T, pmat))
                gamma2 = np.sum(reduce(np.dot, [zu1.T, smat, zu2])) + gamma2_trace
                gamma_mat[val, m] = gamma2
        # print(gamma_mat, gamma_vec)
        gamma = np.dot(np.linalg.inv(gamma_mat), gamma_vec)
        var_com_new[:-1] = var_com_new[:-1] * gamma * gamma
        delta = var_com_new - var_com
        cc_par_val = np.sum(delta * delta) / np.sum(var_com_new * var_com_new)
        cc_par_val = np.sqrt(cc_par_val)
        var_com = np.array(var_com_new)
        logging.info('Norm of update vector: ' + str(cc_par_val))
        logging.info('Updated variances: ' + ' '.join(list(np.array(var_com_new, dtype=str))))
        if cc_par_val < cc_par:
            break
    if cc_par_val < cc_par:
        logging.info('Variances converged.')
    else:
        logging.info('Variances not converged.')
    return var_com
