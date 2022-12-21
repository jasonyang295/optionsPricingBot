import yfinance as yf

#option format:
# - strike price
# - call or put
# - expiration date


class Option:
  contractSymbol: str = ""
  impliedVolatility: float = ""
  strike: float = ""
  bid: float = ""
  ask: float = ""
  ticker: str = ""
  expirationDate: str = ""
  type: str = ""

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
    
    """ % (self.contractSymbol, self.impliedVolatility, self.strike, self.bid,
           self.ask, self.ticker, self.expirationDate, self.type))


def get_option_dates(ticker: str):
  ticker_obj = yf.Ticker(ticker)
  return ticker_obj.options


def get_option_chain(ticker: str, expiration_date: str):
  ticker_obj = yf.Ticker(ticker)
  return ticker_obj.option_chain(expiration_date)


def main():
  ticker = "MSFT"
  option_dates = get_option_dates(ticker)
  call_objects = []
  put_objects = []
  for option_date in option_dates:
    option_chain = get_option_chain(ticker, option_date)
    calls = option_chain[0]
    puts = option_chain[1]
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
      put_objects.append(new_option)

    #print(option_chain)
    # import pdb
    # pdb.set_trace()

  print(call_objects[0])


if __name__ == "__main__":
  main()
