import numpy as np
from matplotlib import pyplot as plt
import time
from multipletau_cor_tttr.correlate import CCF as xcorr
import os
__author__ = 'Anders Barth'

def run():
    # load data
    t = np.load(os.path.join(os.path.dirname(__file__), 'sample_data.npy'))
    syncrate = 27027027.027  # normally provided by photon file

    # correlate and time
    start = time.time()
    corr, error, timeaxis = xcorr(t, t)
    stop = time.time()
    print("Autocorrelated " + str(len(t)) + " photons in " + str(stop-start) + " s.")

    # plot
    plt.errorbar(timeaxis/syncrate, corr, error)
    plt.xscale('log')
    plt.xlabel('Timelag t (s)')
    plt.ylabel('G(t)')
    plt.xlim((1e-6, 1))
    plt.ylim((np.min(corr-error), np.max(corr+error)))
    plt.axvline(5E-4, linestyle='-', color='red')
    plt.text(0.6E-3, 4, r"$\tau_{D}$ = 500 ms")
    plt.show()


if __name__ == '__main__':
    """
    Example analysis using sample data found in sample_data.npy.
    Synthetic data of a single diffusing species. Diffusion time is 0.5 ms (indicated in plot).
    """
    run_example()

    