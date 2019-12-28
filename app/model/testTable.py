from app.model.baseModel import Base, dbSession

import datetime
from uuid import uuid4
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text

class TestTable(Base):
    """
    just for test
    """
    __tablename__ = 'test_table'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='id')
    valid = Column(Boolean(True), nullable=False,  comment='用户名')
    created_at = Column(DateTime, default=datetime.datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.datetime.now, comment='修改时间')
    SignalNumber = Column(Text, nullable=True, comment='用户密码')


# unit test
if __name__ == '__main__':
    row = TestTable(valid=True, SignalNumber="123")
    dbSession.add(row)
    dbSession.commit()