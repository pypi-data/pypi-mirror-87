# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.5.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Explore the connectivity for efficient synapse computation

# + pycharm={"name": "#%%\n"}
import time
import numpy as np
import numba as nb

import sys
sys.path.append('../../')

import brainpy as bp


# + pycharm={"name": "#%%\n"}
def run(f, num=10, *args):
    t0 = time.time()
    for _ in range(num):
        f(*args)
    t1 = time.time()
    return t1 - t0


# -

# Let's first generate the connection between two neuron groups.

# + pycharm={"name": "#%%\n"}
N = pre_num = post_num = 5000
pre_indexes, post_indexes, pre_anchors = nn.connect.fixed_prob(N, N, 0.1)
conn_mat = np.zeros((N, N))
conn_mat[pre_indexes, post_indexes] = 1.

pre_spike = np.zeros(N)
spike_idx = np.random.randint(0, N, 1000)
pre_spike[spike_idx] = 1.


# -

# ## Method 1

# The first method is to use `np.dot` to compute spike numbers for each post-synaptic neuron.

# + pycharm={"name": "#%%\n"}
def np_syn1(pre_spike, conn_mat):
    return np.dot(pre_spike, conn_mat)


# + pycharm={"name": "#%%\n"}
@nb.njit
def nb_syn1(pre_spike, conn_mat):
    return np.dot(pre_spike, conn_mat)


# + pycharm={"name": "#%%\n"}
run_num = 1000
# time_np_syn1 = run(np_syn1, run_num, pre_spike, conn_mat)
# print('np_syn1 : {} s'.format(time_np_syn1))
# time_nb_syn1 = run(nb_syn1, run_num, pre_spike, conn_mat)
# print('nb_syn1 : {} s'.format(time_nb_syn1))


# -

# The advantage of this method is that it can use the auto-parallelism of `np.dot` method. 
# However, when the `pre_spike` is highly sparse, or, none of pre-synaptic neuron produces spike,
# this method will waste too much time to compute useless and trivial results.The complexity of 
# this method is O(`pre_num`) * O(`pre_num`) * O(`post_num`).

# ## Method 2

# The second method is to use `dict` data structure to accommodate the correspondence between 
# pre-synaptic neurons and post-synaptic neurons. This method is intutive, becanse whenever you
# want to get the `post-synaptic neuron indeces`, you can directly call `pre2post_dict[pre_idx]`.
#
# So, let's first generate the corresponding data structure.

# + pycharm={"name": "#%%\n"}
def correspondence(num_pre, num_post, i, j):
    assert len(i) == len(j)
    pre_indexes = {i_: [] for i_ in range(num_pre)}
    post_indexes = {j_: [] for j_ in range(num_post)}
    for index, i_ in enumerate(i):
        i_ = i_
        j_ = j[index]
        pre_indexes[i_].append(index)
        post_indexes[j_].append(index)
    return pre_indexes, post_indexes


# + pycharm={"name": "#%%\n"}
pre2syn, post2syn = correspondence(N, N, pre_indexes, post_indexes)
pre2syn = [v for _, v in sorted(pre2syn.items())]
post2syn = [v for _, v in sorted(post2syn.items())]


# + pycharm={"name": "#%%\n"}
def np_syn2():
    syn_val = np.zeros((len(post_indexes),))
    for i_ in spike_idx:
        syn_val[pre2syn[i_]] = 1.
    post_val = np.zeros(N)
    for i, j_ in enumerate(post2syn):
        post_val[i] = np.sum(syn_val[j_])


# + pycharm={"name": "#%%\n"}
# time_np_syn2 = run(np_syn2, run_num // 10)
# print('np_syn2 : {} s'.format(time_np_syn2))
# -

# As you can see, this method is higly computation ineffective. More importantly, this method cannot be accelerated by `Numba` technology, for `dict` is not well supported in `Numba`.

# ## Method 3

# The third method is use `tuple` or `list` structure to accommodate the correspondence 
# between pre-synaptic neurons and post-synaptic neurons.
#
# For `pre2post` object, the first position `pre2post[0]` retrives the post-synaptic neurons 
# connected with pre-neuron 0.
#
# Similarly, `post2pre` object contains the pre-synaptic neuron indices corresponding to the 
# post-synaptic neurons. Get the pre-neurons connectd to post-neuron `x`, you can directly 
# call `post2pre[x]`.

# + pycharm={"name": "#%%\n"}
pre2post = [np.where(conn_mat[i] > 0.)[0] for i in range(N)]
post2pre = [np.where(conn_mat[:, i] > 0.)[0] for i in range(N)]


# + pycharm={"name": "#%%\n"}
def np_syn3(post_num, pre_spike, post2pre):
    post_val = np.zeros(post_num)
    for i in range(post_num):
        post_val[i] = np.sum(pre_spike[post2pre[i]])
    return post_val


# + pycharm={"name": "#%%\n"}
# time_np_syn3 = run(np_syn3, run_num, post_num, pre_spike, post2pre)
# print('np_syn3 : {} s'.format(time_np_syn3))


# -

# In general terms, this kind of data structure can be highly effective. However, when the user 
# greedily interates `post_num`, too much time will be wasted on the neurons which do not produce 
# spikes. So, this method is not a good choice. 

# ## Method 4

# Instead of grid-search the post-synpatic neurons, we use the pre-synpatic neuron which produce spikes.
# When one neuron produces a spike, we retrive its connected post-synaptic neurons, and add a spike-induced
# value to the post-neurons. 

# + pycharm={"name": "#%%\n"}
def np_syn4(post_num, pre_spike, pre2post):
    post_val = np.zeros(post_num)
    spike_idx = np.where(pre_spike > 0)[0]
    for i in spike_idx:
        post_idx = pre2post[i]
        post_val[post_idx] += 1
    return post_val


# + pycharm={"name": "#%%\n"}
time_np_syn4 = run(np_syn4, run_num, post_num, pre_spike, pre2post)
print('np_syn4 : {} s'.format(time_np_syn4))
# -

# As you can see, this method is highly efficient for synapse computation. 
#
# However, its problem is the data structure of `pre2post` or `post2pre` is hard
# to be compiled by Numba. As you can see in the follows:

pre2post_nb = nb.typed.List()
for l in pre2post:
    if len(l):
        pre2post_nb.append(nb.typed.List(l))
    else:
        pre2post_nb.append(nb.typed.List.empty_list(nb.types.int64))


# + pycharm={"name": "#%%\n"}
@nb.njit
def nb_syn4(post_num, pre_spike, pre2post):
    post_val = np.zeros(post_num)
    spike_idx = np.where(pre_spike > 0)[0]
    for i in spike_idx:
        post_idx = pre2post[i]
        for j in post_idx:
            post_val[j] += 1
    return post_val


# -

time_nb_syn4 = run(nb_syn4, run_num, post_num, pre_spike, pre2post_nb)
print('nb_syn4 : {} s'.format(time_nb_syn4))

time_nb_syn4 = run(nb_syn4, run_num, post_num, pre_spike, pre2post_nb)
print('nb_syn4 again : {} s'.format(time_nb_syn4))


# ## Method 5

# An alternative way is to use `numpy array` to wrap the pre2post or post2pre correspondence.
# For example, 1-D array `pre_indexes` presents the connected pre-synaptic neurons, 
# 1-D array `post_indexes` denotes the connected post-synaptic neurons. This means
# `(pre_indexes[x], post_indexes[x])` is a pair of connected neurons. 
# In order to conveniently get post-indices by a pre-synaptic id, we can also contruct a 2-D 
# array `pre_anchors` with the dimension of `(2, num_pre)`. `num_pre` is the number of the 
# pre-synaptic neurons, and `2` is the `start` and the `end` positions in the `post_indexes`. 
# `idx = pre_anchors[x]` extracts the start and end position of `post_indexes`.
#
# Let's see our experimental results:

# + pycharm={"name": "#%%\n"}
def np_syn5(post_num, pre_spike, post_indexes, pre_anchors):
    post_val = np.zeros(post_num)
    spike_idx = np.where(pre_spike > 0)[0]
    for i_ in spike_idx:
        index = pre_anchors[:, i_]
        post_idx = post_indexes[index[0]: index[1]]
        post_val[post_idx] += 1
    return post_val


# -

# time_np_syn5 = run(np_syn5, run_num, post_num, pre_spike, post_indexes, pre_anchors)
# print('np_syn5 : {} s'.format(time_np_syn5))


def np_syn5_2(post_num, pre_spike, post_indexes, pre_anchors):
    post_val = np.zeros(post_num)
    spike_idx = np.where(pre_spike > 0)[0]
    for i_ in spike_idx:
        start, end = pre_anchors[:, i_]
        post_idx = post_indexes[start: end]
        post_val[post_idx] += 1
    return post_val


# time_np_syn5_2 = run(np_syn5_2, run_num, post_num, pre_spike, post_indexes, pre_anchors)
# print('np_syn5_2 : {} s'.format(time_np_syn5_2))


# + pycharm={"name": "#%%\n"}
@nb.njit
def nb_syn5(post_num, pre_spike, post_indexes, pre_anchors):
    post_val = np.zeros(post_num)
    spike_idx = np.where(pre_spike > 0)[0]
    for i_ in spike_idx:
        index = pre_anchors[:, i_]
        post_idx = post_indexes[index[0]: index[1]]
        post_val[post_idx] += 1
    return post_val


# + pycharm={"name": "#%%\n"}
# time_nb_syn5 = run(nb_syn5, run_num, post_num, pre_spike, post_indexes, pre_anchors)
# print('nb_syn5 : {} s'.format(time_nb_syn5))


# -

# As you can see, the kind of synaptic data sturcture is highly efficient. Most importantly, 
# it can be accelerated by Numba.

# ## Systermatic comparison

# Finnaly, let's synatermically compare the different synaptic data structures under 
# the different number of pre-synaptic spikes.

# + pycharm={"name": "#%%\n"}
def single_run(num_spike_neuron, pre_num=5000, post_num=5000):
    pre_indexes, post_indexes, pre_anchors = nn.conn.fixed_prob(pre_num, post_num, 0.1)
    conn_mat = np.zeros((pre_num, post_num))
    conn_mat[pre_indexes, post_indexes] = 1.
    
    pre2post = [np.where(conn_mat[i] > 0.)[0] for i in range(N)]
    post2pre = [np.where(conn_mat[:, i] > 0.)[0] for i in range(N)]

    pre_spike = np.zeros(pre_num)
    spike_idx = list(range(num_spike_neuron))
    pre_spike[spike_idx] = 1.
    
    time_np_syn1 = run(np_syn1, run_num, pre_spike, conn_mat)
    time_nb_syn1 = run(nb_syn1, run_num, pre_spike, conn_mat)
    time_np_syn3 = run(np_syn3, run_num, post_num, pre_spike, post2pre)
    time_np_syn4 = run(np_syn4, run_num, post_num, pre_spike, pre2post)
    time_np_syn5 = run(np_syn5, run_num, post_num, pre_spike, post_indexes, pre_anchors)
    time_nb_syn5 = run(nb_syn5, run_num, post_num, pre_spike, post_indexes, pre_anchors)
    
    return time_np_syn1, time_nb_syn1, time_np_syn3, time_np_syn4, time_np_syn5, time_nb_syn5


# + pycharm={"name": "#%%\n"}
import matplotlib.pyplot as plt

# + pycharm={"name": "#%%\n"}
# all_num_pre_spike = list(range(0, 5000+1, 200))
# all_np_syn1 = []
# all_nb_syn1 = []
# all_np_syn3 = []
# all_np_syn4 = []
# all_np_syn5 = []
# all_nb_syn5 = []
# for num in all_num_pre_spike:
#     res = single_run(num)
#     all_np_syn1.append(res[0])
#     all_nb_syn1.append(res[1])
#     all_np_syn3.append(res[2])
#     all_np_syn4.append(res[3])
#     all_np_syn5.append(res[4])
#     all_nb_syn5.append(res[5])
#
# plt.figure(figsize=(14, 6))
# plt.plot(all_num_pre_spike, all_np_syn1, label='np_syn1')
# plt.plot(all_num_pre_spike, all_nb_syn1, label='nb_syn1')
# plt.plot(all_num_pre_spike, all_np_syn3, label='np_syn3')
# plt.plot(all_num_pre_spike, all_np_syn4, label='np_syn4')
# plt.plot(all_num_pre_spike, all_np_syn5, label='np_syn5')
# plt.plot(all_num_pre_spike, all_nb_syn5, label='nb_syn5')
# plt.legend()
# plt.ylabel('Time (s)')
# plt.xlabel('Number of pre-synaptic spikes')
# plt.tight_layout()
# plt.show()
# -


