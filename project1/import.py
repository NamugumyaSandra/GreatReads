import os
import csv
import psycopg2

# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session,sessionmaker

DATABASE_URL=os.getenv('DATABASE_URL')
conn = psycopg2.connect(dbname='yongsun1',host='localhost', user='postgres', password='y0ng5un1')
cur = conn.cursor()

# database engine that manages database connections
# engine = create_engine(os.getenv('DATABASE_URL'))
# # creates a scoped session to ensure that every 
# # user's database interactions are kept separate
# db = scoped_session(sessionmaker(bind=engine))

cur.execute(""" 
CREATE TABLE IF NOT EXISTS users (
    user_id serial PRIMARY KEY,
    username VARCHAR (50) UNIQUE NOT NULL,
    email VARCHAR (100) UNIQUE NOT NULL,
    password VARCHAR NOT NULL
);
CREATE TABLE IF NOT EXISTS books (
    book_id serial PRIMARY KEY,
    isbn VARCHAR UNIQUE NOT NULL,
    title VARCHAR (50)  NOT NULL,
    author VARCHAR (50) NOT NULL,
    year INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS reviews (
    review_id serial,
    reviewer INTEGER REFERENCES users(user_id),
    rated_book INTEGER REFERENCES books(book_id) ON DELETE CASCADE,
    review VARCHAR (250) UNIQUE NOT NULL,
    rating INTEGER NOT NULL CHECK (rating>=1 AND rating<=5),
    PRIMARY KEY (review_id, reviewer, rated_book)
);
""")
conn.commit()
print('Tables created')

def main():
    b= open('books.csv') 
    reader = csv.reader(b)# alternatively in one line, with open('books.csv','r') as f:next(f)
    next(reader)  # skip the header
    for isbn,title,author,year in reader:
        cur.execute('INSERT INTO books(isbn,title,author,year) VALUES(%s,%s,%s,%s)',(isbn,title,author,year))
        conn.commit()
        print('book created')
main()
print('Books created')