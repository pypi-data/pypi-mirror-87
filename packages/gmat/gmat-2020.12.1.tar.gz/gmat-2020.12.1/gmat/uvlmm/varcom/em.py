import numpy as np
from functools import reduce
import gc
import logging
from scipy.sparse import hstack


def em_mme(y, xmat, zmat_lst, gmat_inv_lst, init=None, maxiter=100, cc_par=1.0e-8):
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
        df_sum = xmat_df
        for k in range(len(gmat_inv_lst)):
            indexa = df_sum
            df_sum += gmat_inv_lst[k].shape[0]
            indexb = df_sum
            var_com_new[k] = np.sum(coef_inv[indexa:indexb, indexa:indexb]*gmat_inv_lst[k]) \
                             + np.sum(reduce(np.dot, [eff[indexa:indexb, :].T, gmat_inv_lst[k], eff[indexa:indexb, :]]))
            qk = gmat_inv_lst[k].shape[0]
            var_com_new[k] /= qk
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


def em_vmat(y, xmat, zmat_lst, gmat_lst, init=None, maxiter=100, cc_par=1.0e-8):
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
        for val in range(len(gmat_lst)):
            var_com_new[val] = var_com[val] - var_com[val] * var_com[val] * np.sum(zgzmat_lst[val]*pmat) / n + \
                var_com[val] * var_com[val] * np.sum(reduce(np.dot, [pymat.T, zgzmat_lst[val], pymat])) / n
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


def em_mme2(y, xmat, zmat_lst, gmat_inv_lst, init=None, maxiter=100, cc_par=1.0e-8):
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
    h_mat = np.eye(xmat.shape[0]) - reduce(np.dot, [xmat, np.linalg.inv(np.dot(xmat.T, xmat)), xmat.T])
    zhz_mat = zmat_concat.T.dot((zmat_concat.T.dot(h_mat)).T)
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
        e_hat2 = y - zmat_concat.dot(eff[xmat_df:, :])
        var_com_new[-1] = np.sum(reduce(np.dot, [e_hat2.T, h_mat, e_hat2])) + \
                            np.sum(zhz_mat * coef_inv[xmat_df:, xmat_df:]) # fast trace calculation
        var_com_new[-1] /= y.shape[0] - xmat_df
        # random variances
        df_sum = xmat_df
        for k in range(len(gmat_inv_lst)):
            indexa = df_sum
            df_sum += gmat_inv_lst[k].shape[0]
            indexb = df_sum
            var_com_new[k] = np.sum(coef_inv[indexa:indexb, indexa:indexb]*gmat_inv_lst[k]) \
                             + np.sum(reduce(np.dot, [eff[indexa:indexb, :].T, gmat_inv_lst[k], eff[indexa:indexb, :]]))
            qk = gmat_inv_lst[k].shape[0]
            var_com_new[k] /= qk
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


def em_vmat2(y, xmat, zmat_lst, gmat_lst, init=None, maxiter=100, cc_par=1.0e-8):
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
        trace_term1 = reduce(np.dot, [xmat, xvxmat, xmat.T])
        trace_term2 = reduce(np.dot, [xmat, xvxmat, vxmat.T]) * var_com[-1]
        trace_term = trace_term1 - trace_term2 + np.diag([var_com[-1]] * n) - vmat*var_com[-1]*var_com[-1] - \
                     trace_term2.T + vxxvxxv_mat * var_com[-1] * var_com[-1]
        trace_term = np.sum(trace_term * h_mat)
        y_zu = y - np.dot(zgzmat, pymat)
        var_com_new[-1] = trace_term + np.sum(reduce(np.dot, [y_zu.T, h_mat, y_zu]))
        var_com_new[-1] /= n - xmat.shape[1]
        for val in range(len(gmat_lst)):
            var_com_new[val] = var_com[val] - var_com[val] * var_com[val] * np.sum(zgzmat_lst[val]*pmat) / n + \
                var_com[val] * var_com[val] * np.sum(reduce(np.dot, [pymat.T, zgzmat_lst[val], pymat])) / n
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


def em_mme22(y, xmat, zmat_lst, gmat_inv_lst, init=None, maxiter=100, cc_par=1.0e-8):
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
    h_mat = np.eye(xmat.shape[0]) - reduce(np.dot, [xmat, np.linalg.inv(np.dot(xmat.T, xmat)), xmat.T])
    whw_mat = xzmat.T.dot((xzmat.T.dot(h_mat)).T)
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
        e_hat2 = y - zmat_concat.dot(eff[xmat_df:, :])
        var_com_new[-1] = np.sum(reduce(np.dot, [e_hat2.T, h_mat, e_hat2])) + \
                            np.sum(whw_mat * coef_inv) # fast trace calculation
        var_com_new[-1] /= y.shape[0] - xmat_df
        # random variances
        df_sum = xmat_df
        for k in range(len(gmat_inv_lst)):
            indexa = df_sum
            df_sum += gmat_inv_lst[k].shape[0]
            indexb = df_sum
            var_com_new[k] = np.sum(coef_inv[indexa:indexb, indexa:indexb]*gmat_inv_lst[k]) \
                             + np.sum(reduce(np.dot, [eff[indexa:indexb, :].T, gmat_inv_lst[k], eff[indexa:indexb, :]]))
            qk = gmat_inv_lst[k].shape[0]
            var_com_new[k] /= qk
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


def em_vmat22(y, xmat, zmat_lst, gmat_lst, init=None, maxiter=100, cc_par=1.0e-8):
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
        for val in range(len(gmat_lst)):
            var_com_new[val] = var_com[val] - var_com[val] * var_com[val] * np.sum(zgzmat_lst[val]*pmat) / n + \
                var_com[val] * var_com[val] * np.sum(reduce(np.dot, [pymat.T, zgzmat_lst[val], pymat])) / n
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
