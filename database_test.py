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
               create table if not exists products (
               id serial primary key,
               name text not null,
               price numeric(10,2) not null
               )
               ''') # execute the sql statement to create the products table;
    cur.execute('''
                create table if not exists couriers (
                id serial primary key,
                name text not null,
                phone_number integer not null
                )
                ''') # execute the sql statement to create the couriers table;
    cur.execute('''
                create table if not exists orders (
                id serial primary key,
                customer_name text not null,
                customer_address text not null,
                customer_phone integer not null,
                courier_id integer references couriers(id),
                status text not null,
                items integer not null references products(id)
                )
                ''') # execute the squl statement to create the orders table;  

    with open('Orders.csv', 'r') as f:
      next(f)  # Skip header
      cur.copy_from(f, 'orders', sep=',', null='', 
                    columns=('customer_name', 
                             'customer_address',
                               'customer_phone',
                                 'courier_id',
                                   'status',
                                     'items'))
    conn.commit() # commit chages to DB
    cur.close() # close cursor
    conn.close() # close connection
    print("Table created successfully")

create_table()

