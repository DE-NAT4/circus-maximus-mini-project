import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host =os.getenv('postgres_host'),
        port = os.getenv('postgres_port'),
        database= os.getenv('postgres_db'),
        user = os.getenv('postgres_user'),
        password = os.getenv('postgres_password')

    )
def create_table():
    conn = get_connection() # call the get connection function to establish a connection
    cur = conn.cursor() # call the cursor method aginst the 'conn' object

    cur.execute('''
               create table if not exists more_products (
               id serial primary key,
               name text not null,
               price numeric(10,2) not null
               )
               ''') # execute the sql statement to create a table;
    conn.commit() # commit chages to DB
    cur.close() # close cursor
    conn.close() # close connection
    print("Table created successfully")

create_table()