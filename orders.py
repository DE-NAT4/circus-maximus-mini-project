import csv
from select import select
from couriers import load_couriers
from products import retrieve_products
from db import get_connection


#FIELDNAMES = ['customer_name', 'customer_address', 'customer_phone', 'courier', 'status', 'items']
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
def choose_courier():
    couriers = load_couriers()
    if not couriers:
        return "No couriers available, please add a courier first."

    print('Choose a courier:')
    for i, courier in enumerate(couriers):
        print(f'{i}: {courier.get("name", "Unnamed courier")} ({courier.get("phone", "")})')
    try:
        choice = int(input('Enter courier index: ').strip())
    except ValueError:
        return None
    if 0 <= choice < len(couriers):
        return couriers[choice]
    return None

# change
def parse_index_list(raw_input):
    try:
        return [int(x.strip()) for x in raw_input.split(',') if x.strip()]
    except Exception:
        return []


def choose_products(products):
    if not products:
        return input('Enter items (comma-separated): ').strip()
    print('Choose product indexes separated by commas:')
    for i, product in enumerate(products):
        print(f'{i}: {product.get("Name", "Unnamed product")} ({product.get("Price", "")})')
    raw_items = input('Enter product indexes (comma-separated): ').strip()
    item_indexes = parse_index_list(raw_items)
    if item_indexes:
        return ', '.join(
            products[item_index].get('Name', f'Product {item_index}')
            if 0 <= item_index < len(products)
            else f'Product {item_index}'
            for item_index in item_indexes
        )
    return raw_items

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

print_orders()

def update_order_status():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT order_id, status FROM orders
                    ORDER BY order_id ASC        
                """)
                orders = cur.fetchall()
                if not orders:
                    print('No orders available to update.')
                    return False
                for order in orders:
                    print(f'{order[0]}: {order[1]}')
                order_id = input('Enter the order ID to update: ')
                print('Choose new status:')
                cur.excute("""
                           SELECT DISTINCT status FROM status 
                           """)
                statuses = cur.fetchall()
                status_index = int(input('Enter status index: '))
                if 0 <= status_index < len(statuses):
                    new_status = statuses[status_index][0]
                    cur.execute("""
                        UPDATE orders
                        SET status = %s
                        WHERE order_id = %s
                    """, (new_status, order_id))
                    print('Order status updated successfully.')
                    return True
                else:
                    print('Invalid status index.')
    except ValueError:
        print('Please enter a valid number.')
    return False

# change
def add_order(order_list, couriers, products):
    customer_name = input('What is the new customer\'s name? ')
    customer_address = input('What is the address of the customer? ')
    customer_phone = input('What is the phone number of the customer? ')
    courier = choose_courier(couriers)
    status = 'Pending'
    print('Choose the order status:')
    for i, status_option in enumerate(STATUSES):
        print(f'{i}: {status_option}')
    try:
        status_index = int(input('Enter status index: '))
        if 0 <= status_index < len(STATUSES):
            status = STATUSES[status_index]
        else:
            print('Invalid status index, defaulting to Pending.')
    except ValueError:
        print('Invalid status input, defaulting to Pending.')
    items = choose_products(products)
    order_list.append({
        'customer_name': customer_name,
        'customer_address': customer_address,
        'customer_phone': customer_phone,
        'courier': courier,
        'status': status,
        'items': items,
    })
    print('Order added to list')
    return True

# change


# change
def update_order_details(order_list, couriers, products):
    if not order_list:
        print('No orders available to update.')
        return False
    print_order_list(order_list)
    try:
        index = int(input('Select order index: '))
        order = order_list[index]

        for key in ['customer_name', 'customer_address', 'customer_phone']:
            new_value = input(f"Update {key} (leave blank to keep '{order.get(key, '')}'): ")
            if new_value.strip():
                order[key] = new_value.strip()

        new_courier = choose_courier(couriers)
        if new_courier.strip():
            order['courier'] = new_courier.strip()

        new_items = choose_products(products)
        if new_items.strip():
            order['items'] = new_items.strip()

        print('Choose the new status:')
        for i, status_option in enumerate(STATUSES):
            print(f'{i}: {status_option}')
        status_input = input('Enter status index (leave blank to keep current): ').strip()
        if status_input:
            status_index = int(status_input)
            if 0 <= status_index < len(STATUSES):
                order['status'] = STATUSES[status_index]
            else:
                print('Invalid status index, keeping current status.')

        print('Order updated.')
        return True
    except (IndexError, ValueError):
        print('Invalid input.')
    return False

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
def order_menu(couriers, products, order_list):
    while True:
        print_order_menu()
        choice = input('Please select an option: ')
        if choice == '0':
            break
        elif choice == '1':
            print_order_list(order_list)
        elif choice == '2':
            add_order(order_list, couriers, products)
        elif choice == '3':
            update_order_status(order_list)
        elif choice == '4':
            update_order_details(order_list, couriers, products)
        elif choice == '5':
            delete_order(order_list)
        else:
            print('Invalid input')


# if __name__ == "__main__":
#     couriers = load_couriers()
#     #products = load_products()
#     orders = load_orders(couriers, products)
#     order_menu(couriers, products, orders)

