# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

import brainpy as bp
import brainpy.numpy as np


def define_LIF(tau=10., Vr=0., Vth=10., noise=0., ref=0.):
    """Leaky integrate-and-fire neuron model.

    Parameters
    ----------
    tau : float
        Membrane time constants.
    Vr : float
        The reset potential.
    Vth : float
        The spike threshold.
    noise : float, callable
        The noise item.
    ref : float
        The refractory period.
    """

    ST = bp.types.NeuState(
        {'V': 0, 'sp_t': -1e7, 'sp': 0., 'inp': 0.},
    )

    @bp.integrate
    def int_f(V, t, Isyn):
        return (-V + Vr + Isyn) / tau, noise / tau

    def update(ST, _t_):
        if _t_ - ST['sp_t'] > ref:
            V = int_f(ST['V'], _t_, ST['inp'])
            if V >= Vth:
                V = Vr
                ST['sp_t'] = _t_
                ST['sp'] = True
            ST['V'] = V
        else:
            ST['sp'] = False
        ST['inp'] = 0.

    return bp.NeuType(name='LIF', requires=dict(ST=ST), steps=update, vector_based=False)


if __name__ == '__main__':
    bp.profile.set(backend='numba', dt=0.02, merge_steps=True)

    LIF = define_LIF(noise=1.)

    neu = bp.NeuGroup(LIF, geometry=(10,), monitors=['sp', 'V'])
    neu.pars['Vr'] = np.random.randint(0, 2, size=(10,))
    neu.pars['tau'] = np.random.randint(5, 10, size=(10,))
    neu.run(duration=100., inputs=['ST.inp', 13.], report=True)

    fig, gs = bp.visualize.get_figure(1, 1, 4, 8)

    fig.add_subplot(gs[0, 0])
    plt.plot(neu.mon.ts, neu.mon.V[:, 0], label=f'N-0 (tau={neu.pars.get("tau")[0]})')
    plt.plot(neu.mon.ts, neu.mon.V[:, 2], label=f'N-2 (tau={neu.pars.get("tau")[2]})')
    plt.ylabel('Membrane potential')
    plt.xlim(- 0.1, 100.1)
    plt.legend()
    plt.xlabel('Time (ms)')

    plt.show()
