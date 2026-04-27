# pylint: disable=C0103,W0603,W0602
"""This file is used to create database session and initialize new database if it
doesn't exist"""

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.orm import Session

SqlAlchemyBase = orm.declarative_base()

__factory = None


def global_init(db_file):
    """This function initializes database globally"""
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise ValueError("Необходимо указать файл базы данных.")

    conn_str = f"sqlite:///{db_file.strip()}?check_same_thread=False"
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    """This function start database at file and return active base"""
    global __factory
    return __factory()
