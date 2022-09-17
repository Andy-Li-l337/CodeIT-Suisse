import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import truncnorm
import math
fig, ax = plt.subplots(1, 1)
myclip_a = 35
myclip_b = 45
my_mean = 40
my_std = math.sqrt(10)
a, b = (myclip_a - my_mean) / my_std, (myclip_b - my_mean) / my_std
rv = truncnorm(a, b, loc=my_mean, scale=my_std)
x = np.linspace(rv.ppf(0.01), rv.ppf(0.99), 100)
print(np.sum(np.multiply(rv.pdf(x), np.where(x < 40, -1, x-41))))
