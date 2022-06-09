from typing import List
from urllib import response
import fastapi as _fastapi
from fastapi.exceptions import HTTPException
import sqlalchemy.orm as _orm
import src.services as _services
import src.schemas as _schemas

app = _fastapi.FastAPI()


_services.create_database()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/api/account/{accountId}")
def read_account(accountId: str, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_account = _services.get_account_by_accountId(db = db, accountId = accountId)
    if db_account is None:
        raise HTTPException(status_code = 404, detail = "Account does not exist")
    return db_account
    
@app.post("/api/account/{accountId}")
def create_self_transaction(accountId: str, transaction: _schemas.SelfTransactionCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    transaction.account_from = accountId
    transaction.account_to = accountId
    
    db_transaction = _services.create_self_transaction(db = db, transaction = transaction)

@app.post("/api/account")
def create_account(account: _schemas.AccountCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return {"accountId" : _services.create_account(db = db, account = account).accountId}

@app.get("/api/account", response_model=List[_schemas.Account])
def read_accounts(skip: int=0, limit: int=10, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    accounts = _services.get_accounts(db = db, skip = skip, limit = limit)
    return accounts

