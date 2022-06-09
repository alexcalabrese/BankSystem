import imp
import secrets
import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import uuid
import datetime as _dt
from sqlalchemy.dialects.postgresql import UUID


import src.database as _database


class Account(_database.Base):
    __tablename__ = "accounts"
    accountId = _sql.Column(
        _sql.String, primary_key=True, default= secrets.token_hex(10))
    name = _sql.Column(_sql.String)
    surname = _sql.Column(_sql.String)
    balance = _sql.Column(_sql.Float, default=0)


class Transaction(_database.Base):
    __tablename__ = "transactions"
    transactionId = _sql.Column(
        _sql.String, primary_key=True, default= lambda: str(uuid.uuid4()))

    account_from_id = _sql.Column(
        _sql.String, _sql.ForeignKey("accounts.accountId"))
    account_to_id = _sql.Column(
        _sql.String, _sql.ForeignKey("accounts.accountId"))
    amount = _sql.Column(_sql.Float)

    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    date_last_updated = _sql. Column(
        _sql. DateTime, default=_dt.datetime. utcnow)
