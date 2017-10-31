import math
#daily_returns
def daily_returns(df):
    daily_returns = (df / df.shift(1)) - 1
    daily_returns.ix[0, :] = 0
    return daily_returns

def daily_returns_simple(df):
    daily_returns = (df / df.shift(1)) - 1
    daily_returns[0] = 0
    return daily_returns
	
#cumulative return
def cumulative_return(df):
    df_cum = (df / df.ix[0, :]) - 1
    return df_cum

# Average Daily return
def average_daily_return(df):
    return daily_returns(df).mean()

# Average Daily return
def risk(df):
    return daily_returns(df).std()

def sharpe_ratio(daily_rets, daily_rf, sampling_freq):
    return math.sqrt(sampling_freq) * (daily_rets - daily_rf).mean() / daily_rets.std()

def sharpe_ratio_dayily(daily_rets, daily_rf):
    return sharpe_ratio(daily_rets, daily_rf, 252)
def sharpe_ratio_weekly(daily_rets, daily_rf):
    return sharpe_ratio(daily_rets, daily_rf, 52)
def sharpe_ratio_monthly(daily_rets, daily_rf):
    return sharpe_ratio(daily_rets, daily_rf, 12)