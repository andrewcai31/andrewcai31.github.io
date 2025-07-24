---
layout: writing
title: "influence functions"
date: 2025-03-21
---

this was not written for others to read. it's just my summary of the anthropic influence functions paper.

Authors use influence functions on LLMs (from 810m up to 52b param. models) to analyze most influential sequence trends. On top of EK-FAC influence functions, they perform efficient evaluation by TF-IDF filtering for top 10k potential sequences, then performing query batching (must store either query gradients or sequence gradients in memory — since less queries, query gradients can be approximated as rank-32). Because EK-FAC assumes independence between different parameter matrices (per layer) and thus a block-diagonal $G$, influence of each datapoint can be attributed to specific layers. Token attribution can also be constructed by deconstructing the training gradient into a sum of terms per token. Authors confirm that EK-FAC parameter estimates closely resemble the PBRF. The authors find that influence scores typically follow a power law on the top 0.01% of scores (without TF-IDF filtering), and their distribution is highly sparse. Using these fitted power laws, authors estimate that scanning 5m sequences would result in a similar top-10 influence distribution as 10k TF-IDF sequences. They also find that larger models have most influential sequences that are similar in meaning, while smaller models have most influential sequences that are similar in tokens only. Furthermore, authors find cross-lingual influence of English training sequences in foreign-language queries (with similar content) increase as model size increases. Finally, they find that influences are spread evenly through layers. They find that outside of famous quotes, memorization does not occur on the most influential sequences, and that influence patterns are sensitive to word ordering (for all model sizes). They also find that role-playing behavior results from imitation of examples in training set, and descriptions of how types of agents behave.

Technical information on how EK-FAC influence functions are computed: If we assume the model is trained without a document sample $z$, the new optimal parameters can be identified as 

$$\theta_\epsilon = \arg\min_\theta (L(\theta) + \epsilon \ell(z, \theta))$$

with $\epsilon$ estimating the perturbation amount (eg. $\epsilon = -\frac{1}{n}$ corresponds to removing a single training point). Thus, the influence of $z$ on $z_\textrm{test}$ is measured the change in loss; equal to 

$$\ell(z_\textrm{test}, \theta_\epsilon) - \ell(z_\textrm{test}, \theta) \approx \nabla_\theta \ell(z_\textrm{test}, \theta)^T (\theta_\epsilon - \theta)$$

from a first-order Taylor expansion. We then desire to estimate $\theta_\epsilon - \theta$ given the stationary conditions $\nabla_\theta L(\theta) = 0$ and $\nabla_\theta L(\theta_\epsilon) + \epsilon \nabla_\theta \ell(z, \theta_\epsilon) = 0$. Using another first-order Taylor expansion gives 

$$H(\theta_\epsilon - \theta) + \epsilon \nabla_\theta \ell(z, \theta) = 0$$

where Hessian $H = \nabla_\theta^2 L(\theta)$, hence 

$$\theta_\epsilon - \theta = -\epsilon H^{-1} \nabla_\theta \ell(z, \theta)$$

However, assuming $N$ neurons in the model, computing the inverse of the Hessian requires $O(N^4)$ memory and $O(N^6)$ time, with $N^2$ total parameters as each dimension of the matrix. We want a quicker, low-memory method to estimate the product of $H^{-1}$ with $O(N^2)$-length vectors. First, assuming $\ell$ is log-likelihood, $\mathbb{E}[\nabla_\theta \ell(\theta)] = 0$, which we plug into the identity $\mathbb{E}[\nabla^2 g(X)] = \mathbb{V}[\nabla g(X)] + (\mathbb{E}[\nabla g(X)])^2$. Thus, $\mathbb{E}[H] = \mathbb{E}[F]$ for the observed Fisher information matrix 

$$F = \nabla_\theta\ell(z, \theta) \nabla_\theta \ell(z, \theta)^T$$

(which in this case is the variance), so we estimate $H \approx F$. Letting $a$ be the vector of input activations and $g$ be the vector of backpropagated gradients (each with length $N$) and $\textrm{vec}$ the function that reshapes a matrix as a vector, we have that $F = \textrm{vec}(ag^T)\textrm{vec}(ag^T)^T$ since the gradient of the loss at each layer is just the product of the input activations and the backpropagated gradients. By the Kronecker product identity $(C^T \otimes A) \textrm{vec}(B) = \textrm{vec}(ABC)$, we have that $\textrm{vec}(ag^T) = g \otimes a$, hence 

$$F = (gg^T) \otimes (aa^T) = G \otimes A$$

for unnormalized cov matrices $G$ and $A$ (corresponding to $g$ and $a$). Note that in practice, $G$ and $A$ are estimated using block-diagonal matrices, with the assumption that weights in different layers are uncorrelated. Using this formulation, we have that for vector $v$ it holds that $F^{-1}v = (A \otimes G)^{-1} v = \textrm{vec}(G^{-1}VA^{-T})$ since inversion is separable under Kronecker products, where $V$ is a $n \times n$ matrix formed from $v$. This can be computed in $O(n^2)$ memory and $O(n^3)$ time, rendering it feasible in practice. Hence, our influence scores are computed using the Kronecker-product identity on 

$$\nabla_\theta \ell(z_\textrm{test}, \theta)^T (A \otimes G)^{-1} \nabla_\theta \ell(z, \theta)$$

In practice, EK-FAC influence functions are computed not using the standard objective $L(\theta_\epsilon) + \epsilon \ell(z, \theta_\epsilon)$, but the Proximal Bregman Objective:

$$\sum_i D_{\mathcal{L}_i} (h(\theta, x_i), h(\theta_\epsilon, x_i)) + \epsilon \mathcal{L}(z_m, \theta) + \frac{\lambda}{2} || \theta - \theta_\epsilon ||^2$$

where $D$ measures divergence and $\mathcal{L}_y$ measures the loss function defined in terms of outputs/targets $y$. This allows for second-order estimation and more accurate gradient-descent based estimation of parameters, rather than just first-order optimized parameters. However, PBO / PBRF (Proximal Bregman Response Function) of course doesn’t measure what $\theta_\epsilon$ would be when retraining from scratch, just the effect of local perturbations to $\theta$. Furthermore, they use eigenvalue-corrected K-FAC values, which takes the multiplication computation from $O(n^3)$ complexity to $O(kn^2)$ for $k$ defined as the number of eigenvalues truncated to and amortizes the inversion computation, since the eigenbasis doesn’t update often (though computing it is $O(n^3)$ and eigenvalue computation is easy (simply $O(n^2)$). Eigenvalue-corrected K-FAC values are simply computed by finding the eigendecomposition of $A$ and $G$, such that 

$$F = A \otimes G = (U_A \otimes U_G) (\Lambda_A \otimes \Lambda_G) (U_A^T\otimes U_G^T)$$

EK-FAC is typically only run on MLP weights, keeping attention layers frozen.