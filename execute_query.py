import configparser as cp
from sqlalchemy import create_engine, text
import pandas as pd

class ExecuteQuery:

    """
    Usage:

        1st, to read the databse configration file to conntect databse;
        2nd, to read the sql query file and coovert to text format;
        3rd, to run the sql query and return a dataframe
    """

    def __init__(self, db: str, config: str, query: str, par=None):
        
        self.db = db
        self.config = config
        self.query = query
        self.par = par

    def db_connect(self):
        config = cp.ConfigParser()
        config.read(self.config)
        db_type = config[self.db]['type']
        db_name = config[self.db]['database']
        db_user = config[self.db]['user']
        db_passwd = config[self.db]['password']
        db_host = config[self.db]['host']
        db_port = config[self.db]['port']
        connect_args = {
                        'connect_timeout': 60,
                        'read_timeout': 90
                       }
        engine = create_engine(f'{db_type}://{db_user}:{db_passwd}@{db_host}:{db_port}/{db_name}',connect_args = connect_args)
        return engine


    def read_query(self):
        if self.par == None:
            with open(self.query,'r',encoding = 'utf8') as f:
                query = "".join(f.readlines())
                stmt = text(query)
        else:
            with open(self.query,'r',encoding = 'utf8') as f:
                query = "".join(f.readlines())
                stmt = text(query).bindparams(**self.par)
        return stmt


    def run(self):
        engine = self.db_connect()
        with engine.connect() as con:
            stmt = self.read_query()
            df = pd.read_sql_query(stmt,con)       
        return df