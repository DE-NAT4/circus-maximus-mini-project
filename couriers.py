from database import execute, fetch_all


def print_courier_menu():
    print("\n ----- Courier Menu -----")
    print("|\t\t\t\t|")
    print("| 1. Print Courier list\t|")
    print("| 2. Add Courier\t|")
    print("| 3. Update Courier\t|")
    print("| 4. Remove Courier\t|")
    print("| 0. Main Menu\t\t|")
    print("|\t\t\t\t|")
    print("------------------------")


def load_couriers():
    couriers = fetch_all('couriers')
    if not couriers:
        default = [
            {'name': 'John', 'phone': '071111111111'},
            {'name': 'Mark', 'phone': '072222222222'}
        ]
        for courier in default:
            execute(
                'INSERT INTO couriers (name, phone) VALUES (?, ?)',
                (courier['name'], courier['phone']),
                commit=True
            )
        couriers = fetch_all('couriers')
    return couriers


def save_couriers(couriers):
    # Data is persisted live to the database when menu operations run.
    return


def print_courier_list(courier_list):
    if not courier_list:
        print('WARNING - Courier list is empty returning back to menu')
    else:
        for courier in courier_list:
            print(f"{courier['id']}: {courier['name']} ({courier['phone']})")


def add_courier(courier_list):
    try:
        new_name = input('Enter the name of courier: ').strip()
        new_phone = input('Enter the phone number of courier: ').strip()
        if not new_name:
            print('Courier name is required.')
            return

        if any(c['name'] == new_name and c['phone'] == new_phone for c in courier_list):
            print('Courier already exists')
            return

        cursor = execute(
            'INSERT INTO couriers (name, phone) VALUES (?, ?)',
            (new_name, new_phone),
            commit=True
        )
        courier_id = cursor.lastrowid
        courier_list.append({'id': courier_id, 'name': new_name, 'phone': new_phone})
        print('New Courier Added')
    except Exception as e:
        print(f'Error: {e}')


def update_courier(courier_list):
    if not courier_list:
        print('WARNING - Courier list is empty returning back to menu')
        return

    print_courier_list(courier_list)
    try:
        courier_id = int(input('Enter courier id to update: '))
    except ValueError:
        print('Invalid id')
        return

    courier = next((c for c in courier_list if c['id'] == courier_id), None)
    if not courier:
        print('Courier not found')
        return

    new_name = input('Enter a new name (leave blank to keep current): ').strip() or courier['name']
    new_phone = input('Enter a new phone number (leave blank to keep current): ').strip() or courier['phone']

    if any(c['name'] == new_name and c['phone'] == new_phone and c['id'] != courier_id for c in courier_list):
        print('Courier already exists')
        return

    execute(
        'UPDATE couriers SET name = ?, phone = ? WHERE id = ?',
        (new_name, new_phone, courier_id),
        commit=True
    )
    courier.update({'name': new_name, 'phone': new_phone})
    print('Updated Successfully')


def remove_courier(courier_list):
    if not courier_list:
        print('WARNING - Courier list is empty returning back to menu')
        return

    print_courier_list(courier_list)
    try:
        courier_id = int(input('Enter courier id to delete: '))
    except ValueError:
        print('Invalid id')
        return

    courier = next((c for c in courier_list if c['id'] == courier_id), None)
    if not courier:
        print('Courier not found')
        return

    execute('DELETE FROM couriers WHERE id = ?', (courier_id,), commit=True)
    courier_list.remove(courier)
    print('Courier Deleted')


def courier_menu(courier_list):
    while True:
        print_courier_menu()
        courier_choice = input('Enter Option: ')

        if courier_choice == '0':
            break
        elif courier_choice == '1':
            print_courier_list(courier_list)
        elif courier_choice == '2':
            add_courier(courier_list)
        elif courier_choice == '3':
            update_courier(courier_list)
        elif courier_choice == '4':
            remove_courier(courier_list)
        else:
            print('Invalid Input')

