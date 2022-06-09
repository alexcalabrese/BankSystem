from typing import List
from uuid import UUID, uuid4
import datetime as _dt
from pydantic import BaseModel, Field


class _TransactionBase(BaseModel):
    account_from: str
    account_to: str
    amount: float


class TransactionCreate(_TransactionBase):
    pass


class Transaction(_TransactionBase):
    id: str
    date_created: _dt.datetime
    date_last_updated: _dt.datetime

    class Config:
        orm_mode = True


class _AccountBase(BaseModel):
    name: str
    surname: str
    balance: float


class AccountCreate(_AccountBase):
    pass


class Account(_AccountBase):
    accountId: str
    transactions: List[Transaction] = []

    class Config:
        orm_mode = True
