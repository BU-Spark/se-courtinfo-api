from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime

from app.core import config

engine = create_engine(config.SQLALCHEMY_DATABASE_URI, )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class utcnow(expression.FunctionElement):
    type = DateTime()

# Taken directly from
# https://docs.sqlalchemy.org/en/13/core/compiler.html#utc-timestamp-function
# Generates a UTC timestamp
@compiles(utcnow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
