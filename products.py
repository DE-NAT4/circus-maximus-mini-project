import csv
import os
from dotenv import load_dotenv
import csv
import psycopg2


def print_product_menu():
    print("\n ------ Products Menu ------")
    print("|\t\t\t|")
    print("| 1. Products list\t|")
    print("| 2. Add product\t|")
    print("| 3. Update product\t|")
    print("| 4. Remove product\t|")
    print("| 0. Main Menu\t\t|")
    print("|\t\t\t|")
    print("------------------------")


def save_products(products):
    #Save products back to Products.txt file
    try:
        with open('Products.csv', 'w') as file:
            headers = ["Name","Price"]
            f = csv.DictWriter(file, fieldnames=headers)
            f.writeheader()
            f.writerows(products)
    except Exception as e:
        print(f"Error saving products: {e}")


# def load_products():
#     #Load products from Products.txt file
#     products = []
#     try:
#         file = open("Products.csv", "r")
#         f = csv.DictReader(file)
#         for dictonary in f:
#             products.append(dictonary)
#     except FileNotFoundError:
#         print("Product not found. Using default products.")
#         products = [
#         {"Name":"Tea",
#         "Price":2.99},
#         {"Name":"Latte",
#         "Price":1.99}
#         ]

    return products
        

def product_menu():
            while True:
                print_product_menu()
                product_choice = input("Enter option: ")

                if product_choice == "0":
                    break

                elif product_choice == "1":
                    # print(products_list)
                    retrieve_products()
                    
                elif product_choice == "2":
                    while True:
                        # Gets input for a new product and inserts it into database
                        # MISSING ERROR HANDLING
                        try:         
                            new_product = input("Enter new product name: ")
                            new_product_price = float(input("Enter a price for this product: "))
                            insert_products(new_product, new_product_price)
                            break
                        except: ValueError
                        print("Please enter a new product")
                            
                elif product_choice == "3":
                    while True:
                        # Calls upon functions to print the database and update either name or price using the previously selected id. If it is blank it will pass the function to update 
                        #MISSING ERROR HANDLING
                        try:
                            retrieve_products()
                            select_id = (input("Please select an id to update "))
                            print("Product selected: ")
                            retrieve_product(select_id)
                            upd_name = input("Please select a new name - Leave blank to keep ")
                            if upd_name != "":
                                update_products_name(select_id, upd_name)
                                pass
                            else:
                                pass
                            
                                upd_price = float(input("Please select a new price - Leave blank to keep "))
                                if upd_price != "":
                                    update_product_price(select_id, upd_price)
                                    pass
                                else:
                                    pass
                                break
                        except:
                            print("Invalid Input ")
                            cursor.close()
                            break
    




                elif product_choice == "4":
                    while True:
                        retrieve_products()
                        delete_id = (input("please select the ID of what you want to delete "))
                        delete_product(delete_id)
                        break


####################################################################
#Database code - Some will be replaced when merged
#WARNING UNTIL MAIN DATABASE IS MADE A TEMPORARY TABLE IS NEEDED below is the code needed to test this
# CREATE TABLE products (
#     product_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
#     product_name VARCHAR(255),
#     product_price FLOAT
# );




load_dotenv()
host_name = os.environ.get("POSTGRES_HOST")
database_name = os.environ.get("POSTGRES_DB")
user_name = os.environ.get("POSTGRES_USER")
user_password = os.environ.get("POSTGRES_PASSWORD")



conn_string = f'host={host_name} dbname={database_name} user={user_name} password={user_password}'
# Establish a database connection
try:
    with psycopg2.connect(conn_string) as connection:

        # print('Opening cursor...')
        cursor = connection.cursor()
except:
    print("WARNING - Failed to connect to database ")

def insert_products(new_product, new_product_price):
    cursor = connection.cursor()
    insert = '''
    INSERT INTO products (product_name, product_price)
    VALUES (%s,%s)
    '''

    cursor.execute(insert, (new_product, new_product_price))
    connection.commit()

    cursor.close()

def retrieve_products():
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM products')
    print(cursor.fetchall())
    cursor.close()

def retrieve_product(select_id):
        cursor = connection.cursor()
        product_pull = '''SELECT * FROM products
        WHERE product_id = %s'''
        cursor.execute(product_pull, select_id)
        print(cursor.fetchall())
        cursor.close()

        

def update_products_name(select_id, upd_name):
    cursor = connection.cursor()
    
    update = '''
    UPDATE products
    SET product_name =%s
    WHERE product_id = %s
    '''
    cursor.execute(update, (upd_name, select_id))
    connection.commit()
    
    cursor.close()

def update_product_price(select_id, upd_price):
    cursor = connection.cursor()
    
    update = '''
    UPDATE products
    SET product_price =%s
    WHERE product_id = %s
    '''
    cursor.execute(update, (upd_price, select_id))
    connection.commit()
    
    cursor.close()


def delete_product(delete_id):
    cursor = connection.cursor()
    delete = 'DELETE FROM products WHERE product_id =%s'
    cursor.execute(delete, (delete_id))
    
    connection.commit()
    
    cursor.close()