import csv
import psycopg2
from dotenv import load_dotenv
import os

#######################################
# TEST: DATABASE CREATION AND CONNECTION
# delete later

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

def check_database():
    try:
        with get_connection() as conn:
            print("Connection successful!")

    except Exception as e:
        print(f"Connection failed: {e}")

check_database()

def create_tables():
    conn = get_connection() # Call the get_connection() function
    cur = conn.cursor() # Call the cursor method against the 'conn' object

    # Create a table using the cursor's execute method
    cur.execute("""
        CREATE TABLE IF NOT EXISTS couriers (
            courier_id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT NOT NULL
        );
    """)
    
    conn.commit() # Commit changes to DB
    cur.close() # Close cursor
    conn.close() # Close connection
    print("Table created successfully!")
    
#create_tables() # Call function    

def dummy_values_load():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO couriers (name, phone) VALUES
        ('Alice Johnson', '07123456789'),
        ('Bob Smith', '07234567890'),
        ('Charlie Brown', '07345678901');
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Dummy Values loaded")

#dummy_values_load()

#########################################    



def print_courier_menu():
    print("\n ----- Courier Menu -----")
    print("|\t\t\t|")
    print("| 1. Print Courier list\t|")
    print("| 2. Add Courier\t|")
    print("| 3. Update Courier\t|")
    print("| 4. Remove Courier\t|")
    print("| 0. Main Menu\t\t|")
    print("|\t\t\t|")
    print("------------------------")


def load_couriers():
    """Load couriers from couriers.txt file"""
    couriers = []
    try:
        with open('couriers.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                courier = {
                    'name': row['name'],
                    'phone': row['phone']
                }

                couriers.append(courier)
                
    except FileNotFoundError:
        print("Courier not found. Using default couriers.")
        couriers = [
            {"name": "John",
             "phone": "071111111111"},
            {"name": "Mark",
             "phone": "072222222222"} 
        ]
    return couriers


def save_couriers(couriers):
    """Save couriers back to couriers.txt file"""
    try:
        with open('couriers.csv', 'w', newline='') as csvfile:
            fieldnames = ['name', 'phone']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for courier in couriers:
                writer.writerow({'name': courier['name'], 'phone': courier['phone']})

    except Exception as e:
        print(f"Error saving couriers: {e}")

# def print_courier_list(courier_list):
#     if len(courier_list) == 0:
#             print("WARNING - Courier list is empty returning back to menu")
            
#     else:
#         for courier in enumerate(courier_list):
#             print(courier)

def print_courier_list():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT * FROM couriers
                    ORDER BY courier_id ASC        
                """)

                couriers = cur.fetchall()
                if couriers:
                    print(couriers)
                else:
                    print(f'No Couriers')

    except Exception as e:
        print(f'Error: {e}')

print_courier_list()

def print_courier(courier_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                sql = """
                SELECT * FROM couriers
                WHERE courier_id = %s"""
                cur.execute(sql, (courier_id,))

                courier = cur.fetchone()

                if courier:
                    print(courier)

                else:
                    print("Courier doesn't exist")

    except Exception as e:
        print(f'Error: {e}')

print_courier(4)

def add_courier():
    # Ask user to enter a name and a phone number
    new_courier = input("Enter the name of courier: ")          
    new_courier_phone = input("Enter the phone number of courier: ")
    try: 
        with get_connection() as conn:
            with conn.cursor() as cur:
                sql = "INSERT INTO couriers (name, phone) VALUES (%s, %s)"
                cur.execute(sql, (new_courier, new_courier_phone))
                conn.commit()

    except Exception as e:
        print(f"Error: {e}")

# add_courier()

# def update_courier(courier_list):
#     while True:
#         if len(courier_list) == 0:
#             print("WARNING - Courier list is empty returning back to menu")
#             break
        
#         else:
#             print_courier_list(courier_list)
#             try:
#                 index = int(input("Enter index to update: "))
#                 print(courier_list[index])      # catch index error immediately

#                 # Ask user for courier name and phone number and put values in a dict
#                 new_name = input("Enter a new name: ")
#                 new_phone_num = input("Enter a new phone number: ")
#                 updated_courier = {
#                     'name': new_name,
#                     'phone': new_phone_num
#                 }
#                 # Check if courier already exist 
#                 if updated_courier not in courier_list:
#                     courier_list[index] = updated_courier
#                     print ("Updated Sucessfully")
#                     break

#                 else:
#                     print ("Courier already exists")
#                     break
                        
#             except Exception as e:
#                 print(f"Error: {e}")

def update_courier_name(id_choice, new_name):
    try: 
        with get_connection() as conn:
            with conn.cursor() as cur:
                sql = """
                UPDATE couriers
                SET name = %s
                WHERE courier_id = %s
                """
                cur.execute(sql, (new_name, id_choice))
                conn.commit()

    except Exception as e:
        print(f"Error: {e}")

def update_courier_phone(id_choice, new_phone):
    try: 
        with get_connection() as conn:
            with conn.cursor() as cur:
                sql = """
                UPDATE couriers
                SET phone = %s
                WHERE courier_id = %s
                """
                cur.execute(sql, (new_phone, id_choice))
                conn.commit()

    except Exception as e:
        print(f"Error: {e}")




def update_courier():
    print_courier_list()

    id_choice = input("Enter the id of a courier you want to update: ")
    
    if id_choice != "":
        print_courier(id_choice)

        new_courier_name = input("Enter a new name (leave blank to keep old): ")

        if new_courier_name != "":
            update_courier_name(id_choice=id_choice, new_name=new_courier_name)

        new_courier_phone = input("Enter a new phone number (leave blank to keep old): ")

        if new_courier_phone != "":
            update_courier_phone(id_choice=id_choice, new_phone=new_courier_phone)



# update_courier()
                            
# def remove_courier(courier_list):
# while True:
#     if len(courier_list) == 0:
#         print("WARNING - Courier list is empty returning back to menu")
#         break

#     else:
#         print_courier_list(courier_list)
#         try:
#             index = int(input("Enter index to delete: "))
#             print(courier_list[index])      # catch index error immediately

#             courier_list.pop(index)
#             print("Courier Deleted")
#             break
#         except Exception as e:
#             print(f"Error: {e}")

def remove_courier():
    # while True:
        print_courier_list()
        delete_id = input("Enter the id of courier to delete: ")
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    sql = """DELETE FROM couriers
                    WHERE courier_id = %s"""
                
                    cur.execute(sql, (delete_id,))
                    print("Courier deleted")
                    # break

        except Exception as e:
            print(f"Error: {e}")
    
# remove_courier()


def courier_menu():
    while True:
        print_courier_menu()
        courier_choice = input("Enter Option: ")

        if courier_choice == "0":
            break

        elif courier_choice == "1":
            print_courier_list()
            
        elif courier_choice == "2":
            add_courier()            
            
        elif courier_choice == "3":
            update_courier()
            
        elif courier_choice == "4":
            remove_courier()

        else: 
            print ("Invalid Input")


# Ideas:
# - add a function that drops data from tables so we can start with a clean test env