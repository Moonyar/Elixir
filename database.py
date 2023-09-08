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


def get_all_cfls(start_date, end_date):
    with engine.connect() as conn:
        query = text("SELECT * FROM cfls WHERE updated_at BETWEEN :start AND :end")
        records = conn.execute(query, {'start': start_date, 'end': end_date}).fetchall()

    if len(records) == 0:
        return None
    else:
        all = []
        for row in records:
            all.append(dict(row._mapping))

    return all


def update_cfl(cfl_id, data):
    with engine.connect() as conn:
        query = text("""
            UPDATE cfls SET 
            partner = :partner_name, 
            leader = :leader_name, 
            item = :item, 
            reason = :reason, 
            breakdown = :breakdown, 
            solution = :solution
            WHERE id = :cfl_id
        """)

        conn.execute(query, {
            "cfl_id": cfl_id,
            "partner_name": data['partner_name'],
            "leader_name": data['leader_name'],
            "item": data['item'],
            "reason": data['cfl_reason'],
            "breakdown": data['breakdown'],
            "solution": data['solution']
        })


def delete_cfl(cfl_id):
    with engine.connect() as conn:
        query = text("DELETE FROM cfls WHERE id = :cfl_id")
        conn.execute(query, {"cfl_id": cfl_id})
