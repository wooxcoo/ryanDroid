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
      `VOITHSignalNumber` text NOT NULL COMMENT 'text, ignore length current now',
      `Area` text NOT NULL,
      `Language1` text NOT NULL,
      `Language2` text NOT NULL,
      `Hierarchy` text NOT NULL,
      `Chart` text,
      `Block` text,
      `Block_comment` text,
      `Create_block_icon` text,
      `Block_icon` text,
      `OCM_possible` text,
      `Block_type` text,
      `Block_group` text,
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
    VOITHSignalNumber = Column(Text, nullable=False)
    Area = Column(Text, nullable=False)
    Language1 = Column(Text, nullable=False, default="")
    Language2 = Column(Text, nullable=False, default="")
    # original data
    Hierarchy = Column(Text, nullable=False)
    Chart = Column(Text, nullable=True)
    Block = Column(Text, nullable=True)
    Block_comment = Column(Text, nullable=True)
    Create_block_icon = Column(Text, nullable=True)
    Block_icon = Column(Text, nullable=True)
    OCM_possible = Column(Text, nullable=True)
    Block_type = Column(Text, nullable=True)
    Block_group = Column(Text, nullable=True)

    def insert_one(cls, **param):
        # insert dict, store into db
        row = LoopspyTable(**param)
        dbSession.add(row)
        dbSession.commit()

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
        "Hierarchy": "Hierarchy"
    }
    row = LoopspyTable(**row)
    dbSession.add(row)
    dbSession.commit()