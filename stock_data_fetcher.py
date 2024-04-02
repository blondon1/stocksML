import yfinance as yf

def fetch_stock_data(symbol, period='1d'):
    stock = yf.Ticker(symbol)
    hist = stock.history(period=period)
    return hist
