import tensorflow as tf
from tensorflow.keras import losses

from ._utils import compute_mmd, _nelem, _nan2zero, _nan2inf, _reduce_mean


def kl_recon_mse(mu, log_var, alpha=0.1, eta=1.0):
    def kl_recon_loss(y_true, y_pred):
        kl_loss = pure_kl_loss(mu, log_var)(y_true, y_pred)
        recon_loss = mse_loss(y_true, y_pred)
        return eta * recon_loss + alpha * kl_loss

    return kl_recon_loss


def kl_recon_sse(mu, log_var, alpha=0.1, eta=1.0):
    def kl_recon_loss(y_true, y_pred):
        kl_loss = pure_kl_loss(mu, log_var)(y_true, y_pred)
        recon_loss = sse_loss(y_true, y_pred)
        return eta * recon_loss + alpha * kl_loss

    return kl_recon_loss


class CVAELoss(tf.keras.losses.Loss):
    def __init__(self):
        super(CVAELoss, self).__init__(reduction=tf.keras.losses.Reduction.NONE)

    def call(self, y_true, y_pred):
        pass


def pure_kl_loss(mu, log_var):
    def kl_loss(y_true, y_pred):
        kl_div = tf.reduce_mean(tf.exp(log_var) + tf.square(mu) - 1. - log_var, 1)
        return tf.reduce_mean(kl_div)

    kl_loss.__name__ = "kl"

    return kl_loss


def sse_loss(y_true, y_pred):
    return tf.reduce_sum(tf.reduce_sum(tf.square((y_true - y_pred)), axis=-1))


def mse_loss(y_true, y_pred):
    return tf.reduce_mean(tf.keras.losses.mean_squared_error(y_true, y_pred))


def mmd(n_conditions, kernel_method='multi-scale-rbf', computation_method="general"):
    def mmd_loss(real_labels, y_pred):
        # with tf.compat.v1.variable_scope("mmd_loss", reuse=tf.compat.v1.AUTO_REUSE):
        real_labels = tf.reshape(tf.cast(real_labels, 'int32'), (-1,))
        conditions_mmd = tf.dynamic_partition(y_pred, real_labels, num_partitions=n_conditions)
        loss = 0.0
        if computation_method.isdigit():
            boundary = int(computation_method)
            for i in range(boundary):
                for j in range(boundary, n_conditions):
                    loss += _nan2zero(compute_mmd(conditions_mmd[i], conditions_mmd[j], kernel_method))
        else:
            for i in range(len(conditions_mmd)):
                for j in range(i):
                    loss += _nan2zero(compute_mmd(conditions_mmd[i], conditions_mmd[j], kernel_method))
        if n_conditions == 1:
            loss = _nan2zero(tf.zeros(shape=(1,)))[0]
        return loss

    return mmd_loss


# NB loss and ZINB are taken from https://github.com/theislab/dca, thanks to @gokceneraslan

class NB(object):
    def __init__(self, theta=None, masking=False, scope='nbinom_loss/',
                 scale_factor=1.0):

        # for numerical stability
        self.eps = 1e-8
        self.scale_factor = scale_factor
        self.scope = scope
        self.masking = masking
        self.theta = theta

    def loss(self, y_true, y_pred, mean=True):
        scale_factor = self.scale_factor
        eps = self.eps

        with tf.name_scope(self.scope):
            y_true = tf.cast(y_true, tf.float32)
            y_pred = tf.cast(y_pred, tf.float32) * scale_factor

            if self.masking:
                nelem = _nelem(y_true)
                y_true = _nan2zero(y_true)

            # Clip theta
            theta = tf.minimum(self.theta, 1e6)

            t1 = tf.math.lgamma(theta + eps) + tf.math.lgamma(y_true + 1.0) - tf.math.lgamma(y_true + theta + eps)
            t2 = (theta + y_true) * tf.math.log(1.0 + (y_pred / (theta + eps))) + (
                    y_true * (tf.math.log(theta + eps) - tf.math.log(y_pred + eps)))
            final = t1 + t2

            final = _nan2inf(final)

            if mean:
                if self.masking:
                    final = tf.divide(tf.reduce_sum(final), nelem)
                else:
                    final = tf.reduce_mean(final)

        return final


class ZINB(NB):
    def __init__(self, pi, ridge_lambda=0.0, scope='zinb_loss/', **kwargs):
        super().__init__(scope=scope, **kwargs)
        self.pi = pi
        self.ridge_lambda = ridge_lambda

    def loss(self, y_true, y_pred, mean=True):
        scale_factor = self.scale_factor
        eps = self.eps

        with tf.name_scope(self.scope):
            # reuse existing NB neg.log.lik.
            # mean is always False here, because everything is calculated
            # element-wise. we take the mean only in the end
            nb_case = super().loss(y_true, y_pred, mean=False) - tf.math.log(1.0 - self.pi + eps)

            y_true = tf.cast(y_true, tf.float32)
            y_pred = tf.cast(y_pred, tf.float32) * scale_factor
            theta = tf.minimum(self.theta, 1e6)

            zero_nb = tf.pow(theta / (theta + y_pred + eps), theta)
            zero_case = -tf.math.log(self.pi + ((1.0 - self.pi) * zero_nb) + eps)
            result = tf.where(tf.less(y_true, 1e-8), zero_case, nb_case)
            ridge = self.ridge_lambda * tf.square(self.pi)
            result += ridge

            if mean:
                if self.masking:
                    result = _reduce_mean(result)
                else:
                    result = tf.reduce_mean(result)

            result = _nan2inf(result)

        return result


def nb_kl_loss(disp, mu, log_var, scale_factor=1.0, alpha=0.1, eta=1.0):
    kl = pure_kl_loss(mu, log_var)

    def nb(y_true, y_pred):
        nb_obj = NB(theta=disp, masking=False, scale_factor=scale_factor)
        return eta * nb_obj.loss(y_true, y_pred, mean=True) + alpha * kl(y_true, y_pred)

    nb.__name__ = 'nb_kl'
    return nb


def nb_loss(disp, scale_factor=1.0, eta=1.0):
    def nb(y_true, y_pred):
        nb_obj = NB(theta=disp, masking=False, scale_factor=scale_factor)
        return eta * nb_obj.loss(y_true, y_pred, mean=True)

    nb.__name__ = 'nb'
    return nb


def zinb_kl_loss(pi, disp, mu, log_var, ridge=0.1, alpha=0.1, eta=1.0):
    kl = pure_kl_loss(mu, log_var)

    def zinb(y_true, y_pred):
        zinb_obj = ZINB(pi, theta=disp, ridge_lambda=ridge)
        return eta * zinb_obj.loss(y_true, y_pred) + alpha * kl(y_true, y_pred)

    zinb.__name__ = 'zinb_kl'
    return zinb


def zinb_loss(pi, disp, ridge=0.1, eta=1.0):
    def zinb(y_true, y_pred):
        zinb_obj = ZINB(pi, theta=disp, ridge_lambda=ridge)
        return eta * zinb_obj.loss(y_true, y_pred)

    zinb.__name__ = 'zinb'
    return zinb


LOSSES = {
    "mse": kl_recon_mse,
    "sse": kl_recon_sse,
    "mmd": mmd,
    "nb": nb_kl_loss,
    "zinb": zinb_kl_loss,
    "kl": pure_kl_loss,
    "sse_recon": sse_loss,
    "mse_recon": mse_loss,
    "nb_wo_kl": nb_loss,
    "zinb_wo_kl": zinb_loss,
}
