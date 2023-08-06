#arg1 population stats, arg2 sample stats

import pickle, sys
import numpy as np
import scipy.stats
pop = pickle.load(open(sys.argv[1], 'rb'))
sample = pickle.load(open(sys.argv[2], 'rb'))
print('sample size',len(pop), sample.mean() - pop.mean())
z = (sample.mean() - pop.mean())/(pop.std()/np.sqrt(pop))
print(pop.std(), sample.std())
p_values = scipy.stats.norm.sf(abs(z))
print(z, p_values)