from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(
    settings.database_url,
    echo=True,
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()




        

# from sqlalchemy import create_engine
# from sqlalchemy .orm import declarative_base, sessionmaker


# from app.core.config import settings



# engine = create_engine(
#     settings.database_url,
#     echo=True,
# )

# SessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine,
# )


# Base = declarative_base


# def get_db():
#     """
#     Create and provide a database session.
#     """

#     db = SessionLocal()

#     try:
#         yield
#     finally:
#         db.close()    