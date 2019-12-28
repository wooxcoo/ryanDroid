# -*- coding: utf8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.util.mysql_conn import getSqlConn

# sessionmaker生成一个session类
# todo： access 可以替换这个连接源
engine = getSqlConn()
Session = sessionmaker(bind=engine)
dbSession = Session()

Base = declarative_base(engine)

