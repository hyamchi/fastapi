from app.calculations import add, multiply, BankAccount, InsufficientFunds
import pytest

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def fifty_bank_account():
    return BankAccount(50) 

@pytest.mark.parametrize("num1, num2, expected", [(3, 2, 5), (7, 1, 8), (12, 4, 16)])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected 


def test_multiply():
    assert multiply(5, 3) == 15 

def test_initial_balance(fifty_bank_account):
    # ba = BankAccount(50)
    # assert ba.balance == 50
    assert fifty_bank_account.balance == 50    

def test_initial_balance_default(zero_bank_account):
    # ba = BankAccount()
    assert zero_bank_account.balance == 0

def test_withdraw(fifty_bank_account):
    # ba = BankAccount(50)
    fifty_bank_account.withdraw(20)
    assert  fifty_bank_account.balance == 30

def test_interest(fifty_bank_account):
    # ba = BankAccount(50)
    fifty_bank_account.collect_interest()
    # assert  ba.balance == 55
    assert  round(fifty_bank_account.balance, 4) == 55

@pytest.mark.parametrize("deposited, withdrew, expected", [(100, 20, 80), (500, 400, 100), (1200, 1000, 200)])
def test_transaction(zero_bank_account, deposited, withdrew, expected):
    
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert  zero_bank_account.balance == expected

def test_insufficient_amount(fifty_bank_account):
    with pytest.raises(InsufficientFunds):
        fifty_bank_account.withdraw(100)