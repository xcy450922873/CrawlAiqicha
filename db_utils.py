import pymysql

"""
    class CompanyMessage：
        get_conn：返回数据库连接实例
"""


class CompanyMessage:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CompanyMessage, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', password='root',
                                    database='company_message')

    def execute(self, sql, return_type='all'):
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            if return_type != 'all':
                return cursor.fetchone()
            return cursor.fetchall()

    def commit(self, sql, return_type='all'):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                self.conn.commit()
                if return_type != 'all':
                    return cursor.fetchone()
                return cursor.fetchall()
        except pymysql.err.InternalError as e:
            print(f"InternalError occurred: {e}")
            self.conn.rollback()

    def executeWithParams(self, sql, params, return_type='all'):
        with self.conn.cursor() as cursor:
            cursor.execute(sql, params)
            self.conn.commit()
            if return_type != 'all':
                return cursor.fetchone()
            return cursor.fetchall()