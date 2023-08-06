```python
from sbi.simulators.linear_gaussian import linear_gaussian
import torch
from torch.distributions import MultivariateNormal
from sbi.utils import BoxUniform
from torch import Tensor, eye, ones, zeros
```


```python
dim = 1

def model(theta, n=1, cov=None):
    
    ns, dim = theta.shape
    if cov is None:
        cov = torch.eye(dim)

    x = MultivariateNormal(theta, covariance_matrix=cov).sample((n, ))
    
    return x.squeeze(0)

prior = BoxUniform(-10 * torch.ones(1), 10 * torch.ones(1))
```


```python
def true_model(theta, n=1, variance=1.0):
    ns, dim = theta.shape

    scales = torch.ones(ns)
    scales[torch.rand(ns) > 2/3] = variance
    cov = torch.ones(ns, dim, dim)
    for i in range(ns):
        cov[i, ] = scales[i] * torch.eye(dim)
    x = MultivariateNormal(theta, covariance_matrix= cov).sample((n, ))
    
#     return torch.cat((x.mean(dim=0), x.std(dim=0)**2), dim=1)
    return x.squeeze(0)
```


```python
# TODO: need dependency on iid samples n.
def sample_true_posterior(x_o, variance, num_samples):
    
    dim = x_o.shape[1]
    scales = torch.ones(num_samples)
    scales[torch.rand(num_samples) > 2/3] = variance
    cov = torch.ones(num_samples, dim, dim)
    for i in range(num_samples):
        cov[i, ] = scales[i] * torch.eye(dim)
    x = MultivariateNormal(x_o, covariance_matrix= cov).sample()
    
    return x
```


```python
t0 = prior.sample((1,))
x0 = model(t0)
sample_true_posterior(x0, variance=4.0, num_samples=10)
```




    tensor([[-5.8349],
            [-6.8498],
            [-5.7198],
            [-7.0183],
            [-4.0052],
            [-5.3367],
            [-4.5858],
            [-5.2005],
            [-5.2532],
            [-6.9799]])



# True posterior
Given the uniform prior, the underlying true model and a fixed $\sigma$, the true posterior is given by

$$ 
p(\theta | x_o) \sim 2 / 3 \; \mathcal{N}(\theta | x_o, 1) + 1 / 3 \; \mathcal{N}(\theta | x_o, \sigma)
$$

This holds only for number of iid samples $n=1$.

For the $n>1$ one probably has to derive the posterior for iid samples for each Gaussian component and sample from the mixture of both.

# Inference


```python
from sbi.utils.get_nn_models import posterior_nn
import sbi.utils as utils
from sbi.inference import SNPE, prepare_for_sbi
from sbi.simulators.linear_gaussian import linear_gaussian
import torch
from torch.distributions import MultivariateNormal, Uniform
from torch import Tensor, eye, ones, zeros
```


```python
inference = SNPE(model, prior, density_estimator="mdn", 
                 show_progress_bars=True)
```


```python
posterior = inference(num_simulations=5000)
```


    HBox(children=(FloatProgress(value=0.0, description='Running 5000 simulations.', max=5000.0, style=ProgressSty…


    
    Neural network successfully converged after 60 epochs.



```python
# do inference for observed data from true model
ss = 6
true_thetas = torch.zeros(ss)
variances = torch.linspace(1, 5, ss)
```


```python
xos = torch.cat([true_model(true_thetas[i].reshape(1, -1), variance=variances[i]) for i in range(ss)])
```


```python
import matplotlib.pyplot as plt
```


```python
fig, ax = plt.subplots(2, 3, figsize=(18, 10))

i = 0 
j = 0
for i in range(2):
    for j in range(3):
        idx = i * 3 + j
        ps = posterior.sample((1000, ), x=xos[idx], show_progress_bars=False)
        pts = sample_true_posterior(xos[idx].reshape(1, -1), variances[idx], 1000)
        plt.sca(ax[i, j])
        _, bins, _ = plt.hist(ps.numpy().squeeze(), bins=20, alpha=0.7)
        plt.hist(pts.numpy().squeeze(), bins=bins, alpha=0.7);
        plt.axvline(x=true_thetas[idx], c='k')
        plt.axvline(x=xos[idx], c='r')

```


![png](SBI%20and%20Model%20Misspecification_files/SBI%20and%20Model%20Misspecification_13_0.png)


## Results
Seems to work quite well! 

To Do: do for $n>1$.

Note, that the actual model misspecification wrt to the variance takes effect only when $n>1$.


```python

```
