import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask

app = Flask(__name__)
class Database:
    def __init__(self):
        self.credentials=dict(dbname='',host='localhost', user='postgres', password='y0ng5un1')
        if app.config.get('ENV')=='development':
            self.credentials['dbname']='yongsun1'
        
        if app.config.get('ENV')=='production':
            self.credentials['dbname']='d6eqjp9bgo8p68'
            self.credentials['host']='ec2-54-83-55-115.compute-1.amazonaws.com'
            self.credentials['user']='tnswtibitipkpo'
            self.credentials['password']='1cf67e757dbe06117a2fed90cb34aa00a43602f3e7608842f1cc46c09587f2ef'

        try:
            self.conn = psycopg2.connect(**self.credentials, cursor_factory=RealDictCursor)
            self.cur = self.conn.cursor()
            self.conn.autocommit = True
            print('You have successfully connected.')
        except:
            print('failed to connect')