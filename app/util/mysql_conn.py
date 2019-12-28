# -*- coding: utf8 -*-

from sqlalchemy import create_engine

# config

HOSTNAME = '127.0.0.1'
PORT = '3301'
DATABASE = 'ryan_test'
USERNAME = 'root'
PASSWORD = 'admin'

def getSqlConn(user=USERNAME, pwd=PASSWORD, hostname=HOSTNAME, port=PORT, database=DATABASE):
    db_url = 'mysql+pymysql://{username}:{password}@{hostname}:{port}/{database}?charset=utf8'.format(
        username=user,
        password=pwd,
        hostname=hostname,
        port=port,
        database=database
    )

    engine = create_engine(db_url)
    connection = engine.connect()
    return connection


# unit test
if __name__ == '__main__':
    getSqlConn()