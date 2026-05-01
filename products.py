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


def save_products(products):
    #Save products back to Products.txt file
    try:
        with open('Products.txt', 'w') as file:
            for product in products:
                file.write(product + '\n')
    except Exception as e:
        print(f"Error saving products: {e}")


def load_products():
    #Load products from Products.txt file
    products = []
    try:
        with open('Products.txt', 'r') as file:
            for product in file:
                products.append(product.strip())
    except FileNotFoundError:
        print("Product not found. Using default products.")
        products = ["Mocha", "Americano", "Cappucino", "Latte", "Tea"]
    return products







def product_menu(products_list):
            while True:
                print_product_menu()
                product_choice = input("Enter option: ")

                if product_choice == "0":
                    break

                elif product_choice == "1":
                    print(products_list)
                    
                elif product_choice == "2":
                    while True:
                        try:         
                            new_product = input("Enter new product name: ")

                            if new_product in products_list:
                                print ("this product already exists")
                            else:
                                products_list.append(new_product)
                                print(products_list)
                                break
                        except: ValueError
                        print("please eneter a new product")
                            
                elif product_choice == "3":
                    while True:
                        try:
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
                        except ValueError:
                            print("Invalid input, please enter a number")

                elif product_choice == "4":
                    while True:
                        try:
                            for (index, product) in enumerate(products_list):
                                print (index, product)
                            delete_select_index = int(input("please select the index of what you want to delete "))
                            if 0 <= delete_select_index < len(products_list):
                                products_list.pop(delete_select_index)
                                print(f"Here is the new product list: {products_list}")
                                break
                            else:
                                print("please enter a valid input")
                        except ValueError:
                            print("Invalid input, please enter a number")