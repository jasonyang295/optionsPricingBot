from datetime import datetime
import yfinance as yf
import numpy as np
import math
from scipy.stats import norm

#option format:
# - strike price
# - call or put
# - expiration date


class Option:
  contractSymbol: str = ""
  impliedVolatility: float = 0.0
  strike: float = 0.0
  bid: float = ""
  ask: float = ""
  ticker: str = ""
  expirationDate: str = ""
  type: str = ""
  spot: float = 0.0

  def __str__(self):
    return ("""
    Contract: %s
    Implied Volatility: %s
    Strike: %s
    Bid: %s
    Ask: %s
    Ticker: %s
    Expiration Date: %s
    Type: %s
    Spot: %f
    """ % (self.contractSymbol, self.impliedVolatility, self.strike, self.bid,
           self.ask, self.ticker, self.expirationDate, self.type, self.spot))


def get_option_dates(ticker: str):
  ticker_obj = yf.Ticker(ticker)
  return ticker_obj.options


def get_option_chain(ticker: str, expiration_date: str):
  ticker_obj = yf.Ticker(ticker)
  return ticker_obj.option_chain(expiration_date)


def get_price(ticker: str):
  ticker_obj = yf.Ticker(ticker)
  return ticker_obj.info["regularMarketPrice"]


def black_scholes(spot_price: float, strike_price: float, expiration_date: str,
                  impliedVolatility: float):

  #if time horizon is super low, set to new value that is extremely small instead of 0 as that causes value to go to inf. if call is zero day to expiry call, set denom to small value since 0 causes the value to go to infinity which is inaccurate. 
  time_horizon = (datetime.strptime(expiration_date, "%Y-%m-%d") -
                  datetime.now()).days
  vol_sqrt_t = 0.000001 if (impliedVolatility * math.sqrt(time_horizon)) == 0.0 else (impliedVolatility * math.sqrt(time_horizon))
                    
  #using black scholes equation and libor rate from this week
  d1 = np.log(
    spot_price / strike_price) + (0.0548 +
                                  (impliedVolatility**2) / 2) * time_horizon
  d1 = d1 / (impliedVolatility * np.sqrt(time_horizon))
  d2 = d1 - (impliedVolatility * np.sqrt(time_horizon))

  # print("D1: %f" % d1)
  # print("D2: %f" % d2)
  cumsum_n1 = norm.cdf(d1) * spot_price
  cumsum_n2 = norm.cdf(d2) * strike_price * math.e ** (-0.0548 * time_horizon)

  return cumsum_n1 - cumsum_n2


def get_options_arrays():
  ticker = "MSFT"
  option_dates = get_option_dates(ticker)
  call_objects = []
  put_objects = []
  price = get_price(ticker)
  idx = 0

  for option_date in option_dates:
    option_chain = get_option_chain(ticker, option_date)
    calls = option_chain[0]
    puts = option_chain[1]
    idx += 1
    if idx >= 5:
      break
    for optionIdx in calls.index:
      if (optionIdx >= len(calls['contractSymbol'])):
        break
      new_option = Option()
      new_option.contractSymbol = calls['contractSymbol'][optionIdx]
      new_option.impliedVolatility = calls['impliedVolatility'][optionIdx]
      new_option.strike = calls['strike'][optionIdx]
      new_option.bid = calls['bid'][optionIdx]
      new_option.ask = calls['ask'][optionIdx]
      new_option.ticker = ticker
      new_option.expirationDate = option_date
      new_option.type = 'C'
      new_option.spot = float(price)
      call_objects.append(new_option)

    for optionIdx in puts.index:
      new_option = Option()
      if (optionIdx >= len(puts['contractSymbol'])):
        break
      new_option.contractSymbol = puts['contractSymbol'][optionIdx]
      new_option.impliedVolatility = puts['impliedVolatility'][optionIdx]
      new_option.strike = puts['strike'][optionIdx]
      new_option.bid = puts['bid'][optionIdx]
      new_option.ask = puts['ask'][optionIdx]
      new_option.ticker = ticker
      new_option.expirationDate = option_date
      new_option.type = 'P'
      new_option.spot = float(price)
      put_objects.append(new_option)

    #print(option_chain)
    # import pdb
    # pdb.set_trace()

  return call_objects, put_objects
  #print(call_objects[0])


def main():
  calls, puts = get_options_arrays()
  for call in calls:
    price = black_scholes(spot_price = call.spot,
                         strike_price = call.strike,
                         expiration_date = call.expirationDate,
                         impliedVolatility = call.impliedVolatility)
    print(price)
    print(call)


if __name__ == "__main__":
  main()
