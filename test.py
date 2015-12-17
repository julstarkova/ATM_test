__author__ = 'Julia'

from functools import partial
from unittest import TestCase

from mock import ANY, Mock, sentinel

from exceptions import*
from ATM import*
from coverage import*


def mocked_card(account=None, blocked=False, pin=True):
    card = Mock()
    card.check_pin.return_value = pin
    card.is_blocked.return_value = blocked
    card.get_account.return_value = account
    return card


def mocked_account(balance):
    def _withdraw(self, amount):
        self.get_balance.return_value -= amount
        return amount

    account = Mock()
    account.get_balance.return_value = balance
    account.withdraw.side_effect = partial(_withdraw, account)
    return account


class TestValidation(TestCase):
    def setUp(self):
        self.atm = ATM(100)

    def test_good_card_validation(self):
        card = mocked_card()
        self.atm.validate_card(card, sentinel.pin_code)

        #card.check_pin.assert_called_once_with(sentinel.pin_code)
        self.assertEqual(self.atm.card, card)

    def test_blocked_card_validation(self):
        card = mocked_card(blocked=True)
        self.atm.validate_card(card, ANY)

        card.check_pin.assert_not_called()
        self.assertIsNone(self.atm.card)
        self.test_no_card_inserted()

    def test_wrong_pin_validation(self):
        card = mocked_card(pin=False)
        self.atm.validate_card(card, sentinel.pin_code)

        #card.check_pin.assert_called_once_with(sentinel.pin_code)
        self.assertIsNone(self.atm.card)
        self.test_no_card_inserted()

    def test_no_card_inserted(self):
        with self.assertRaises(NoCardInserted):
            self.atm.card_balance()
        with self.assertRaises(NoCardInserted):
            self.atm.get_money(100)



class TestOperation(TestCase):
    def setUp(self):
        self.atm = ATM(500)
        account = mocked_account(balance=700)
        card = mocked_card(account=account)
        self.atm.validate_card(card, ANY)

    def test_get_balance(self):
        self.assertEqual(self.atm.card_balance(), 700)
        self.atm.card.get_account().get_balance.assert_called_with()

    def test_get_cash_success(self):
        remaining = self.atm.get_money(50)
        self.atm.card.get_account().get_balance.assert_called_with()
        self.atm.card.get_account().withdraw.assert_called_with(50)
        self.assertEqual(remaining, 600)
        self.assertEqual(self.atm.card_balance(), 650)
        self.assertEqual(self.atm.money_balance, 450)

    def test_not_enough_money_in_atm(self):
        with self.assertRaises(NotEnoughMoneyInATM):
            self.atm.get_money(600)

    def test_not_enough_money_in_account(self):
        with self.assertRaises(NotEnoughMoneyInAccount):
            self.atm.get_money(850)


