import orders     
def load_products():
    """Load products from Products.txt file"""
    products = []
    try:
        with open('Products.txt', 'r') as file:
            for product in file:
                products.append(product.strip())
    except FileNotFoundError:
        print("Product not found. Using default products.")
        products = ["Mocha", "Americano", "Cappucino", "Latte", "Tea"]
    return products

def save_products(products):
    """Save products back to Products.txt file"""
    try:
        with open('Products.txt', 'w') as file:
            for product in products:
                file.write(product + '\n')
    except Exception as e:
        print(f"Error saving products: {e}")

def products_menu():
    while True:
            print_product_menu()
            product_choice = input("Enter option: ")

            if product_choice == "0":
                break

            elif product_choice == "1":
                print(products_list)
                
            elif product_choice == "2":
                new_product = input("Enter new product name: ")
                products_list.append(new_product)
                save_products(products_list)
                print(products_list)
                print("New product added")

            elif product_choice == "3":
                while True:
                    for (index, product) in enumerate(products_list):
                        print (index, product)
                    update_select_index = int(input("Please select the index of what you want to update "))

                    if   0 <= update_select_index < len(products_list):
                    #if update_select_index in products_list:
                        update_select_name = str(input("Please enter a new name "))
                        if update_select_name in products_list:
                            print ("This item already exists")
                        else:
                            products_list[update_select_index] = update_select_name
                            save_products(products_list)
                            print ("Product updated")
                            print (products_list)
                            break

                    else: 
                        print ("Invalid Index")

            elif product_choice == "4":
                print(f"Here are the current products: {products_list}")

                index = int(input("Enter the index of the product to be deleted: "))
                products_list.pop(index)
                save_products(products_list)

                print(f"Here is the new product list: {products_list}")

            else:
                print("invalid input")



products_list = load_products()

courier_list = []
# checking branches




def print_main_menu():
    print(" ------ Main Menu ------")
    print("|\t\t\t|")
    print("| 1. Products Menu\t|")
    print("| 2. Courier Menu \t|")
    print("| 3. Order Menu \t|")
    print("| 0. Exit\t\t|")
    print("|\t\t\t|")
    print("------------------------")

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




order_list = [{
    "Customer Name": "John",
    "Customer Address":"Bradford",
    "Customer Phone":"071111111",
    "Order Status": "Pending"
    }]

# This function will print the courier menu (NEEDS TO BE LINKED TO THE TXT FILE)
def print_courier_list():
    for courier in enumerate(courier_list):
        print (courier)
    



while True:
    print_main_menu()
    user_input = input("Enter option: ")

    if user_input == "0":
        print("Exiting app...")
        break

    elif user_input == "1":
        products_menu()

    elif user_input== "2":
        while True:
            print_courier_menu()
            courier_choice = input("Enter Option: ")

            if courier_choice == "0":
                break

            if courier_choice == "1":
                print_courier_list()
                pass

            if courier_choice == "2":
                new_courier = input("Enter the name of courier: ")
                courier_list.append(new_courier)
                print ("New Courier Added")
                print_courier_list()
                pass

            if courier_choice == "3":
                while True:
                    print_courier_list()
                    index = int(input("Enter index to update: "))
                    if 0 <= index <= len(courier_list):
                        new_name = input("Enter a new name: ")
                        courier_list[index] = new_name
                        print ("Updated Sucessfully")
                        print_courier_list()
                        break
                    else:
                        print ("Invalid Input")

                

            if courier_choice == "4":
                while True:
                    print_courier_list()
                    index = int(input("Enter index to delete: "))
                    if 0 <= index <+ len(courier_list):
                        courier_list.pop(index)
                        print("Courier Deleted")
                        print_courier_list()
                        break
                    else:
                        print("Invalid Input")


    elif user_input == "3":
        orders.order_menu()
        # print(orders.__file__)
        # print(dir(orders))

    else:
        print("Invalid input")

        