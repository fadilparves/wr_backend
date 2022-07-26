import pymysql
from sqlalchemy import create_engine
from privateconfig import db_host, db_pw, db_user

def connect():
    try:
        cnx = create_engine('mysql+pymysql://{}:{}@{}:3306/wr_prod'.format(db_user, db_pw, db_host))
        return cnx
    except Exception as e:
        print(e)
        return None