import csv
from couriers import load_couriers
from products import load_products

FIELDNAMES = ['customer_name', 'customer_address', 'customer_phone', 'courier', 'status', 'items']
STATUSES = ['Pending', 'order received', 'preparing', 'On the way', 'delivered']

def print_order_menu():
    print('\n ---------- Order Menu ---------')
    print('|\t\t\t\t|')
    print('| 1. Print Order Dictionary\t|')
    print('| 2. Add Order to Dictionary\t|')
    print("| 3. Update an Order's Status\t|")
    print("| 4. Update an Order's Details\t|")
    print('| 5. Delete an Order\t\t|')
    print('| 0. Exit to Main Menu\t\t|')
    print('| \t\t\t\t|')
    print('--------------------------------')

def read_orders_csv():
    try:
        with open('Orders.csv', 'r') as file:
            reader = csv.DictReader(file, skipinitialspace=True)
            if reader.fieldnames:
                reader.fieldnames = [name.strip() for name in reader.fieldnames if name]
            return [row for row in reader if any((value or '').strip() for value in row.values())]
    except FileNotFoundError:
        return []
    except Exception as error:
        print(f'Error reading Orders.csv: {error}')
        return []


def normalize_order(order, couriers, products):
    # Normalize courier: if it's an index, convert to name
    try:
        courier_index = int(order.get('courier', ''))
        if 0 <= courier_index < len(couriers):
            order['courier'] = couriers[courier_index]['name']
    except (ValueError, TypeError):
        pass  # Keep as is if not index

    # Normalize items: if comma-separated indices, convert to names
    items_str = order.get('items', '')
    if items_str:
        try:
            indices = [int(x.strip()) for x in items_str.split(',') if x.strip()]
            names = []
            for idx in indices:
                if 0 <= idx < len(products):
                    names.append(products[idx]['Name'])
            if names:
                order['items'] = ', '.join(names)
        except (ValueError, TypeError):
            pass  # Keep as is

    return order


def parse_index_list(raw_input):
    try:
        return [int(x.strip()) for x in raw_input.split(',') if x.strip()]
    except ValueError:
        return []


def choose_courier(couriers):
    if not couriers:
        return input('Enter courier name: ').strip()
    print('Choose a courier index:')
    for i, courier in enumerate(couriers):
        print(f'{i}: {courier.get("name", "Unnamed courier")}')
    try:
        index = int(input('Enter courier index: '))
        if 0 <= index < len(couriers):
            return couriers[index]['name']
    except ValueError:
        pass
    print('Invalid courier index, leaving blank.')
    return ''


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


def load_orders(couriers, products):
    return [normalize_order(order, couriers, products) for order in read_orders_csv()]


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

def print_order_list(order_list):
    if not order_list:
        print("WARNING - Order list is empty returning back to menu")
    else:
        for i, order in enumerate(order_list):
            print(f"{i}: Customer: {order.get('customer_name', '')}, "
                  f"Address: {order.get('customer_address', '')}, "
                  f"Phone: {order.get('customer_phone', '')}, "
                  f"Courier: {order.get('courier', '')}, "
                  f"Status: {order.get('status', '')}, "
                  f"Items: {order.get('items', '')}")



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


def update_order_status(order_list):
    if not order_list:
        print('No orders available to update.')
        return False
    print_order_list(order_list)
    try:
        order_index = int(input('Enter the order index to update: '))
        if 0 <= order_index < len(order_list):
            for i, status in enumerate(STATUSES):
                print(f'{i}: {status}')
            status_index = int(input('Enter the status index: '))
            if 0 <= status_index < len(STATUSES):
                order_list[order_index]['status'] = STATUSES[status_index]
                print('Order status updated successfully.')
                return True
        print('Invalid order or status index.')
    except ValueError:
        print('Please enter a valid number.')
    return False


def update_order_details(order_list):
    if not order_list:
        print('No orders available to update.')
        return False
    print_order_list(order_list)
    try:
        index = int(input('Select order index: '))
        order = order_list[index]
        for key in ['customer_name', 'customer_address', 'customer_phone', 'courier', 'status', 'items']:
            new_value = input(f"Update {key} (leave blank to keep '{order.get(key, '')}'): ")
            if new_value.strip():
                order[key] = new_value.strip()
        print('Order updated.')
        return True
    except (IndexError, ValueError):
        print('Invalid input.')
    return False


def delete_order(order_list):
    if not order_list:
        print('No orders available to delete.')
        return False
    print_order_list(order_list)
    try:
        index = int(input('Select order index to delete: '))
        if 0 <= index < len(order_list):
            order_list.pop(index)
            print('Order deleted!')
            return True
        print('Invalid index')
    except ValueError:
        print('Invalid input')
    return False



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
            update_order_details(order_list)   
        elif choice == '5':
            delete_order(order_list)
        else:
            print('Invalid input')


if __name__ == "__main__":
    couriers = load_couriers()
    products = load_products()
    orders = load_orders(couriers, products)
    order_menu(couriers, products, orders)

