
from decimal import Decimal
from typing import List

import sqlalchemy
import sqlalchemy.engine.row 
import json
import yfinance as yf
import pandas as pd
import numpy as np
import datetime
from zoneinfo import ZoneInfo

class Stock:
    def __init__(self, ticker: yf.Ticker):
        self.info = ticker.get_info()
        self.__history = ticker.history(period = "1d", interval = "1m")
        self.__price = self.__history["currentPrice"]
        self.__split = ticker.splits

    def getPrice(self) -> np.float64:
        return self.__price
    
    def getSplit(self) -> pd.core.series.Series:
        return self.__split
    

class Portfolio:
    # should pull the params from the created database
    def __init__(self, rows: List[sqlalchemy.engine.row.Row]):
        # portfolio for 1 person
        # expects rows taken from the database for init method

        # function should print what we need to do to rebalance the portfolio
        # inputs: dict of current portfolio holdings, target allocation and total value of portfolio

        if not rows:
            raise Exception("Expected more than 0 rows")
        self.id = rows[0].id
        self.username = rows[0].username
        self.contact_number = rows[0].contact_number
        self.email = rows[0].email

        # user's percentage preference, is a string, need to parse json
        self.percentage_preference = rows[0].percentage_preference

        # calculate amount of money the person has in each ticker
        self.current_holdings = {}
        self.last_update_dates = {}
        self.number_of_shares = {} # number of shares for each stock
        self.stock_price = {}

        # our updates for the same ticker should not create new rows in the database
        for row in rows:
            self.current_holdings[row.ticker] = row.price * row.number_of_shares
            self.last_update_dates[row.ticker] = row.last_update_date
            self.stock_price[row.ticker] = row.price
            self.number_of_shares[row.ticker] = row.number_of_shares
        

        # NOTE: TO BE DELETED 
        # for row in rows:
        #     self.number_of_shares[row.ticker] = row.number_of_shares
        #     self.current_holdings[row.ticker] = row.price * row.number_of_shares
        #     self.last_update_dates[row.ticker] = row.last_update_date

        # find total value of portfolio
        self.total_value = sum(self.current_holdings.values())


    def rebalance(self) -> None:
        """
        Rebalance the portfolio. Currently only prints out what the user should purchase, does not update user's holdings yet.

        Args:
            None.
            NOTE: We are printing the number of shares each person should purchase. Update the function later on.

        Returns:
            None.

        Idea:

        1. inputs: current portfolio percentages + ideal portfolio percentages
        2. compute new total value of portfolio
        3. use the ideal percentages that the user wants to multiply by the new value
        4. find the difference for each stock (if stock exists previously, need to consider current value in portfolio to calculate difference)
        5. suggest what to buy and sell
        
        """
        # step 2: compute total value of portfolio (done)

        # step 3: use ideal percentages that user wants, multiply by new value
        # dict of key=ticker, value=ideal amount user wants
        ideal_holdings = {}
        for ticker, ideal_percentage in self.percentage_preference.items():
            # convert from float to decimal for precise calculations
            ideal_holdings[ticker] = Decimal(ideal_percentage) * self.total_value

        # step 4: find difference in amount between ideal amount user wants, and current amount user owns
        # for each stock
        differences = {}
        for ticker in ideal_holdings.keys():
            # if > 0, means need to buy
            # if < 0, means need to sell
            differences[ticker] = ideal_holdings[ticker] - self.current_holdings[ticker]

        # step 5: finally, print out how much of each stock should be bought or sold
        for ticker, amount_to_buy in differences.items():
            shares_to_buy = amount_to_buy / self.stock_price[ticker]
            if shares_to_buy > 0:
                print(f"You should buy {shares_to_buy: .2f} shares of {ticker}")
            else:
                print(f"You should sell {-1 * shares_to_buy: .2f} shares of {ticker}")


    def setLastUpdateDate(self, new_date: datetime.date, ticker: str):
        """
        update last update date for a particular tick

        Args:
            new_date: datetime.date (in America/New york)
        """
        self.last_update_dates[ticker] = datetime.date

    def setStockPrice(self, new_price: Decimal, ticker: str):
        self.stock_price[ticker] = new_price

    def setNumberOfShares(self, no_of_shares, ticker: str):
        self.number_of_shares[ticker] = no_of_shares


    def updateStockInfo(self):
        """
        TRACK PORTFOLIO FEATURE:

        check number of splits for each stock
        update number of shares, price for each stock
        update the date of retrieving the stock's information

        """
        for ticker in self.current_holdings:
            # stock_price = self.stock_price[ticker]
            no_of_share = self.number_of_shares[ticker]
            stock_last_update_date = self.last_update_dates[ticker]

            # find and retrieve new stock price
            cur_stock = Stock(yf.Ticker(ticker))
            new_stock_price = cur_stock.getPrice() #np.float64
            new_stock_price = Decimal(str(new_stock_price)) # convert to Decimal type

            # dealing with stock split logic
            stock_split_series = cur_stock.getSplit() #it is a pd series of stock splits
            # NOTE
                # for now, assume last update date is in 'America/New_York' timezone for filtering out date (to be updated in the future)
            target_date = pd.Timestamp(stock_last_update_date, tz='America/New_York')
            stock_split_series_filtered = stock_split_series[stock_split_series.index > target_date]
            cum_factor = np.prod(stock_split_series_filtered.values) #np.float64
            new_share_amt = cum_factor * no_of_share

            cur_date = datetime.datetime.now(ZoneInfo('America/New_York')).date()

            self.setLastUpdateDate(cur_date, ticker)
            self.setStockPrice(new_stock_price, ticker)
            self.setNumberOfShares(new_share_amt, ticker)



