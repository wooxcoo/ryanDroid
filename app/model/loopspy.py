from app.model.baseModel import Base, dbSession

import datetime
from sqlalchemy import Column, Integer, DateTime, Boolean, Text


class LoopspyTable(Base):
    """
    sql / access should be the same structure
    change with the real requirement
    """
    __tablename__ = 'loopspy'


    """
    CREATE TABLE `loopspy` (
      `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
      `valid` tinyint(1) DEFAULT '1' COMMENT '1 if valid or others if not',
      `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
      `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      `SignalNumber` text NOT NULL,
      `VOITHSignalNumber` text COMMENT 'text, ignore length current now',
      `Area` text,
      `Language1` text,
      `Language2` text,
      `hierarchy` text,
      `chart` text,
      `block` text,
      `block_comment` text,
      `create_block_icon` text,
      `block_icon` text,
      `ocm_possible` text,
      `readback_allowed` text,   
      `block_type` text,
      `block_group` text,
      PRIMARY KEY (`id`),
      KEY `idx_created_at` (`created_at`),
      KEY `idx_updated_at` (`updated_at`)
    ) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COMMENT='try';
    """
    id = Column(Integer, primary_key=True, autoincrement=True, comment='id')
    valid = Column(Boolean(True), nullable=False,  comment='用户名')
    created_at = Column(DateTime, default=datetime.datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.datetime.now, comment='修改时间')
    SignalNumber = Column(Text, nullable=False)
    VOITHSignalNumber = Column(Text, nullable=True)
    Area = Column(Text, nullable=True)
    Language1 = Column(Text, nullable=True)
    Language2 = Column(Text, nullable=True)
    # original data
    hierarchy = Column(Text, nullable=True)
    chart = Column(Text, nullable=True)
    block = Column(Text, nullable=True)
    block_comment = Column(Text, nullable=True)
    create_block_icon = Column(Text, nullable=True)
    block_icon = Column(Text, nullable=True)
    ocm_possible = Column(Text, nullable=True)
    readback_allowed = Column(Text, nullable=True)
    block_type = Column(Text, nullable=True)
    block_group = Column(Text, nullable=True)

    @classmethod
    def insert_one(cls, **param):
        # insert dict, store into db
        row = LoopspyTable(**param)
        dbSession.add(row)
        dbSession.commit()

    @classmethod
    def insert_batch(cls, data_list, batch_cnt=100):
        """
        batch insert
        :param data_list: input as a list
        :param batch_cnt:  commit once batch reach the cnt
        :return:
        """
        cnt = 0
        for item in data_list:
            row = LoopspyTable(**item)
            dbSession.add(row)
            cnt+=1
            if cnt >= batch_cnt:
                dbSession.commit()
                cnt = 0
        dbSession.commit()


# unit test
if __name__ == '__main__':
    # test
    row = {
        "valid": True,
        "SignalNumber": "SignalNumber",
        "VOITHSignalNumber": "VOITHSignalNumber",
        "Area": "Area",
        "hierarchy": "Hierarchy"
    }
    row = LoopspyTable(**row)
    dbSession.add(row)
    dbSession.commit()