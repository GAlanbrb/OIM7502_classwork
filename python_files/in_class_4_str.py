import datetime as dt
import matplotlib.pyplot as plt
#import matplotlib.ticker as mtick # optional may be helpful for plotting percentage
import numpy as np
import pandas as pd
import seaborn as sb # optional to set plot t
import yfinance as yf

sb.set_theme() # optional to set plot theme

DEFAULT_START = dt.date.isoformat(dt.date.today() - dt.timedelta(365))
DEFAULT_END = dt.date.isoformat(dt.date.today())

class Stock:
    def __init__(self, symbol, start=DEFAULT_START, end=DEFAULT_END):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.data = self.get_data()


    def get_data(self):
        data = yf.download(self.symbol, start=self.start, end=self.end,auto_adjust=False #interval="1d",#progress=False
        )
        data.index = pd.to_datetime(data.index)
        data = self.calc_returns(data)
        return data


    def calc_returns(self, df):
        df["change"] = df["Close"].diff() # Close-to-close difference
        df["instant_return"] = np.log(df["Close"]).diff().round(4) # Instantaneous (log) return
        return df

    
    def plot_return_dist(self): #"""method that plots instantaneous returns as histogram"""
        r = self.data["instant_return"].dropna()

        plt.figure(figsize=(8, 5))
        plt.hist(r, bins=50, edgecolor="black")
        plt.title(f"{self.symbol}: Distribution of Daily Instantaneous Returns")
        plt.xlabel("Instantaneous return (log diff)")
        plt.ylabel("Frequency")
        plt.grid(True, linestyle="-.", alpha=0.5)
        plt.tight_layout()
        plt.show()


    def plot_performance(self): # """method that plots stock object performance as percent """
        close = self.data["Close"].dropna()

        perf_pct = (close / close.iloc[0] - 1.0) * 100.0 # percent gain/loss relative to first period

        plt.figure(figsize=(9, 5))
        plt.plot(perf_pct.index, perf_pct.values, linewidth=2)
        plt.title(f"{self.symbol}: Performance (% gain/loss) {self.start} to {self.end}")
        plt.xlabel("Date")
        plt.ylabel("Percent")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.show()


def main():
    test = Stock(symbol=["AAPL"]) # optionally test custom data range
    print(test.data)
    test.plot_performance()
    test.plot_return_dist()


if __name__ == '__main__':
    main()