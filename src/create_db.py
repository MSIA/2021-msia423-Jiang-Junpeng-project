from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, MetaData
import sqlalchemy as sql
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel("INFO")

Base = declarative_base()


def generate_engine_string():
    conn_type = "mysql+pymysql"
    user = os.environ.get("MYSQL_USER")
    password = os.environ.get("MYSQL_PASSWORD")
    host = os.environ.get("MYSQL_HOST")
    port = os.environ.get("MYSQL_PORT")
    database = os.environ.get("DATABASE_NAME")
    engine_string = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, database)

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


def create_db():
    engine_string = generate_engine_string()
    # set up mysql connection
    engine = sql.create_engine(engine_string)

    # create the steam table
    Base.metadata.create_all(engine)
    logger.info("Database created.")


