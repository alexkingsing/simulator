# THIS WILL HOLD THE SIMULATION SETTINGS

import numpy as np

def daily_demand():
    # Mean demand of 20 orders a day
    demand = np.random.poisson(lam=20)
    