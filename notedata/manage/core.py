import os
import sqlite3
import time

from notetool.download import download
from notetool.tool import log, path_parse, path_join

logger = log(__name__)
conn = None


class Dataset:
    def __init__(self,
                 id=0,
                 name=None,
                 urls=None,
                 md5=None,
                 path=None,
                 size=None
                 ):
        self.id = id
        self.name = name
        self.urls = urls
        self.md5 = md5
        self.path = path
        self.size = size

    def __str__(self):
        return "id:{}, name:{}, urls={}, path={}".format(self.id, self.name, self.urls, self.path)


class DatasetManage:
    def __init__(self, db_path=None, path_root=None):
        self.db_path = db_path or os.path.join(os.path.realpath(os.path.dirname(__file__)), "dataset.db")
        global conn
        self.conn = conn or sqlite3.connect(self.db_path)
        conn = self.conn
        self.cursor = self.conn.cursor()
        self.table_name = 'dataset_detail'
        self.path_root = path_root or path_parse('~/tmp/dataset/')
        self.__init()

    def __init(self):
        self.execute("""create table if not exists {} (
            id                  integer  primary key AUTOINCREMENT
           ,name                varchar(200)
           ,urls                varchar(200)
           ,md5                 varchar(200)  DEFAULT ('')
           ,path                varchar(200)  DEFAULT ('')           
           ,size                integer       DEFAULT (0)
           ,download            integer       DEFAULT (0)
           )
        """.format(self.table_name))

    def execute(self, sql):
        info(sql)
        time.sleep(0.1)
        self.conn.commit()
        return self.cursor.execute(sql)

    def close(self):
        self.cursor.close()
        self.conn.close()

    def print(self):
        print(self.cursor.rowcount)

    def all(self):
        res = self.execute("""select * from  {}""".format(self.table_name))

        for line in res:
            print(line)

        return res

    def insert(self, data: Dataset):
        if self.exists_in_table(data):
            info("dataset exist, update it.")
            self.update(data)
            return
        else:
            info("dataset not exist, create it.")
            self.execute(
                """insert into {} (name, urls, md5, path, size) values ('{}','{}','{}','{}','{}')""".format(
                    self.table_name, data.name, data.urls, data.md5, data.path, data.size)
            )
            return True

    def update(self, data: Dataset):
        self.execute("UPDATE {} set {} where name='{}'".format(self.table_name,
                                                               self.condition(data, sep=','),
                                                               data.name))

        return True

    def dataset(self, name):
        file = list(self.execute("select id,name,urls,md5,path,size from  {} where name='{}'".format(self.table_name,
                                                                                                     name)))

        if len(file) == 0:
            info("dataset not exist!(name={})".format(name))
            return None
        file = file[0]
        data = Dataset(id=file[0],
                       name=file[1],
                       urls=file[2],
                       md5=file[3],
                       path=path_join(self.path_root, file[4]),
                       size=file[5])
        return data

    @staticmethod
    def condition(data: Dataset, sep=' and '):
        conf = []
        # conf.append("id='{}'".format(data.id)) if data.id == 0 else None
        conf.append("name='{}'".format(data.name)) if data.name else None
        conf.append("urls='{}'".format(data.urls)) if data.urls else None
        conf.append("md5='{}'".format(data.md5)) if data.md5 else None
        conf.append("path='{}'".format(data.path)) if data.path else None
        conf.append("size='{}'".format(data.size)) if data.size else None
        return sep.join(conf)

    def exists(self, data: Dataset):
        res = self.execute("""select * from  {} where {}""".format(self.table_name, self.condition(data)))
        for _ in res:
            return True

        return False

    def exists_in_table(self, data: Dataset):
        res = self.execute('select * from  {} where name="{}"'.format(self.table_name, data.name))
        for _ in res:
            return True

        return False

    def download(self, name, overwrite=False) -> Dataset:
        data = self.dataset(name)
        if data is None:
            return None

        download(data.urls, path=data.path, overwrite=overwrite)
        self.execute("UPDATE {} set download = 1 where name='{}'".format(self.table_name, name))

        return data
