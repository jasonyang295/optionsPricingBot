import yfinance as yf

#option format:
# - strike price
# - call or put
# - expiration date

class Option:
  contractSymbol: str = ""
  impliedVolatility: float = ""
  strike : float = ""
  bid: float = ""
  ask: float = ""
  ticker: str = ""
  expirationDate: str = ""
  type: str = ""
  
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
    for option in calls: 
      new_option = Option()
      new_option.contractSymbol = option['contractSymbol']
      new_option.impliedVolatility = option['impliedVolatility']
      new_option.strike = option['strike']
      new_option.bid = option['bid']
      new_option.ask = option['ask']
      new_option.ticker = ticker
      new_option.expirationDate = option_date
      new_option.type = 'C'
    for option in puts: 
      new_option = Option()
      new_option.contractSymbol = option['contractSymbol']
      new_option.impliedVolatility = option['impliedVolatility']
      new_option.strike = option['strike']
      new_option.bid = option['bid']
      new_option.ask = option['ask']
      new_option.ticker = ticker
      new_option.expirationDate = option_date
      new_option.type = 'P'
      
    print(option_chain)
    import pdb
    pdb.set_trace()


if __name__ == "__main__":
  main()
