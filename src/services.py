import src.database as _database
import sqlalchemy.orm as _orm
import src.models as _models
import src.schemas as _schemas


def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_account_by_id(db: _orm.Session, accountId: str):
    return db.query(_models.Account).filter(_models.Account.accountId == accountId).first()

def get_accounts(db: _orm.Session, skip: int = 0, limit: int = 100):
    return db.query(_models.Account).offset(skip).limit(limit).all()

def create_account(db: _orm.Session, account: _schemas.AccountCreate):
    db_account = _models.Account(name=account.name, surname=account.surname)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

# def create_transaction(db: _orm.Session, post: _schemas.TransactionCreate, user_id: int):
#     db_transaction = _models.Transaction(**post.dict(), owner_id=user_id)
#     db.add(db_transaction)
#     db.commit()
#     db.refresh(db_transaction)
#     return db_transaction
