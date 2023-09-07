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


def load_cfl(id):
    with engine.connect() as conn:
        result = conn.execute(text("select * from cfls where id = :cfl_id"), {"cfl_id": id})

        rows = result.all()
        if len(rows) == 0:
            return None
        else:
            return rows[0]._asdict()

def add_cfl(data):
    with engine.connect() as conn:
        query = text(
            "INSERT INTO cfls (partner, leader, item , reason, breakdown, solution) VALUES (:partner_name, :leader_name, :item, :reason, :breakdown, :solution)")

        conn.execute(query, {"partner_name": data['partner_name'],
                             "leader_name": data['leader_name'],
                             "item": data['item'],
                             "reason": data['cfl_reason'],
                             "breakdown": data['breakdown'],
                             "solution": data['solution']})
        result = conn.execute(text("SELECT LAST_INSERT_ID()"))
        return result.fetchone()[0]