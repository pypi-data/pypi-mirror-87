import numpy as np
import sys

from . import mixing as mx


class SimpleModel():
    def __init__(self, uniform=False):
        self.num_strata = 3
        self.population = np.array([1_000_000, 1_500_000, 500_000])
        # NOTE: each row is the distribution of secondary infections across
        # the population strata that arise from individuals in a single
        # stratum.
        if uniform:
            self.mixing = np.eye(3)
        else:
            self.mixing = np.array([
                [0.9, 0.1, 0.0],
                [0.2, 0.6, 0.2],
                [0.3, 0.3, 0.4]
            ])

    def dtype(self):
        strata_shape = (self.num_strata, )
        return np.dtype([
            ('S', np.float, strata_shape),
            ('E', np.float, strata_shape),
            ('I', np.float, strata_shape),
            ('R', np.float, strata_shape),
            ('beta', np.float),
            ('gamma', np.float),
            ('sigma', np.float),
        ])

    def init(self, svec):
        exps = np.array([1, 1.5, 0.5])
        svec['E'] = exps
        svec['S'] = self.population - exps
        svec['beta'] = 0.7
        svec['gamma'] = 0.5
        svec['sigma'] = 0.5

    def step(self, prev, curr, t, dt):
        frac_susc = prev['S'] / self.population
        beta_i = prev['beta'] * prev['I']
        new_E = dt * mx.force_of_infection(beta_i, self.mixing) * frac_susc
        new_I = dt * prev['gamma'] * prev['E']
        new_R = dt * prev['sigma'] * prev['I']
        curr['S'] = prev['S'] - new_E
        curr['E'] = prev['E'] + new_E - new_I
        curr['I'] = prev['I'] + new_I - new_R
        curr['R'] = prev['R'] + new_R
        curr['beta'] = prev['beta']
        curr['gamma'] = prev['gamma']
        curr['sigma'] = prev['sigma']


def run_simple_model(f, uniform):
    model = SimpleModel(uniform=uniform)
    dtype = model.dtype()
    num_days = 250
    steps_per_day = 20
    dt = 1 / steps_per_day
    num_steps = num_days * steps_per_day
    hist = np.zeros((num_steps + 1, ), dtype=dtype)
    model.init(hist[0])
    print('t Ia Ib Ic Ra Rb Rc', file=f)
    print('0 {} {}'.format(
        ' '.join(str(v) for v in hist['I'][0]),
        ' '.join(str(v) for v in hist['R'][0])),
          file=f)
    for prev_ix in range(num_steps):
        t = (prev_ix + 1) / steps_per_day
        model.step(hist[prev_ix], hist[prev_ix + 1], t, dt)
        if (prev_ix + 1) % steps_per_day == 0:
            t = (prev_ix + 1) / steps_per_day
            print('{} {} {}'.format(
                t,
                ' '.join(str(v) for v in hist['I'][prev_ix + 1]),
                ' '.join(str(v) for v in hist['R'][prev_ix + 1])),
                  file=f)
    return hist


# https://numpy.org/doc/stable/user/basics.broadcasting.html
#
# When operating on two arrays, NumPy compares their shapes element-wise.
# It starts with the trailing dimensions and works its way forward.
# Two dimensions are compatible when:
#
# 1. they are equal, or
# 2. one of them is 1
#
# Arrays do not need to have the same number of dimensions.
#
# Regarding matrix multiplication (numpy.matmul, @):
#
# https://numpy.org/doc/stable/reference/generated/numpy.matmul.html
#
# 1. If both arguments are 2-D they are multiplied like conventional matrices.
#
# 2. If either argument is N-D, N > 2, it is treated as a stack of matrices residing in the last two indexes and broadcast accordingly.
#
# 3. If the first argument is 1-D, it is promoted to a matrix by prepending a 1 to its dimensions. After matrix multiplication the prepended 1 is removed.
#
# 4. If the second argument is 1-D, it is promoted to a matrix by appending a 1 to its dimensions. After matrix multiplication the appended 1 is removed.
#
class SimpleVecModel():
    def __init__(self, uniform=False):
        self.num_strata = 3
        self.population = np.array([1_000_000, 1_500_000, 500_000])
        # NOTE: each row is the distribution of secondary infections across
        # the population strata that arise from individuals in a single
        # stratum.
        if uniform:
            self.mixing = np.eye(3)
        else:
            self.mixing = np.array([
                [0.9, 0.1, 0.0],
                [0.2, 0.6, 0.2],
                [0.3, 0.3, 0.4]
            ])

    def dtype(self):
        strata_shape = (self.num_strata, )
        return np.dtype([
            ('S', np.float, strata_shape),
            ('E', np.float, strata_shape),
            ('I', np.float, strata_shape),
            ('R', np.float, strata_shape),
            ('beta', np.float),
            ('gamma', np.float),
            ('sigma', np.float),
        ])

    def init(self, svec):
        exps = np.array([1, 1.5, 0.5])
        svec['E'][:] = exps
        svec['S'][:] = self.population - exps
        # svec['beta'][:] = 0.7
        svec['beta'][:] = np.array([0.7, 0.75])
        svec['gamma'][:] = 0.5
        svec['sigma'][:] = 0.5

    def step(self, prev, curr, t, dt):
        frac_susc = prev['S'] / self.population
        beta_i = prev['beta'][:, None] * prev['I']
        # See notes about numpy.matmul, above.
        # TODO: how to ensure this always has desired shape/result?
        new_E = dt * mx.force_of_infection(beta_i, self.mixing) * frac_susc
        new_I = dt * prev['gamma'][:, None] * prev['E']
        new_R = dt * prev['sigma'][:, None] * prev['I']
        curr['S'] = prev['S'] - new_E
        curr['E'] = prev['E'] + new_E - new_I
        curr['I'] = prev['I'] + new_I - new_R
        curr['R'] = prev['R'] + new_R
        curr['beta'] = prev['beta']
        curr['gamma'] = prev['gamma']
        curr['sigma'] = prev['sigma']


def run_simple_vec_model(f, uniform):
    model = SimpleVecModel(uniform=uniform)
    dtype = model.dtype()
    num_days = 250
    steps_per_day = 20
    dt = 1 / steps_per_day
    num_steps = num_days * steps_per_day
    num_vec = 2
    hist = np.zeros((num_steps + 1, num_vec), dtype=dtype)
    model.init(hist[0])
    vec_ix = 1
    print('t Ia Ib Ic Ra Rb Rc', file=f)
    print('0 {} {}'.format(
        ' '.join(str(v) for v in hist['I'][0, vec_ix]),
        ' '.join(str(v) for v in hist['R'][0, vec_ix])),
          file=f)
    for prev_ix in range(num_steps):
        t = (prev_ix + 1) / steps_per_day
        model.step(hist[prev_ix], hist[prev_ix + 1], t, dt)
        if (prev_ix + 1) % steps_per_day == 0:
            t = (prev_ix + 1) / steps_per_day
            print('{} {} {}'.format(
                t,
                ' '.join(str(v) for v in hist['I'][prev_ix + 1, vec_ix]),
                ' '.join(str(v) for v in hist['R'][prev_ix + 1, vec_ix])),
                  file=f)
    return hist


def main(args=None):
    # TODO: open one file with 'w', write header, and run each
    # set of simulations in turn, each marked with a unique tag/ID.
    with open('simple_unif.ssv', 'w') as f:
        hist_base_unif = run_simple_model(f, uniform=True)

    with open('simple_nonunif.ssv', 'w') as f:
        hist_base = run_simple_model(f, uniform=False)

    with open('simple_vec.ssv', 'w') as f:
        hist_vec = run_simple_vec_model(f, uniform=False)

    # TODO: see ~/work/projects/dh-2018-vaccine-contract/pandemic-vaccination/discrete_rhs.m

    print(hist_base.shape)
    print(hist_vec[:, 0].shape)
    print(hist_base_unif.shape == hist_vec[:, 0].shape)
    print(hist_base.shape == hist_vec[:, 0].shape)
    for field in hist_base.dtype.fields.keys():
        print('{}: {}'.format(
            field,
            np.allclose(hist_base[field], hist_vec[field][:, 0])
        ))

    return 0


if __name__ == "__main__":
    sys.exit(main())
