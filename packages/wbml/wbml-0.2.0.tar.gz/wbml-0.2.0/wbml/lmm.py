import logging

from lab import B
from matrix import Diagonal, LowRank
from plum import Dispatcher, Referentiable, Self
from stheno import Measure, GP, Delta, FixedDelta, Normal, Obs, AbstractObservations

from .util import normal1d_logpdf, BatchVars

__all__ = ["LMMPP", "OLMM", "VaryingNet", "VOLMM"]

log = logging.getLogger(__name__)


def _to_tuples(x, y):
    """Extract tuples with the input locations, output index,
    and observations from a matrix of observations.

    Args:
        x (tensor): Input locations.
        y (tensor): Outputs.

    Returns:
        list[tuple]: List of tuples with the input locations, output index,
            and observations.
    """
    xys = []
    for i in range(B.shape(y)[1]):
        mask = ~B.isnan(y[:, i])
        if B.any(mask):
            xys.append((x[mask], i, y[mask, i]))

    # Ensure that any data was extracted.
    if len(xys) == 0:
        raise ValueError("No data was extracted.")

    return xys


class LMMPP(metaclass=Referentiable):
    """PP implementation of the linear mixing model.

    Args:
        kernels (list[:class:`stheno.Kernel`]) Kernels.
        noise_obs (tensor): Observation noise. One.
        noises_latent (tensor): Latent noises. One per latent process.
        H (tensor): Mixing matrix.
    """

    _dispatch = Dispatcher(in_class=Self)

    @_dispatch(list, B.Numeric, B.Numeric, B.Numeric)
    def __init__(self, kernels, noise_obs, noises_latent, H):
        self.measure = Measure()
        p, m = B.shape(H)

        # Create latent processes.
        xs = [GP(k, measure=self.measure) for k in kernels]

        # Create latent noise.
        es = [GP(noise * Delta(), measure=self.measure) for noise in noises_latent]

        # Create noisy latent processes.
        xs_noisy = [x + e for x, e in zip(xs, es)]

        # Multiply with mixing matrix.
        self.fs = [0 for _ in range(p)]
        for i in range(p):
            for j in range(m):
                self.fs[i] += xs_noisy[j] * H[i, j]

        # Create two observed process.
        self.ys = [f + GP(noise_obs * Delta(), measure=self.measure) for f in self.fs]
        self.y = self.measure.cross(*self.ys)

    @_dispatch(Measure, list, list, GP)
    def __init__(self, Measure, fs, ys, y):
        self.measure = Measure
        self.fs = fs
        self.ys = ys
        self.y = y

    def condition(self, x, y):
        """Condition on data.

        Args:
            x (tensor): Input locations.
            y (tensor): Observed values.
        """
        post = self.measure | Obs(*[(self.ys[i](x), y) for x, i, y in _to_tuples(x, y)])
        return LMMPP(
            post, [post(p) for p in self.fs], [post(p) for p in self.ys], post(self.y)
        )

    def logpdf(self, x, y):
        """Compute the logpdf of data.

        Args:
            x (tensor): Input locations.
            y (tensor): Observed values.

        Returns:
            tensor: Logpdf of data.
        """
        obs = Obs(*[(self.ys[i](x), y) for x, i, y in _to_tuples(x, y)])
        return self.measure.logpdf(obs)

    def marginals(self, x):
        """Compute marginals.

        Args:
            x (tensor): Inputs to construct marginals at.

        Returns:
            tuple[tensor]: Marginals per output, spatial means per time, and
                spatial variance per time.
        """
        preds = [y(x).marginals() for y in self.ys]
        return preds, None, None

        means, vars = [], []
        for i in range(B.shape(x)[0]):
            d = self.y(x[i])
            means.append(d.mean)
            vars.append(d.var)
        return preds, means, vars

    def sample(self, x, latent=True):
        """Sample data.

        Args:
            x (tensor): Inputs to sample at.
            latent (bool, optional): Sample latent processes instead of the
                observed values. Defaults to `True`.
        """
        ps = self.fs if latent else self.ys
        samples = self.measure.sample(*[p(x) for p in ps])
        return B.concat(*samples, axis=1)


class OLMM(metaclass=Referentiable):
    """Orthogonal linear mixing model.

    Args:
        kernels (list[:class:`stheno.Kernel`]) Kernels.
        noise_obs (tensor): Observation noise. One.
        noises_latent (tensor): Latent noises. One per latent processes.
        H (tensor): Mixing matrix.
    """

    _dispatch = Dispatcher(in_class=Self)

    @_dispatch(list, B.Numeric, B.Numeric, B.Numeric, B.Numeric)
    def __init__(self, kernels, noise_obs, noises_latent, U, S_sqrt):
        # Determine number of outputs and latent processes.
        self.p, self.m = B.shape(U)

        # Save components of mixing matrix.
        self.U = U
        self.S_sqrt = S_sqrt

        # Save noises.
        self.noise_obs = noise_obs
        self.noises_latent = noises_latent

        # Compute projected noises.
        noises_projected = [
            noise_obs / self.S_sqrt[i] ** 2 + noises_latent[i] for i in range(self.m)
        ]

        # Construct single-output models.
        self.measures = [Measure() for _ in range(self.m)]
        self.xs = [GP(k, measure=m) for k, m in zip(kernels, self.measures)]
        self.xs_noises = [
            GP(Delta() * n, measure=m) for n, m in zip(noises_projected, self.measures)
        ]
        self.xs_noisy = [p + n for p, n in zip(self.xs, self.xs_noises)]

        # Construct mixing matrix and projection.
        self._construct_H_and_P()

    @_dispatch(list, B.Numeric, B.Numeric, B.Numeric)
    def __init__(self, kernels, noise_obs, noises_latent, H):
        U, S_sqrt, _ = B.svd(H)
        OLMM.__init__(self, kernels, noise_obs, noises_latent, U, S_sqrt)

    @_dispatch(list, list, list, list, B.Numeric, B.Numeric, B.Numeric, B.Numeric)
    def __init__(
        self, measures, xs, xs_noises, xs_noisy, noise_obs, noises_latent, U, S_sqrt
    ):
        # Save GPs.
        self.measures = measures
        self.xs = xs
        self.xs_noises = xs_noises
        self.xs_noisy = xs_noisy

        # Save noises.
        self.noise_obs = noise_obs
        self.noises_latent = noises_latent

        # Save components related to the mixing matrix.
        self.p, self.m = B.shape(U)
        self.U = U
        self.S_sqrt = S_sqrt

        self._construct_H_and_P()

    def _construct_H_and_P(self):
        """Construct mixing matrix and projection."""
        self.H = self.U * self.S_sqrt[None, :]
        self.P = B.transpose(self.H) / self.S_sqrt[:, None] ** 2

    def optimal_U(self, x, y):  # pragma: no cover
        """Approximate the optimal `U`.

        Args:
            x (tensor): Input locations.
            y (tensor): Observed values.
        """
        raise NotImplementedError()

    def project(self, y):
        """Project observations.

        Args:
            y (tensor): Data to project.

        Returns:
            list[tensor]: Projected observations per output.
        """
        return B.unstack(B.matmul(self.P, y, tr_b=True), axis=0)

    @property
    def lik_var(self):
        """Variance of the likelihood."""
        noise_latent = LowRank(self.H * self.noises_latent[None, :] ** 0.5)
        noise_obs = Diagonal(self.noise_obs * B.ones(B.dtype(self.noise_obs), self.p))
        return noise_latent + noise_obs

    def lik(self, y, mean=0):
        """Compute the likelihood of data for a given mean.

        Args:
            y (tensor): Data to evaluate likelihood at.
            mean (tensor): Mean of likelihood. Defaults to zero.

        Returns:
            tensor: Likelihood of `y` given `mean`.
        """
        return B.sum(Normal(self.lik_var).logpdf(B.transpose(y - mean)))

    @_dispatch(B.Numeric, B.Numeric)
    def condition(self, x, y):
        """Condition on data.

        Args:
            x (tensor): Inputs.
            y (tensor): Outputs.
        """
        ys = self.project(y)
        return self.condition(*[Obs(p(x), y) for p, y in zip(self.xs_noisy, ys)])

    @_dispatch([AbstractObservations])
    def condition(self, *obses):
        # Condition latent processes and noises.
        posts = [m | obs for m, obs in zip(self.measures, obses)]
        return OLMM(
            posts,
            [post(p) for p, post in zip(self.xs, posts)],
            [post(p) for p, post in zip(self.xs_noises, posts)],
            [post(p) for p, post in zip(self.xs_noisy, posts)],
            self.noise_obs,
            self.noises_latent,
            self.U,
            self.S_sqrt,
        )

    def logpdf(self, x, y):
        """Compute the logpdf.

        Args:
            x (tensor): Inputs of data.
            y (tensor): Output of data.

        Returns:
            tensor: Logpdf of data.
        """
        # Perform projection.
        ys_proj = self.project(y)

        # Add contributions of latent processes.
        lml = 0
        for p, n, yi in zip(self.xs_noisy, self.xs_noises, ys_proj):
            lml += p(x).logpdf(yi) - n(x).logpdf(yi)

        # Add regularisation contribution.
        lml += self.lik(y)

        return lml

    def marginals(self, x):
        """Compute marginals.

        Args:
            x (tensor): Inputs to construct marginals at.

        Returns:
            tuple[tensor]: Marginals per output, spatial means per time, and
                spatial variance per time.
        """

        # Extract means and variances of the latent processes.
        x_means, x_vars = zip(
            *[(p.mean(x)[:, 0], p.kernel.elwise(x)[:, 0]) for p in self.xs]
        )

        # Pull means through mixing matrix and scale back.
        x_means = B.stack(*x_means, axis=0)
        y_means = B.matmul(self.H, x_means)

        # Pull variances through mixing matrix and scale back.
        x_vars = B.stack(*x_vars, axis=0)
        y_vars = (
            B.matmul(self.H ** 2, x_vars + self.noises_latent[:, None]) + self.noise_obs
        )

        # Compose predictions.
        y_preds = [
            (mean, mean - 2 * var ** 0.5, mean + 2 * var ** 0.5)
            for mean, var in zip(y_means, y_vars)
        ]

        # Unstack to get spatial means.
        y_means_spatial = [mean[:, None] for mean in B.unstack(y_means, axis=1)]

        # Unstack to get spatial variances.
        obs_noise = B.eye(B.dtype(self.noise_obs), self.p) * self.noise_obs
        y_vars_spatial = [
            B.matmul(self.H * (var + self.noises_latent)[None, :], self.H, tr_b=True)
            + obs_noise
            for var in B.unstack(x_vars, axis=1)
        ]

        return y_preds, y_means_spatial, y_vars_spatial

    def sample(self, x, latent=True):
        """Sample model.

        Args:
            x (tensor): Points to sample at.
            latent (bool): Sample latent processes instead of observed values.
                Defaults to `True`.

        Returns:
            tensor: Sample.
        """
        ps = self.xs if latent else self.xs_noisy
        x_samples = B.concat(*[p(x).sample() for p in ps], axis=1)
        return B.matmul(x_samples, self.H, tr_b=True)


class VaryingNet:
    """A :class:`.net.Net` with weights that vary per observation.

    Args:
        net (:class:`.net.Net`): Net whose weights to vary.
    """

    def __init__(self, net):
        self.net = net
        self.output_size = net.layers[-1].width

    def num_weights(self, input_size):
        """Calculate the number of weights given an input size.

        Args:
            input_size (int): Size of the inputs.
        """
        return self.net.num_weights(input_size)

    def __call__(self, x, weights):
        x = B.uprank(x)
        m = B.shape(x)[1]

        # Construct the function from the given weights.
        vs = BatchVars(source=weights)
        self.net.initialise(m, vs)

        # Perform call.
        x = x[:, None, :]  # Insert input axis.
        y = self.net(x)
        y = y[:, 0, :]  # Remove input axis.

        return y


class VOLMM(metaclass=Referentiable):
    """Variational OLMM.

    Args:
        p_kernels (list[:class:`stheno.Kernel`]) Kernels of the prior.
        p_H (tensor): Mixing matrix of the prior.
        p_transform (function): Transform of the inputs and weights to the
            observed values without noise.
        p_noises_obs (tensor): Observation noises of the prior. One per output.
        p_olmm_noise_obs (tensor): Observation noise of the variational
            approximation. One.
        p_olmm_noises_latent (tensor): Latent noises of the variational
            approximation. One per latent process.
        q_x (tensor): Locations of the pseudo-observations of the variational
            approximation.
        q_y (tensor): Pseudo-observations of the variational approximation.
    """

    _dispatch = Dispatcher(in_class=Self)

    def __init__(
        self,
        p_kernels,
        p_H,
        p_transform,
        p_noises_obs,
        p_olmm_noise_obs,
        p_olmm_noises_latent,
        q_x,
        q_y,
        q_y_noises,
    ):
        # Construct OLMM prior.
        self.p_olmm = OLMM(p_kernels, p_olmm_noise_obs, p_olmm_noises_latent, p_H)

        # Likelihood parameters:
        self.p_transform = p_transform
        self.p_noises_obs = p_noises_obs

        # Variational parameters:
        self.q_x = q_x
        self.q_y = q_y
        self.q_y_noises = q_y_noises

    def _olmm_condition(self, olmm):
        obses = []
        for p, n, y in zip(
            olmm.xs, B.unstack(self.q_y_noises, axis=1), B.unstack(self.q_y, axis=1)
        ):
            e = GP(FixedDelta(n), graph=p.graph)
            obses.append(Obs((p + e)(self.q_x), y))
        return olmm.condition(*obses)

    def _olmm_logpdf(self, olmm):
        logpdf = 0
        for p, n, y in zip(
            olmm.xs, B.unstack(self.q_y_noises, axis=1), B.unstack(self.q_y, axis=1)
        ):
            e = GP(FixedDelta(n), graph=p.graph)
            logpdf += (p + e)(self.q_x).logpdf(y)
        return logpdf

    @_dispatch(B.Numeric)
    def sample(self, x, latent=True):
        """Sample from the model.

        Args:
            x (tensor): Locations to sample at.
            latent (bool): Sample from the latent function instead of the
                observed values.

        Returns:
            matrix: Sample.
        """
        # Sample weights and transform.
        q = self._olmm_condition(self.p_olmm)  # Approximate posterior.
        w_sample = q.sample(x, latent=False)
        sample = self.p_transform(x, w_sample)

        # Add noise if an observed sample should be returned.
        if not latent:
            sample = sample + self.p_noises_obs ** 0.5 * B.randn(sample)

        return w_sample, sample

    @_dispatch(B.Numeric, B.Numeric)
    def elbo(self, x, y):
        """Compute the ELBO.

        Args:
            x (tensor): Locations of the observations.
            y (tensor): Observations.
        Returns:
            scalar: ELBO.
        """
        # Compute pseudo-evidence.
        pseudo_evidence = self._olmm_logpdf(self.p_olmm)

        # Likelihood correction: add real likelihood.
        q = self._olmm_condition(self.p_olmm)  # Approximate posterior.
        w_sample = q.sample(x, latent=False)
        f_sample = self.p_transform(x, w_sample)
        # TODO: Fix the below.
        # TensorFlow's gradient computation does not play well with NaNs, so
        # we make a copy and set the NaNs to zero before computing the logpdfs.
        y_copy = y.copy()
        y_copy[B.isnan(y)] = 0
        logpdfs = B.flatten(normal1d_logpdf(y_copy - f_sample, self.p_noises_obs))
        available = ~B.isnan(B.flatten(y))
        taken = B.take(logpdfs, available)
        lik_corr = B.sum(taken)

        # Likelihood correction: subtract pseudo-likelihood.
        # TODO: Compute this analytically!
        w_sample = q.sample(self.q_x, latent=False)
        olmm = self.p_olmm.condition(self.q_x, w_sample)
        lik_corr -= self._olmm_logpdf(olmm)

        # Add together and divide by total number of observations.
        elbo = pseudo_evidence + lik_corr
        elbo /= B.sum(B.cast(B.dtype(elbo), available))

        return elbo
