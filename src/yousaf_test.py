# Initial Products list 
products_list= ["Mocha", "Americano", "Cappucino", "Latte", "Tea"]
 
# MAIN MENU
print("Main Menu:")
print("0 - Exit")
print("1 - Products Menu")
 
main_choice = int(input("Please enter your choice:"))
 
#EXIT 
if main_choice == 0:
    print = ("Exited")
 
# PRODUCTS MENU
elif main_choice == 1:
    print("Products Menu:")
    print("0 - Return to Main Menu")
    print("1 - View Products")
    print("2 - Add Product")
    print("3 - Update Product")
    print("4 - Delete Product")
 
product_choice = int(input("Please enter your choice: "))
# Return to main menu 
if product_choice == 0:
    print("Returning to main menu")
 
#view products
elif product_choice == 1:
        print(products_list)