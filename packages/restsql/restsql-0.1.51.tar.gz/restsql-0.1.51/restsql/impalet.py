import time
from impala.dbapi import connect
from peewee import Database, Context
import logging

logger = logging.getLogger("impalet")

class ImpalaClient(object):
    def __init__(self, host, port=21050, database=None):
        self.host = host
        self.port = int(port or 21050)
        self.database = database
        self.conn = None

    def get_conn(self):
        return connect(host=self.host, port=self.port, database=self.database)

    def run_sql(self, sql):
        start = time.time()
        conn = self.get_conn()
        cursor = conn.cursor()
        logger.info("ImpalaClient: Run sql: %s", sql)
        if isinstance(sql, tuple):
            sql_rep = sql[0].replace("?", "{}")
            cursor.execute(sql_rep.format(*sql[1]))
        else:
            cursor.execute(sql)
        table_description = cursor.description
        results = cursor.fetchall()
        cursor.close()
        records = ImpalaClient.parse_records(results, table_description)
        logger.info("ImpalaClient: Get records: %s", len(records))
        logger.debug("ImpalaClient: Time cost: %s", time.time() - start)
        return records

    @staticmethod
    def parse_records(results, description):
        records = []
        for row in results:
            record = {}
            for index, value in enumerate(row):
                record[description[index][0]] = value
            records.append(record)
        return records


class ImpalaContext(Context):
    def __init__(self, **settings):
        settings["quote"] = "``"
        super(ImpalaContext, self).__init__(**settings)


class ImpalaDatabase(Database):
    context_class = ImpalaContext

    def init(self, database, **kwargs):
        super(ImpalaDatabase, self).init(database, **kwargs)

