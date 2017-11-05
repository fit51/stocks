import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import util.methods as m
import util.statistics as s
#%pylab inline
#pylab.rcParams['figure.figsize'] = (12, 8)

def assess_portfolio(sd='2008-1-1', ed='2009-1-1', \
    symbols=['GOOG','AAPL','GLD','XOM'], \
    allocs=[0.1,0.2,0.3,0.4], \
    start_volume=1000000, \
    rfr=0.0, \
                     #risk free rate
    sf=252.0, \
                     # Sampling frequency
    gen_plot=False):
    
    dates = pd.date_range(sd, ed)
    #prices = m.fill_missing_values(m.get_data(symbols, dates, False))
    prices = m.get_data(symbols, dates, False).dropna()
    normed = m.normalize_data(prices)
    alloced = normed * allocs
    pos_vals = alloced * start_volume
    port_val = pos_vals.sum(axis=1)
    if gen_plot:
        ax = m.normalize_data(port_val).plot(title='Portfolio vs. S&P500 normed', color='g', label='Portfolio')
        #SPY = m.fill_missing_values(m.get_data(['SPY'], dates, False))
        SPY = m.get_data(['SPY'], dates, False).dropna()
        SPY_normed = m.normalize_data(SPY).plot(label='SPY', color='b', ax = ax)
        ax.legend(loc='upper left')
    
    #Statistics
    daily_rets = s.daily_returns_simple(port_val)[1:]
    cum_ret = port_val[-1] / port_val[0] - 1
    print("Cumulative ret = {}".format(cum_ret))
    avg_daily_ret = daily_rets.mean()
    print("Avg Daily ret = {}".format(avg_daily_ret))
    std_daily_ret = daily_rets.std()
    print("Risk = {}".format(std_daily_ret))
    daily_rfr = (1.0 + rfr)**(1/sf) - 1
    k = sf ** (1/2) # sqrt
    sharpe_ratio = k * ((daily_rets - daily_rfr).mean() / std_daily_ret)
    print("Sharpe ratio = {}".format(sharpe_ratio))
    
    end_value = port_val[-1]
    print("End value = {}".format(end_value))
        
    return cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio, end_value