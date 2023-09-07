import sqlalchemy
import pymysql
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine, text

load_dotenv()

db_connection_string = os.environ.get('db_connection_string')

engine = create_engine(db_connection_string,
                       connect_args={
                           "ssl": {
                               "ssl_ca": "/etc/ssl/cert.pem"
                           }
                       }
                       )