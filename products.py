import csv



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
        with open('Products.csv', 'w') as file:
            headers = ["Name","Price"]
            f = csv.DictWriter(file, fieldnames=headers)
            f.writeheader()
            f.writerows(products)
    except Exception as e:
        print(f"Error saving products: {e}")


def load_products():
    #Load products from Products.txt file
    products = []
    try:
        file = open("Products.csv", "r")
        f = csv.DictReader(file)
        for dictonary in f:
            products.append(dictonary)
    except FileNotFoundError:
        print("Product not found. Using default products.")
        products = [
        {"Name":"Tea",
        "Price":2.99},
        {"Name":"Latte",
        "Price":1.99}
        ]

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
                            # Checks each dicts Name key value and if the name matches a duplicate will not move
                            for products in products_list:
                                if new_product == products["Name"]:
                                    print ("This product already exists")
                                    break
                            else:
                                try:
                                    new_product_prince = float(input("Enter a price for this product: "))
                                    products_list.append({
                                    "Name": new_product,
                                    "Price": new_product_prince
                                    })
                                    print(products_list)
                                    break
                                except: ValueError
                                print("Please Enter a valid price")
                        except: ValueError
                        print("Please enter a new product")
                            
                elif product_choice == "3":
                    while True:
                        try:
                            for (index, product) in enumerate(products_list):
                                print (index, product)
                            update_select_index = int(input("Please select the index of what you want to update "))
                            if   0 <= update_select_index < len(products_list):
                                update_product = products_list[update_select_index]

                                for key in update_product:
                                    # Cycles through keys getting input for values if blank doesnt change
                                    new_value = input(f"Update {key}? Leave blank to keep {update_product[key]}: ")
                                    if new_value != "":
                                        # Checks each dicts Name key value and if the name matches a duplicate will skip and not update
                                        for products in products_list:
                                            if new_value in products["Name"]:
                                                print("Already in list")
                                                break
                                        else:
                                            update_product[key] = new_value

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