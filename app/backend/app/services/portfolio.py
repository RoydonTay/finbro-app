from decimal import Decimal
from typing import List

import sqlalchemy


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
        self.prices = {}
        # our updates for the same ticker should not create new rows in the database
        for row in rows:
            self.current_holdings[row.ticker] = row.price * row.number_of_shares
            self.last_update_dates[row.ticker] = row.last_update_date
            self.prices[row.ticker] = row.price

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

        """

        """Idea:

        1. inputs: current portfolio percentages + ideal portfolio percentages
        2. compute new total value of portfolio
        3. use the ideal percentages that the user wants to multiply by the new value
        4. find the difference for each stock (if stock exists previously, need to consider current value in portfolio to calculate difference)
        5. suggest what to buy and sell"""

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
            shares_to_buy = amount_to_buy / self.prices[ticker]
            if shares_to_buy > 0:
                print(f"You should buy {shares_to_buy: .2f} shares of {ticker}")
            else:
                print(f"You should sell {-1 * shares_to_buy: .2f} shares of {ticker}")
