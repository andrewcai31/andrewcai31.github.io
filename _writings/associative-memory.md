---
layout: writing
title: "some notes on an associative memory lecture"
date: 2025-07-14
---

from the ICML associative memory tutorial:

associative memory is association (brain sees amogus brain understand what it’s associated with) + memory (brain sees amogus brain thinks of among us) + error correction (brain sees amogus without legs brain thinks about amogus with legs).

these three ideas are unified via energy minimization: a query with missing/noisy data converges towards some minima in the energy landscape.

terminology:

- local minima: memories
- non-linear energy descent dynamics: memory recall
- process of dynamics between t=0 and convergence: association

hopfield networks: with dynamical neurons ($\pm 1$) $\sigma_i$ and memorized binary pattern vectors $\xi^\mu$,

$$
E = -\sum_{i, j = 1}^D \sigma_iT_{ij}\sigma_j \textrm{  where  } T_{ij} = \sum_{\mu = 1}^K \xi_i^\mu \xi_j^\mu
$$

we have that $K^\textrm{max} \approx 0.14D$ where $D$ is param count, so scaling laws kill you — capacity is tiny.

dense associative memory:

$$
E = -\sum_{i_1, \ldots, i_n}^D T_{i_1, \ldots, i_n} \sigma_{i_1}\cdots\sigma_{i_n} \textrm{ where } T_{i_1, \ldots, i_n} = \sum_{\mu = 1}^K \xi_{i_1}^\mu \cdots \xi_{i_n}^\mu
$$

In fact, we can represent $E = -\displaystyle\sum_{\mu=1}^K F\left(\displaystyle\sum_{i=1}^n \xi_i^\mu \sigma_i\right)$ where $F(x) = x^n$. In the hopfield network case, $n = 2$.

now, $K^\textrm{max} \approx 2^{\frac{D}{2}}$ for the right energy functions.

let’s talk about the energy descent update rule.

- for each neuron on the $t+1$th iteration, we clamp the other neurons’ values to their $t$th iteration and then find which value lowers the energy
- this is equivalent to finding the sign of the difference of the two energies (derivative of $F$, which we’ll denote as $f$), or
    
    $$
    \sigma_i^{(t+1)} = \textrm{Sign}\left[\sum_{\mu=1}^K \xi_i^\mu f\left( \sum_{j \neq i}^D \xi_j^\mu \sigma_j^{(t)}\right)\right]
    $$
    

now let’s examine why dense associative memory can store so many memories (compared to hopfield networks)!:

- take $\xi^\mu$ as $\pm 1$ vectors with 50% probability. Then, let’s figure out how many memories we can store by finding the number of local minima possible — so the update would be constant. initialize $\sigma_i^{(0)} = \xi_i^1$, then we want to find the probability that
    
    
    $$\sigma_i^{(t+1)} = \textrm{Sign} \left[\xi_i^1 f(D-1) + \sum_{\mu = 2}^K \xi_i^\mu f\left(\sum_{j \neq i} ^D \xi_j^\mu \xi_j^1\right)\right] = \xi_i^1$$
    
- The former term in the sign function can be denoted as the signal, while the latter can be denoted as the noise. This is equivalent to finding the probability that the noise is greater than $f(D-1)$, which (for error bound $\alpha$ sd’s) is 
$$K^\textrm{max} = \frac{1}{\alpha^2 (2n-3)!!} D^{n-1}$$. Hence, since $D$ is large, $K^\textrm{max}$ increases significantly with $n$ (that’s why Hopfield networks have low capacity)

first q & a:

- associative memory vs. hamming distance retrieval: sometimes you want to examine the energy landscape
- sparse hopfield networks: we want to train general memories, instead of picking special engineered memories so that $T$ is sparse

many variants of energy-based AM:

- classical hopfield network (1984)
- dense associative memory (2016)
- hierarchical associative memory (2021)
- energy transformer (2023)
- neuron-astrocyte networks (2023)

first, from continuous to binary:

- sign is basically just tanh as $\beta \rightarrow \infty$, let’s denote the neural activations $\hat{x} = \tanh(\beta x)$.
- binary states use energy flips (previous update rule), while continuous states use diffeq’s
- all traditional activation functions are monotonically increasing, so there exists a Lagrangian $\mathcal{L}(x)$ whose gradient is $\hat{x}$
- consider the energy term as the legendre transform of the lagrangian $\mathcal{T}[\mathcal{L}_x] = \langle x, \hat{x} \rangle -\mathcal{L}_x(x)$. Thus, $x$ and $\hat{x}$ evolve together to minimize energy.

necessary properties of associative memory:

- energy function is continuous and bounded from below
- dynamics via gradient flow never increase energy
- bounded energy implies convergence

we have the problems of adding hierarchy:

- multiple nonlinearities
- arbitrarily complex parameterizations (convolution, attention layers)
- scaling (not just retrieving vectors)

here’s the solution, the HAMUX framework:

![HAMUX framework diagram](/assets/images/hamux-framework.png)

let’s build networks using HAMUX:

1. continuous hopfield networks: there’s one dynamic state vector (with energy $E_x$) and one matrix of stored patterns (synapse with energy $E_\textrm{syn}$), with total energy the sum of the two components. Then, activations $\hat{x_i}$ is just tanh, and $E_\textrm{syn}$ as the sum over the squared dot products.
2. dense associative memory: similarly, one dynamic state vector and one matrix of stored pattern. activations are the same. but now $E_\textrm{syn}$ uses ReLU on top of the $n$th power of the dot products.
3. biologically plausible denseAM: $n > 2$ is not biologically probable, so add the notion of hidden neurons $h_\mu$ and pairwise interaction energy that uses $\hat{h}_\mu \xi^\mu_i \hat{x}_i$

now, the energy transformer! we can derive this in the HAMUX framework:

- dynamic state is tokens $x$
- activation is $\hat{x} = \textrm{LayerNorm}(x)$
- computing energy scalar on top of tokens
    - attention energy is integral of softmax of attention scores (?)
    - MLP energy is a classical hopfield network
- notes!
    - attention and MLP are in parallel
    - shared weights through “layers”
    - residual stream uses pre-activations
- interpretable by design:
    - visualize $\Xi$, the synaptic weight matrix — since memory is associative it’s very interpretable through patches
    - ET can assemble patches of memories together

i kinda lost the plot after this, i have some other notes but i don't understand them well enough to add them here.