from typing import List
from urllib import response
import fastapi as _fastapi
import sqlalchemy.orm as _orm
import src.services as _services
import src.schemas as _schemas

app = _fastapi.FastAPI()


_services.create_database()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/api/account", response_model=List[_schemas.Account])
def read_accounts(skip: int=0, limit: int=10, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    accounts = _services.get_accounts(db = db, skip = skip, limit = limit)
    return accounts

@app.post("/api/account")
def create_account(account: _schemas.AccountCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return {"accountId" : _services.create_account(db = db, account = account).accountId}
