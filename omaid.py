product_list = ["apple", "banana", "orange"]

#Main menue:
def print_main_menu():
 print("   ---- Main Menu ----\n|\t\t\t|\n| 0: Exit\t\t|\n| 1: Prouducts Menue\t|\n ---------------------")
 
def print_product_menu():
 print(" ---- Product Menu ----\n|\t\t\t|\n| 0: Main Menu\t\t|\n| 1: Prouducts list\t|\n| 2: Add Product\t|\n| 3: Update Product\t|\n| 4: Remove Productz\t|\n ---------------------")
 
 
# #user input:
while True:
    print_main_menu()
    user_input = input("Enter Option: ")
   
    if user_input == "0":
        print("Exit")
        break
   
    elif user_input == "1":
        while True:
            print_product_menu()
            product_choice = input("Enter Option: ")
           
            if product_choice == "0":
                break
           
            elif product_choice == "1":
                print(product_list)
               
            elif product_choice == "2":
                new_product = input("Enter new product name: ")
                product_list.append(new_product)
                print(product_list)
                print("New product added")
       
            elif product_choice == "3":
                check_product = input("Enter the product name you want to update: ")
                if check_product in product_list:
                    print("valid product")
                   
                    index = product_list.index(check_product)
                    updated_product = input("Enter the updated product name: ")
                    product_list[index] = updated_product
                    print(product_list)
                    print("Product has been updated")
                   
            elif product_choice == "4":
                print(f"current product list: {product_list}")  
                remove_product = int(input("Enter the index of the product you want to remove: "))
                product_list.pop(remove_product)
                print(f"New product list: {product_list}")
           
        else:
            print("invalid input")
           
    else:
            print("invalid input")