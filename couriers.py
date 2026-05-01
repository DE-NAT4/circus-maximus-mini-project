import csv

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

def print_courier_list(courier_list):
    if len(courier_list) == 0:
            print("WARNING - Courier list is empty returning back to menu")
            
    else:
        for courier in enumerate(courier_list):
            print(courier)

def add_courier(courier_list):
    try:
        # Ask user to enter a name and a phone number
        new_courier = input("Enter the name of courier: ")          
        new_courier_phone = input("Enter the phone number of courier: ")        
        
        courier = {
            "name": new_courier,
            "phone": new_courier_phone
        }
        # Check if the courier (name and phone number pair) already exists
        if courier not in courier_list:
            courier_list.append(courier)
            print ("New Courier Added")
        else:
            print("Courier already exists")
            
    except Exception as e:
        print(f"Error: {e}")

def update_courier(courier_list):
    while True:
        if len(courier_list) == 0:
            print("WARNING - Courier list is empty returning back to menu")
            break
        
        else:
            print_courier_list(courier_list)
            try:
                index = int(input("Enter index to update: "))
                print(courier_list[index])      # catch index error immediately

                # Ask user for courier name and phone number and put values in a dict
                new_name = input("Enter a new name: ")
                new_phone_num = input("Enter a new phone number: ")
                updated_courier = {
                    'name': new_name,
                    'phone': new_phone_num
                }
                # Check if courier already exist 
                if updated_courier not in courier_list:
                    courier_list[index] = updated_courier
                    print ("Updated Sucessfully")
                    break

                else:
                    print ("Courier already exists")
                    break
                        
            except Exception as e:
                print(f"Error: {e}")
                            
def remove_courier(courier_list):
    while True:
        if len(courier_list) == 0:
            print("WARNING - Courier list is empty returning back to menu")
            break

        else:
            print_courier_list(courier_list)
            try:
                index = int(input("Enter index to delete: "))
                print(courier_list[index])      # catch index error immediately

                courier_list.pop(index)
                print("Courier Deleted")
                break
            except Exception as e:
                print(f"Error: {e}")

def courier_menu(courier_list):
    while True:
        print_courier_menu()
        courier_choice = input("Enter Option: ")

        if courier_choice == "0":
            break

        elif courier_choice == "1":
            print_courier_list(courier_list)
            
        elif courier_choice == "2":
            add_courier(courier_list)            
            
        elif courier_choice == "3":
            update_courier(courier_list)
            
        elif courier_choice == "4":
            remove_courier(courier_list)

        else: 
            print ("Invalid Input")

