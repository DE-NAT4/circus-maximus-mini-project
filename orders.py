import csv
from select import select
from couriers import load_couriers
#from products import load_products
import os
from dotenv import load_dotenv
import csv
import psycopg2
from products import retrieve_products
from couriers import print_courier_list
from db import get_connection


FIELDNAMES = ['customer_name', 'customer_address', 'customer_phone', 'courier', 'status', 'items']
#STATUSES = ['Pending', 'order received', 'preparing', 'On the way', 'delivered']

def print_order_menu():
    print('\n ---------- Order Menu ---------')
    print('|\t\t\t\t|')
    print('| 1. Print Order Table\t|')
    print('| 2. Add Order to Table\t|')
    print("| 3. Update an Order's Status\t|")
    print("| 4. Update an Order's Details\t|")
    print('| 5. Delete an Order\t\t|')
    print('| 0. Exit to Main Menu\t\t|')
    print('| \t\t\t\t|')
    print('--------------------------------')

# delete
# def read_orders_csv():
#     try:
#         with open('Orders.csv', 'r') as file:
#             reader = csv.DictReader(file, skipinitialspace=True)
#             if reader.fieldnames:
#                 reader.fieldnames = [name.strip() for name in reader.fieldnames if name]
#             return [row for row in reader if any((value or '').strip() for value in row.values())]
#     except FileNotFoundError:
#         return []
#     except Exception as error:
#         print(f'Error reading Orders.csv: {error}')
#         return []

# # delete
# def normalize_order(order, couriers, products):
#     # Normalize courier: if it's an index, convert to name
#     try:
#         courier_index = int(order.get('courier', ''))
#         if 0 <= courier_index < len(couriers):
#             order['courier'] = couriers[courier_index]['name']
#     except (ValueError, TypeError):
#         pass  # Keep as is if not index

#     # Normalize items: if comma-separated indices, convert to names
#     items_str = order.get('items', '')
#     if items_str:
#         try:
#             indices = [int(x.strip()) for x in items_str.split(',') if x.strip()]
#             names = []
#             for idx in indices:
#                 if 0 <= idx < len(products):
#                     names.append(products[idx]['Name'])
#             if names:
#                 order['items'] = ', '.join(names)
#         except (ValueError, TypeError):
#             pass  # Keep as is

#     return order

# #delete
# def parse_index_list(raw_input):
#     try:
#         return [int(x.strip()) for x in raw_input.split(',') if x.strip()]
#     except ValueError:
#         return []

# change
# def choose_courier():
#     couriers = load_couriers()
#     if not couriers:
#         return "No couriers available, please add a courier first."

#     print('Choose a courier:')
#     for i, courier in enumerate(couriers):
#         print(f'{i}: {courier.get("name", "Unnamed courier")} ({courier.get("phone", "")})')
#     try:
#         choice = int(input('Enter courier index: ').strip())
#     except ValueError:
#         return None
#     if 0 <= choice < len(couriers):
#         return couriers[choice]
#     return None

# # change
# def parse_index_list(raw_input):
#     try:
#         return [int(x.strip()) for x in raw_input.split(',') if x.strip()]
#     except Exception:
#         return []



# delete
# def load_orders(couriers, products):
#     return [normalize_order(order, couriers, products) for order in read_orders_csv()]

# keep?
def save_orders(order_list):
    if not order_list:
        return
    try:
        with open('Orders.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()
            for order in order_list:
                writer.writerow({key: order.get(key, '') for key in FIELDNAMES})
    except Exception as error:
        print(f'Unable to save orders: {error}')


def print_status():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            Select * from status
                """)
                statuses = cur.fetchall()
                for status in statuses:
                    print(status)
    except Exception as e:
        print(f'Error: {e}')

# change
# def print_order_list(order_list):
#     if not order_list:
#         print("WARNING - Order list is empty returning back to menu")
#     else:
#         for i, order in enumerate(order_list):
#             print(f"{i}: Customer: {order.get('customer_name', '')}, "
#                   f"Address: {order.get('customer_address', '')}, "
#                   f"Phone: {order.get('customer_phone', '')}, "
#                   f"Courier: {order.get('courier', '')}, "
#                   f"Status: {order.get('status', '')}, "
#                   f"Items: {order.get('items', '')}")

def print_orders():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT * FROM orders
                    ORDER BY order_id ASC        
                """)

                orders = cur.fetchall()
                if orders:
                    for order in orders:
                        print(order)
                else:
                    print(f'No orders')

    except Exception as e:
        print(f'Error: {e}')


def update_order_status():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT * FROM orders
                    ORDER BY order_id ASC        
                """)
                orders = cur.fetchall()
                if not orders:
                    print('No orders available to update.')
                    return False
                for order in orders:
                    print(order)
                order_id = input('Enter the order ID to update: ')
                print('Choose new status:')
                cur.execute("""
                           SELECT DISTINCT status FROM status 
                           """)
                print_status()
                statuses = cur.fetchall()
                status_index = int(input('Enter status index: '))
                if 0 <= status_index < len(statuses):
                    new_status = statuses[status_index][0]
                    cur.execute("""
                        UPDATE orders
                        SET status_id = %s
                        WHERE order_id = %s
                    """, (status_index, order_id))
                    print('Order status updated successfully.')
                    return True
                else:
                    print('Invalid status index.')
    except ValueError:
        print('Please enter a valid number.')
    return False

# change
# def add_order(order_list, couriers, products):
    # customer_name = input('What is the new customer\'s name? ')
    # customer_address = input('What is the address of the customer? ')
    # customer_phone = input('What is the phone number of the customer? ')
    # courier = choose_courier(couriers)
    # status = 'Pending'
    # print('Choose the order status:')
    # for i, status_option in enumerate(STATUSES):
    #     print(f'{i}: {status_option}')
    # try:
    #     status_index = int(input('Enter status index: '))
    #     if 0 <= status_index < len(STATUSES):
    #         status = STATUSES[status_index]
    #     else:
    #         print('Invalid status index, defaulting to Pending.')
    # except ValueError:
    #     print('Invalid status input, defaulting to Pending.')
    # items = choose_products(products)
    # order_list.append({
    #     'customer_name': customer_name,
    #     'customer_address': customer_address,
    #     'customer_phone': customer_phone,
    #     'courier': courier,
    #     'status': status,
    #     'items': items,
    # })
    # print('Order added to list')
    # return True
def add_order():
    while True:
        try:
            new_customer_name = input('What is the new customer\'s name? ')
            new_customer_address = input('What is the address of the customer? ')
            new_customer_phone = int(input('What is the phone number of the customer? '))
            retrieve_products()
            #NEEDS TO BE CHANGED TO WORK WITH STRINGS
            new_order_product = (input("Please select your products using the ID comma seperated: "))
            print_courier_list()
            new_order_courier =  int(input("Please choose your courier using the ID "))
            insert_order(new_customer_name, new_customer_address, new_customer_phone, new_order_product, new_order_courier)
            break
        except: 
            print("Invalid Input")
            cursor.close()
            break


# change
# def delete_order(order_list):
#     if not order_list:
#         print('No orders available to delete.')
#         return False
#     print_order_list(order_list)
#     try:
#         index = int(input('Select order index to delete: '))
#         if 0 <= index < len(order_list):
#             order_list.pop(index)
#             print('Order deleted!')
#             return True
#         print('Invalid index')
#     except ValueError:
#         print('Invalid input')
#     return False

def delete_order():
    print_orders()
    delete_id = input("Enter the id of the order to delete: ")
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                sql = """DELETE FROM orders
                WHERE order_id = %s"""
            
                cur.execute(sql, (delete_id,))
                print("Order deleted")

    except Exception as e:
        print(f"Error: {e}")



# change
def order_menu():
    while True:
        print_order_menu()
        choice = input('Please select an option: ')
        if choice == '0':
            break
        elif choice == '1':
             print_orders()
        elif choice == '2':
            add_order()
        elif choice == '3':
            update_order_status()
        elif choice == '4':
            update_order()
        elif choice == '5':
            delete_order()
        else:
            print('Invalid input')


# if __name__ == "__main__":
#     couriers = load_couriers()
#     #products = load_products()
#     orders = load_orders(couriers, products)
#     order_menu(couriers, products, orders)




load_dotenv()
host_name = os.environ.get("POSTGRES_HOST")
database_name = os.environ.get("POSTGRES_DB")
user_name = os.environ.get("POSTGRES_USER")
user_password = os.environ.get("POSTGRES_PASSWORD")
conn_string = f'host={host_name} dbname={database_name} user={user_name} password={user_password}'

try:
    with psycopg2.connect(conn_string) as connection:

        # print('Opening cursor...')
        cursor = connection.cursor()
except:
    print("WARNING - Failed to connect to database ")

def insert_order(new_customer_name, new_customer_address, new_customer_phone, new_order_product, new_order_courier):
    cursor = connection.cursor()
    insert = '''
    INSERT INTO orders (customer_name, customer_address, customer_phone, courier_id, status_id, products_id)
    VALUES (%s,%s,%s,%s,1,%s)
    '''

    cursor.execute(insert, (new_customer_name, new_customer_address, new_customer_phone, new_order_courier,new_order_product))
    connection.commit()

    cursor.close()


def update_order():

    # SHOW EXISTING ORDERS
    print_orders()

    order_id = input(
        "Enter order ID to update: "
    )

    try:

        with get_connection() as conn:

            with conn.cursor() as cur:

                # =========================
                # GET CURRENT ORDER
                # =========================

                sql = """
                    SELECT
                        customer_name,
                        customer_address,
                        customer_phone,
                        courier_id,
                        products_id
                    FROM orders
                    WHERE order_id = %s;
                """

                cur.execute(sql, (order_id,))

                order = cur.fetchone()

                # CHECK ORDER EXISTS
                if not order:
                    print("Order not found!")
                    return

                # =========================
                # STORE CURRENT VALUES
                # =========================

                current_name = order[0]
                current_address = order[1]
                current_phone = order[2]
                current_courier = order[3]
                current_items = order[4]

                # =========================
                # USER INPUTS
                # =========================

                new_name = input(
                    f"Customer name ({current_name}): "
                )

                new_address = input(
                    f"Customer address ({current_address}): "
                )

                new_phone = input(
                    f"Customer phone ({current_phone}): "
                )

                # =========================
                # SHOW PRODUCTS
                # =========================

                print("\nAVAILABLE PRODUCTS\n")

                cur.execute("""
                    SELECT product_id, product_name, product_price
                    FROM products
                    ORDER BY product_id;
                """)

                products = cur.fetchall()

                for product in products:
                    print(product)

                new_items = input(
                    f"Product IDs ({current_items}): "
                )

                # =========================
                # SHOW COURIERS
                # =========================

                print("\nAVAILABLE COURIERS\n")

                cur.execute("""
                    SELECT courier_id, courier_name, courier_phone
                    FROM couriers
                    ORDER BY courier_id;
                """)

                couriers = cur.fetchall()

                for courier in couriers:
                    print(courier)

                new_courier = input(
                    f"Courier ID ({current_courier}): "
                )

                # =========================
                # KEEP OLD VALUES IF EMPTY
                # =========================

                if new_name == "":
                    new_name = current_name

                if new_address == "":
                    new_address = current_address

                if new_phone == "":
                    new_phone = current_phone

                if new_items == "":
                    new_items = current_items

                if new_courier == "":
                    new_courier = current_courier

                # =========================
                # UPDATE DATABASE
                # =========================

                update_sql = """
                    UPDATE orders
                    SET customer_name = %s,
                        customer_address = %s,
                        customer_phone = %s,
                        courier_id = %s,
                        products_id = %s
                    WHERE order_id = %s;
                """

                cur.execute(
                    update_sql,
                    (
                        new_name,
                        new_address,
                        new_phone,
                        new_courier,
                        new_items,
                        order_id
                    )
                )

                conn.commit()

                print("Order updated!")

    except Exception as e:
        print(f"Error: {e}")