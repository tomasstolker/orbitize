import orbitize
from orbitize import read_input, system, priors, sampler
from orbitize.kepler import calc_orbit
import matplotlib.pyplot as plt
import numpy as np
import astropy.table
import time
from orbitize.read_input import read_file
from orbitize.system import generate_synthetic_data
import time

#record start time
start = time.time()

# generate data
mtot = 1.2 # total system mass [M_sol]
plx = 60.0 # parallax [mas]
n_orbs = 500
sma = 2.3
data_table, orbit_fraction = generate_synthetic_data(mtot, plx, sma=sma,
num_obs=30)
print('The orbit fraction is {}%'.format(np.round(orbit_fraction),1))

# plot orbit coverage with fake data
plt.errorbar(data_table['quant1'], data_table['quant2'], 
yerr = data_table['quant1_err'], xerr = data_table['quant2_err'])
plt.savefig('/home/tmckenna/orbitize/results/fake_orbit_data.png')

# initialize orbitize `System` object
sys = system.System(1, data_table, mtot, plx)
print(data_table)
lab = sys.param_idx

# set all parameters except eccentricity to fixed values for testing
# sys.sys_priors[lab['inc1']] = np.pi/4
sys.sys_priors[lab['sma1']] = sma
# sys.sys_priors[lab['aop1']] = np.pi/4
sys.sys_priors[lab['pan1']] = np.pi/4
# sys.sys_priors[lab['tau1']] = 0.8
sys.sys_priors[lab['plx']] = plx
sys.sys_priors[lab['mtot']] = mtot


# run nested sampler
nested_sampler = sampler.NestedSampler(sys)
_ = nested_sampler.run_sampler(static = True, bound = 'multi', pfrac = 0.8)

# save results
nested_sampler.results.save_results('test9.hdf')

# assumed values for synthetic data
ecc = 0.5 # eccentricity
inc = np.pi/4 # inclination [rad]
aop = np.pi/4
pan = np.pi/4
tau = 0.8

# plot ecc
plt.figure()
accepted_eccentricities = nested_sampler.results.post[:, lab['ecc1']]
plt.hist(accepted_eccentricities, alpha=0.5, bins=50)
plt.axvline(x=ecc, color='red')
plt.xlabel('ecc'); plt.ylabel('number of orbits')
plt.savefig('/home/tmckenna/orbitize/results/ecc_test9.png')

# plot inc
plt.figure()
accepted_inclinations = nested_sampler.results.post[:, lab['inc1']]
plt.hist(accepted_inclinations, alpha=0.5, bins=50)
plt.axvline(x=inc, color='red')
plt.xlabel('inc'); plt.ylabel('number of orbits')
plt.savefig('/home/tmckenna/orbitize/results/inc_test9.png')

# plot aop
plt.figure()
accepted_aop = nested_sampler.results.post[:, lab['aop1']]
plt.hist(accepted_aop, bins=50)
plt.axvline(x=aop, color='red')
plt.xlabel('aop'); plt.ylabel('number of orbits')
plt.savefig('/home/tmckenna/orbitize/results/aop_test9.png')

# plot pan
# plt.figure()
# accepted_pan = nested_sampler.results.post[:, lab['pan1']]
# plt.hist(accepted_pan, bins=50)
# plt.axvline(x=pan, color='red')
# plt.xlabel('pan'); plt.ylabel('number of orbits')
# plt.savefig('/home/tmckenna/orbitize/results/pan_test8.png')

# plot tau
plt.figure()
accepted_tau = nested_sampler.results.post[:, lab['tau1']]
plt.hist(accepted_tau, bins=50)
plt.axvline(x=aop, color='red')
plt.xlabel('tau'); plt.ylabel('number of orbits')
plt.savefig('/home/tmckenna/orbitize/results/tau_test9.png')

#calculate script run time
execution_time = time.time() - start
print("Execution time (s): " + str(execution_time))
