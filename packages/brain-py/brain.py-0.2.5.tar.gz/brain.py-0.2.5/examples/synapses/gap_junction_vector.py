# -*- coding: utf-8 -*-

import brainpy as bp
import brainpy.numpy as np


def define_gap_junction(weight):
    requires = dict(
        ST=bp.types.SynState([]),
        pre=bp.types.NeuState(['V']),
        post=bp.types.NeuState(['V', 'input']),
        post2syn=bp.types.ListConn(help='post-to-synapse connection.'),
        pre_ids=bp.types.Array(dim=1, help='Pre-synaptic neuron indices.'),
    )

    def update(ST, pre, post, post2pre):
        num_post = len(post2pre)
        for post_id in range(num_post):
            pre_ids = post2pre[post_id]
            post['input'][post_id] += weight * np.sum(pre['V'][pre_ids] - post['V'][post_id])

    return bp.SynType(name='GapJunction', requires=requires, steps=update, vector_based=True)


def define_lif_gap_junction(weight, k_spikelet=0.1, post_has_refractory=False):
    requires = dict(
        ST=bp.types.SynState(['spikelet']),
        pre=bp.types.NeuState(['V', 'spike']),
        post2syn=bp.types.ListConn(help='post-to-synapse connection.'),
        pre_ids=bp.types.Array(dim=1, help='Pre-synaptic neuron indices.'),
    )

    if post_has_refractory:
        requires['post'] = bp.types.NeuState(['V', 'input', 'refractory'])

        def update(ST, pre, post, pre2post):
            num_pre = len(pre2post)
            g_post = np.zeros_like(post['V'], dtype=np.float_)
            spikelet = np.zeros_like(post['V'], dtype=np.float_)
            for pre_id in range(num_pre):
                post_ids = pre2post[pre_id]
                pre_V = pre['V'][pre_id]
                g_post[post_ids] = weight * np.sum(pre_V - post['V'][post_ids])
                if pre['spike'][pre_id] > 0.:
                    spikelet[post_ids] += weight * k_spikelet * pre_V
            post['V'] += spikelet * (1. - post['refractory'])
            post['input'] += g_post
    else:
        requires['post'] = bp.types.NeuState(['V', 'input'])

        def update(ST, pre, post, pre2post):
            num_pre = len(pre2post)
            g_post = np.zeros_like(post['V'], dtype=np.float_)
            spikelet = np.zeros_like(post['V'], dtype=np.float_)
            for pre_id in range(num_pre):
                post_ids = pre2post[pre_id]
                pre_V = pre['V'][pre_id]
                g_post[post_ids] = weight * np.sum(pre_V - post['V'][post_ids])
                if pre['spike'][pre_id] > 0.:
                    spikelet[post_ids] += weight * k_spikelet * pre_V
            post['V'] += spikelet
            post['input'] += g_post

    return bp.SynType(name='GapJunctin_for_LIF',
                      requires=requires,
                      steps=update,
                      vector_based=True)
