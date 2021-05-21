from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, MetaData
import sqlalchemy as sql
import logging
import os

logger = logging.getLogger(__name__)

Base = declarative_base()


def generate_engine_string(engine_string):
    """Generate engine_string.
    Args:
        engine_string (string): pased argument from run.py to specify SQLALCHEMY's path (local/RDS)
    Returns:
        engine_string (string): engine_string to be used in create_db()
    """
    DB_HOST = os.environ.get('MYSQL_HOST')
    DB_PORT = os.environ.get('MYSQL_PORT')
    DB_USER = os.environ.get('MYSQL_USER')
    DB_PW = os.environ.get('MYSQL_PASSWORD')
    DATABASE = os.environ.get('DATABASE_NAME')
    DB_DIALECT = 'mysql+pymysql'

    if engine_string is not None:
        pass
    elif DB_HOST is None:
        engine_string = 'sqlite:///data/steam.db'
    else:
        engine_string = '{dialect}://{user}:{pw}@{host}:{port}/{db}'.format(dialect=DB_DIALECT, user=DB_USER,
                                                                                      pw=DB_PW, host=DB_HOST,
                                                                                      port=DB_PORT,
                                                                                      db=DATABASE)
    return engine_string


class Steam(Base):
    """Create a data model for the database to be set up for recording steam games """
    __tablename__ = 'steam'

    appid = Column(Integer, primary_key=True)
    name = Column(String(200), unique=False, nullable=False)
    release_date = Column(DateTime, unique=False, nullable=True)
    english = Column(Integer, unique=False, nullable=False)
    developer = Column(String(200), unique=False, nullable=False)
    publisher = Column(String(200), unique=False, nullable=False)
    platforms = Column(String(200), unique=False, nullable=False)
    required_age = Column(Integer, unique=False, nullable=False)
    genres = Column(String(200), unique=False, nullable=False)
    steamspy_tags = Column(String(200), unique=False, nullable=False)
    achievements = Column(Integer, unique=False, nullable=False)
    positive_ratings = Column(Integer, unique=False, nullable=False)
    negative_ratings = Column(Integer, unique=False, nullable=False)
    average_playtime = Column(Integer, unique=False, nullable=False)
    median_playtime = Column(Integer, unique=False, nullable=False)
    owners = Column(String(200), unique=False, nullable=False)
    price = Column(Float, unique=False, nullable=False)

    def __repr__(self):
        return '<Steam %r>' % self.name


def create_db(real_engine_string):
    """Function to create the database
    Args:
        real_engine_string (string): argument to specify whether to generate database locally or at RDS
    Returns:
        N/A
    """
    engine_string = generate_engine_string(real_engine_string)
    # set up mysql connection
    engine = sql.create_engine(engine_string)

    # create the steam table
    Base.metadata.create_all(engine)
    logger.info("Database created.")


