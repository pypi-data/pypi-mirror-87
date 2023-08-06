import fire
import snowflake.connector
import configparser
import secrets
import pathlib

class Bufu():
    def connect(self):
        cp = configparser.ConfigParser()
        path = pathlib.Path('~/.snowsql/config')
        cp.read(path.expanduser())
        conn = snowflake.connector.connect(
            user = cp['connections']['username'],
            password = cp['connections']['password'],
            account = cp['connections']['accountname'],
            database = cp['connections']['database'],
            schema = cp['connections']['schema'],
            role = cp['connections']['rolename'],
            warehouse = cp['connections']['warehouse']
        )
        return conn

    def __init__(self):
        self.conn = self.connect()

    def show(self, stage=None):
        cur = self.conn.cursor(snowflake.connector.DictCursor)
        if stage is None:
            try:
                cur.execute('SHOW STAGES IN SCHEMA')
                rs = cur.fetchmany(100)
                for row in rs:
                    print(row['name'])
            finally:
                self.conn.close()
        else:
            try:
                cur.execute(f'LIST @{stage}')
                rs = cur.fetchmany(100)
                for row in rs:
                    print(row['name'])
            finally:
                self.conn.close()

    def put(self, file, stage=None):
        path = pathlib.Path(file)
        cur = self.conn.cursor()
        if stage is None:
            stage = f'bufu_{secrets.token_hex(8)}'
            cur.execute(f'CREATE STAGE {stage}')
            print(f'Stage "{stage}" created.')
        try:
            cur.execute(f'put {path.resolve().as_uri()} @{stage}')
            print(f'File "{path.resolve()}" was uploaded to stage "{stage}".')
        finally:
            self.conn.close()

    def create(self, stage):
        try:
            cur = self.conn.cursor()
            cur.execute(f'CREATE STAGE {stage}')
            print(f'Stage "{stage}" created.')
        finally:
            self.conn.close()

def main():
    try:
        b = Bufu()
        fire.Fire({
            'show': b.show,
            'create': b.create,
            'put': b.put
        })
    finally:
        b.conn.close()
