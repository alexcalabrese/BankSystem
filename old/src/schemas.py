from typing import List
from uuid import UUID, uuid4
import datetime as _dt
from pydantic import BaseModel, Field


class _TransactionBase(BaseModel):
    account_from: str
    account_to: str
    amount: float
    
class _SelfTransactionBase(BaseModel):
    account_from: str
    account_to: str
    

class TransactionCreate(_TransactionBase):
    pass

class SelfTransactionCreate(_SelfTransactionBase):
    amount: float

class Transaction(_TransactionBase):
    id: str
    date_created: _dt.datetime
    date_last_updated: _dt.datetime

    class Config:
        orm_mode = True


class _AccountBase(BaseModel):
    name: str
    surname: str


class AccountCreate(_AccountBase):
    pass


class Account(_AccountBase):
    accountId: str
    balance: float
    transactions: List[Transaction] = []

    class Config:
        orm_mode = True