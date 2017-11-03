import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from time import time
import os
import math
import util.statistics as s

def symbol_to_path(symbol, base_dir="data"):
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))
# dates = pd.date_range('2010-01-01', '2010-12-31')
# symbols = ['GOOG','IBM','GLD']

def get_data(symbols, dates, add_spy=True):
    df = pd.DataFrame(index=dates)
    if add_spy and 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, 'SPY')
    print(symbols)
    for symbol in symbols:
        df_temp=pd.read_csv(symbol_to_path(symbol), index_col="Date", 
                     parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
        df_temp=df_temp.rename(columns={'Adj Close': symbol})
        if symbol == 'SPY':
            df=df.join(df_temp, how='inner')
        else:
            df=df.join(df_temp)

    return df
	
def fill_missing_values(df_data):
    df_data.fillna(method='ffill', inplace=True)
    df_data.fillna(method='bfill', inplace=True)
    return df_data

def normalize_data(df):
    return df/df.ix[0]

def plot_selected(df, columns, start_index, end_index):
    df = df.ix[start_index:end_index, columns]
    plot_data(df)
	
def plot_data(df, title="Stock Prices"):
    ax = df.plot(title=title, fontsize=10)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()
	
def print_statistics(df):
	cum_ret = s.cumulative_return(df)
	print("Cumulative Return")
	print(cum_ret.head(n=3))
	print("Daily Return")
	daily_rets = s.daily_returns(df)
	plot_data(daily_rets)
	print(daily_rets.head(n=3))
	print("Average Daily Return:")
	print(s.average_daily_return(df))
	print("Risk:")
	print(s.risk(df))
	print("Sharpe_Ration:") 
	print(s.sharpe_ratio_dayily(daily_rets, 0))