# -*- coding: utf8 -*-
from sqlalchemy import func
from zhongkui.core.utils.lex_yacc import syntax_token
from zhongkui.core.utils.store import table


class BaseModel(object):
    __table_name__ = None

    def __init__(self, raw_data):
        self.__raw_data__ = self.convert_row_proxy_to_dict(raw_data)
        for key, value in self.__raw_data__.items():
            setattr(self, key, value)

    def __repr__(self):
        return "<{cls_name}: {id}, {raw_data}>".format(cls_name=self.__class__.__name__,
                                                       id=self.id,
                                                       raw_data=str(self.__raw_data__))

    def get_uuid(self):
        return '%s:%s' % (self.__table_name__, self.id)

    @classmethod
    def _get_table(cls):
        assert cls.__table_name__ is not None, 'table name can not be null'
        return getattr(table, cls.__table_name__)

    @classmethod
    def get(cls, pk):
        return cls.get_no_cache(pk)

    @classmethod
    def get_no_cache(cls, pk):
        t = cls._get_table()
        q = t.select().where(t.primary_key.columns._all_columns[0] == pk)
        raw_data = table.execute(q).first()
        return cls(raw_data) if raw_data else None

    @classmethod
    @use_master_db
    def get_use_master_db(cls, pk):
        return cls.get_no_cache(pk)

    @classmethod
    def gets_by(cls, only_fields=None, **kwargs):
        r""" 根据各种条件获取 instance list.
        先从 database 里获取 主键，再利用主键逐个获取 instance.
        query syntax support: __gt, __gte, __in, etc; more information in lex_yacc.py

        Usage:
            from from lived.models.trade import Order
            all_order = Order.gets_by()                             # 获取所有订单
            paid_order = Order.gets_by(status=ORDER_STATUS.PAID)    # 获取所有支付订单

            orders = Order.gets_by(id__gt=2)                        # 获取所有大于
        """
        if only_fields:
            assert isinstance(only_fields, list), 'only_fields must be list'
            assert all([isinstance(i, (str, unicode)) for i in only_fields]), 'fields must be str or unicode'
        t = cls._get_table()
        select_sql = t.select().with_only_columns(
            columns=[getattr(t.c, i) for i in only_fields] if only_fields else [t.primary_key.columns._all_columns[0]])
        count_sql = t.count()
        with_total = bool(kwargs.pop('with_total', False))
        total = 0

        offset = kwargs.pop('offset', None)
        limit = kwargs.pop('limit', None)

        for key, value in kwargs.items():
            select_sql = syntax_token.handle(t, select_sql, key, value)
            if with_total:
                count_sql = syntax_token.handle(t, count_sql, key, value)

        if with_total:
            total = table.execute(count_sql).scalar()
        if limit is not None and isinstance(limit, int):
            select_sql = select_sql.limit(limit)
            if offset is not None and isinstance(offset, int):
                select_sql = select_sql.offset(offset)

        ints = table.execute(select_sql).fetchall()
        if only_fields:
            return ints
        rets = [cls.get(its[0]) for its in ints]
        return rets if not with_total else (rets, total)

    @classmethod
    def gets_count(cls, **kwargs):
        r""" 根据各种条件获取 条目个数.

        """
        t = cls._get_table()
        count_sql = t.count()
        for key, value in kwargs.items():
                count_sql = syntax_token.handle(t, count_sql, key, value)

        total = table.execute(count_sql).scalar()
        return total

    @classmethod
    def exec_sql_stmt(cls, sql):
        ints = table.execute(sql).fetchall()
        return [cls.get(its[0]) for its in ints]

    @classmethod
    def exec_sql_force(cls, sql):
        return table.execute(sql)

    @classmethod
    def get_only_filed(cls, only_fields, **kwargs):
        return cls.gets_by(only_fields=only_fields, **kwargs)

    @classmethod
    @use_master_db
    def get_by(cls, **kwargs):
        """
        获取第一个元素
        """
        targets = cls.gets_by(limit=1, **kwargs)
        return targets[0] if targets else None

    @classmethod
    @use_master_db
    def count_row(cls, **kwargs):
        t = cls._get_table()
        count_sql = t.select().with_only_columns(columns=[func.count(t.primary_key.columns._all_columns[0])])
        for key, value in kwargs.items():
            count_sql = syntax_token.handle(t, count_sql, key, value)
        return table.execute(count_sql).scalar()

    @classmethod
    @use_master_db
    def save(cls, **values):
        r""" 保存数据到 持久化层 database，redis，file ect.

        Usage:
            from from lived.models.trade import Order
            new_order = Order.save(user_id=10001, status=ORDER_STATUS.UNPAID)
        """
        ins = cls._get_table().insert().values(**values)
        ret = table.execute(ins)
        pk = ret.inserted_primary_key[0]
        return cls.get(pk)

    # instance method & property
    def update(self, **values):
        r""" 更新 instance, 更新后会清理强制使缓存失效.

        Usage:
            from from lived.models.trade import Order
            order = Order.get(870970330028441645)
            order.commit()
        """
        t = self._get_table()
        upd = t.update().values(**values).where(t.primary_key.columns._all_columns[0] == self.id)
        if table.execute(upd).rowcount == 1:
            for k, v in values.items():
                setattr(self, k, v)
            return True
        else:
            return False

    def delete(self):
        t = self._get_table()
        sql = t.delete().where(t.primary_key.columns._all_columns[0] == self.id)
        table.execute(sql)
        return True

    @classmethod
    def model_fields(cls):
        return [column.name for column in cls._get_table().columns]

    @property
    def fields(self):
        r""" 该 model 包含的字段
        :return [filed1, field2, field3...]
        """
        return [column.name for column in self._get_table().columns]

    # help function
    @staticmethod
    def convert_row_proxy_to_dict(raw_data):
        if type(raw_data) == dict:
            return raw_data
        ret = dict()
        keys = raw_data.keys()
        for i in range(len(keys)):
            ret[keys[i]] = raw_data._row[i]
        return ret

    @classmethod
    def get_object_or_404(cls, error_class=NotFound, **kwargs):
        o = cls.gets_by(**kwargs)
        if o:
            return o[0]
        else:
            raise error_class()

    @classmethod
    @use_master_db
    def get_use_master_db_or_error(cls, error_class=NotFound, **kwargs):
        return cls.get_object_or_404(error_class=error_class, **kwargs)
