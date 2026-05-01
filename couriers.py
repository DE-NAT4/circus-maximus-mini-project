def courier_menu(courier_list):
    while True:
        print_courier_menu()
        courier_choice = input("Enter Option: ")

        if courier_choice == "0":
            break

        elif courier_choice == "1":
            print_courier_list(courier_list)
            

        elif courier_choice == "2":
            try:
                new_courier = input("Enter the name of courier: ")
                if new_courier in courier_list:
                    print("Courier already exists")

                else:
                    courier_list.append(new_courier)
                    print ("New Courier Added")
                    print_courier_list(courier_list)
            except:
                print("Invalid Input")
            

        elif courier_choice == "3":
            while True:
                if len(courier_list) == 0:
                    print("WARNING - Courier list is empty returning back to menu")
                    break
                
                else:
                    print_courier_list(courier_list)
                    try:
                        index = int(input("Enter index to update: "))
                        if 0 <= index <= len(courier_list):
                            new_name = input("Enter a new name: ")
                            if new_name in courier_list:
                                print ("Courier already exists")

                            else:
                                courier_list[index] = new_name
                                print ("Updated Sucessfully")
                                print_courier_list(courier_list)
                                break
                    except:
                        print ("Invalid Input")
                    else:
                        print ("Invalid Input")

                

        elif courier_choice == "4":
            while True:
                if len(courier_list) == 0:
                    print("WARNING - Courier list is empty returning back to menu")
                    break

                else:
                    print_courier_list(courier_list)
                    try:
                        index = int(input("Enter index to delete: "))
                        if 0 <= index <+ len(courier_list):
                            courier_list.pop(index)
                            print("Courier Deleted")
                            print_courier_list(courier_list)
                            break
                        else:
                            print("Invalid Input")
                    except:
                        print ("Invalid Input")
        else: 
            print ("Invalid Input")


def load_couriers():
    """Load couriers from couriers.txt file"""
    couriers = []
    try:
        with open('couriers.txt', 'r') as file:
            for courier in file:
                couriers.append(courier.strip())
    except FileNotFoundError:
        print("Courier not found. Using default couriers.")
        couriers = ["courier1", "courier2", "courier3"]
    return couriers
 
def save_couriers(couriers):
    """Save couriers back to couriers.txt file"""
    try:
        with open('couriers.txt', 'w') as file:
            for courier in couriers:
                file.write(courier + '\n')
    except Exception as e:
        print(f"Error saving couriers: {e}")


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

# This function will print the courier menu
def print_courier_list(courier_list):
    for courier in enumerate(courier_list):
        print (courier)