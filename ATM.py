__author__ = 'Julia'

from exceptions import *
from functools import wraps

class Account:
    def get_balance(self):
        "_"

    def withdraw(self,amount):
        "_"

class Card:
    def is_blocked (self):
        "_"

    def get_account(Account):
        "_"

    def check_pin (self,pin):
        "_"

def ascertain_card(func):
    @wraps(func)
    def wrapp(self, *a):
        if not self.card:
            raise NoCardInserted
        return func(self, *a)

    return wrapp

class ATM:
    def __init__(self,cash=0):
        self.money_balance = cash
        self.card = None

    def validate_card(self,card,pin):
        if card.is_blocked() or not card.check_pin():
            return False
        self.card = card

    @ascertain_card
    def card_balance(self):
        return self.card.get_account().get_balance()

    @ascertain_card
    def get_money(self,am):
        if am > self.card_balance() :
            raise NotEnoughMoneyInAccount
        if am > self.money_balance:
            raise NotEnoughMoneyInATM

        withdrawn = self.card.get_account().withdraw(am)
        self.money_balance -= withdrawn
        rem = self.card_balance() - withdrawn
        return rem





