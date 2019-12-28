# -*- coding: utf8 -*-

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 网上抄的，需要试下： https://stackoverflow.com/questions/9233912/connecting-sqlalchemy-to-msaccess
def fixup_access():
    import sqlalchemy.dialects.access.base
    class FixedAccessDialect(sqlalchemy.dialects.access.base.AccessDialect):
        def _check_unicode_returns(self, connection):
            return True
        def do_execute(self, cursor, statement, params, context=None, **kwargs):
            if params == {}:
                params = ()
            super(sqlalchemy.dialects.access.base.AccessDialect, self).do_execute(cursor, statement, params, **kwargs)

    class SomeObject(object):
        pass
    fixed_dialect_mod = SomeObject
    fixed_dialect_mod.dialect = FixedAccessDialect
    sqlalchemy.dialects.access.fix = fixed_dialect_mod

fixup_access()

# db_location, 替换成你的
engine = sqlalchemy.create_engine('access+fix://admin@/%s'%(db_location))

Session = sessionmaker(bind=engine)
dbSession = Session()
Base = declarative_base(engine)
