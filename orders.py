import csv
from pathlib import Path

DATA_DIR = Path(__file__).parent
PRODUCTS_PATH = DATA_DIR / 'Products.csv'
ORDERS_PATH = DATA_DIR / 'Orders.csv'
COURIERS_PATH = DATA_DIR / 'couriers.csv'

Statuses = ['Pending', 'order received', 'preparing', 'On the way', 'delivered']


def load_csv(path):
    try:
        with open(path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, skipinitialspace=True)
            if reader.fieldnames:
                reader.fieldnames = [name.strip() if name else name for name in reader.fieldnames]
            return [row for row in reader if any((value or '').strip() for value in row.values())]
    except FileNotFoundError:
        print(f'{path.name} not found')
        return []
    except Exception as error:
        print(f'Error reading {path.name}: {error}')
        return []


def load_products():
    return load_csv(PRODUCTS_PATH)


def load_couriers():
    return load_csv(COURIERS_PATH)


def parse_index_list(value):
    if not value:
        return []

    parts = [part.strip() for part in str(value).split(',') if part.strip()]
    indexes = []
    for part in parts:
        if part.isdigit():
            indexes.append(int(part))
    return indexes


def normalize_order(order, couriers, products):
    order = {
        (key.strip() if key else ''): (value or '').strip()
        for key, value in order.items()
        if key is not None
    }

    if order.get('status', '').isdigit():
        status_index = int(order['status'])
        order['status'] = Statuses[status_index] if 0 <= status_index < len(Statuses) else 'Unknown'

    if order.get('courier', '').isdigit():
        courier_index = int(order['courier'])
        if 0 <= courier_index < len(couriers):
            order['courier'] = couriers[courier_index].get('name', f'Courier {courier_index}')
        else:
            order['courier'] = f'Courier {courier_index}'

    items_value = order.get('items', '')
    item_indexes = parse_index_list(items_value)
    if item_indexes:
        item_names = []
        for item_index in item_indexes:
            if 0 <= item_index < len(products):
                item_names.append(products[item_index].get('Name', f'Product {item_index}'))
            else:
                item_names.append(f'Product {item_index}')
        order['items'] = ', '.join(item_names)
    else:
        order['items'] = ', '.join([item.strip() for item in items_value.split(',') if item.strip()])

    return order


def load_orders(couriers, products):
    orders = load_csv(ORDERS_PATH)
    return [normalize_order(order, couriers, products) for order in orders]


def save_orders(order_list):
    if not order_list:
        return

    fieldnames = ['customer_name', 'customer_address', 'customer_phone', 'courier', 'status', 'items']
    try:
        with open(ORDERS_PATH, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for order in order_list:
                writer.writerow({key: order.get(key, '') for key in fieldnames})
    except Exception as error:
        print(f'Unable to save orders: {error}')


products = load_products()
couriers = load_couriers()
order_list = load_orders(couriers, products)
order_dirty = False


def print_order_menu():
    print('\n ---------- Order Menu ---------')
    print('|\t\t\t\t|')
    print('| 1. Print Order Dictionary\t|')
    print('| 2. Add Order to Dictionary\t|')
    print("| 3. Update an Order's Status\t|")
    print('| 4. Update an Order\'s Details\t|')
    print('| 5. Delete an Order\t\t|')
    print('| 0. Exit to Main Menu\t\t|')
    print('| \t\t\t\t|')
    print('--------------------------------')


def print_order_list():
    if not order_list:
        print('No orders found.')
        return

    for index, order in enumerate(order_list):
        print(f'Order {index}:')
        for key, value in order.items():
            print(f'  {key}: {value}')
        print()


def add_order():
    new_customer_name = input('What is the new customer\'s name? ')
    new_customer_address = input('What is the address of the customer? ')
    new_customer_pnumber = input('What is the phone number of the customer? ')

    courier_value = ''
    if couriers:
        print('Choose a courier index:')
        for i, courier in enumerate(couriers):
            print(f'{i}: {courier.get("name", "Unnamed courier")}')
        try:
            courier_index = int(input('Enter courier index: '))
            if 0 <= courier_index < len(couriers):
                courier_value = couriers[courier_index].get('name', f'Courier {courier_index}')
            else:
                print('Invalid courier index, leaving blank.')
        except ValueError:
            print('Invalid courier input, leaving blank.')
    else:
        courier_value = input('Enter courier name: ').strip()

    status_value = 'Pending'
    print('Choose the order status:')
    for i, status in enumerate(Statuses):
        print(f'{i}: {status}')
    try:
        status_index = int(input('Enter status index: '))
        if 0 <= status_index < len(Statuses):
            status_value = Statuses[status_index]
        else:
            print('Invalid status index, defaulting to Pending.')
    except ValueError:
        print('Invalid status input, defaulting to Pending.')

    items_value = ''
    if products:
        print('Choose product indexes separated by commas:')
        for i, product in enumerate(products):
            print(f'{i}: {product.get("Name", "Unnamed product")} ({product.get("Price", "")})')
        raw_items = input('Enter product indexes (comma-separated): ').strip()
        item_indexes = parse_index_list(raw_items)
        if item_indexes:
            item_names = []
            for item_index in item_indexes:
                if 0 <= item_index < len(products):
                    item_names.append(products[item_index].get('Name', f'Product {item_index}'))
                else:
                    item_names.append(f'Product {item_index}')
            items_value = ', '.join(item_names)
        else:
            items_value = raw_items
    else:
        items_value = input('Enter items (comma-separated): ').strip()

    global order_dirty
    order_list.append({
        'customer_name': new_customer_name,
        'customer_address': new_customer_address,
        'customer_phone': new_customer_pnumber,
        'courier': courier_value,
        'status': status_value,
        'items': items_value,
    })
    order_dirty = True
    print('Order added to list')


def update_order_status():
    global order_dirty
    if not order_list:
        print('No orders available to update.')
        return

    print_order_list()
    try:
        order_index = int(input('Enter the order index to update: '))
        if 0 <= order_index < len(order_list):
            for i, status in enumerate(Statuses):
                print(f'{i}: {status}')
            status_index = int(input('Enter the status index: '))
            if 0 <= status_index < len(Statuses):
                order_list[order_index]['status'] = Statuses[status_index]
                order_dirty = True
                print('Order status updated successfully.')
                return
        print('Invalid order or status index.')
    except ValueError:
        print('Please enter a valid number.')


def update_order_details():
    global order_dirty
    if not order_list:
        print('No orders available to update.')
        return

    print_order_list()
    try:
        index = int(input('Select order index: '))
        order = order_list[index]
        for key in ['customer_name', 'customer_address', 'customer_phone', 'courier', 'status', 'items']:
            new_value = input(f"Update {key} (leave blank to keep '{order.get(key, '')}'): ")
            if new_value.strip():
                order[key] = new_value.strip()
        order_dirty = True
        print('Order updated.')
    except (IndexError, ValueError):
        print('Invalid input.')


def delete_order():
    global order_dirty
    if not order_list:
        print('No orders available to delete.')
        return

    print_order_list()
    try:
        index = int(input('Select order index to delete: '))
        if 0 <= index < len(order_list):
            order_list.pop(index)
            order_dirty = True
            print('Order deleted!')
        else:
            print('Invalid index')
    except ValueError:
        print('Invalid input')


def order_menu():
    while True:
        print_order_menu()
        order_menu_choice = input('Please select an option: ')

        if order_menu_choice == '0':
            save_orders(order_list)
            print('Your Order Changes are saved.')
            break
        elif order_menu_choice == '1':
            print_order_list()
        elif order_menu_choice == '2':
            add_order()
        elif order_menu_choice == '3':
            update_order_status()
        elif order_menu_choice == '4':
            update_order_details()
        elif order_menu_choice == '5':
            delete_order()
        else:
            print('Invalid input')


if __name__ == '__main__':
    order_menu()