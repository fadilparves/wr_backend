import pymysql
from sqlalchemy import create_engine
from privateconfig import db_host, db_pw, db_user

def connect():
    cnx = create_engine('mysql+pymysql://{}:{}@{}/wr_prod'.format(db_user, db_pw, db_host))
    return cnx