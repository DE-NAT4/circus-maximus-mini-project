products_list = ["Mocha", "Americano", "Cappucino", "Latte", "Tea"]

def print_main_menu():
    print(" ------ Main Menu ------")
    print("|\t\t\t|")
    print("| 1. Products Menu\t|")
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

while True:
    print_main_menu()
    user_input = input("Enter option: ")

    if user_input == "0":
        print("Exiting app...")
        break

    elif user_input == "1":
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
                            print ("Product updated")
                            print (products_list)
                            break

                    else: 
                        print ("Invalid Index")

            elif product_choice == "4":
                print(f"Here are the current products: {products_list}")

                index = int(input("Enter the index of the product to be deleted: "))
                products_list.pop(index)

                print(f"Here is the new product list: {products_list}")

            else:
                print("invalid input")


    else:
        print("Invalid input")

        

