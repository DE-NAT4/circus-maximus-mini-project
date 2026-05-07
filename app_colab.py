import orders 
import products
import couriers


products_list = products.load_products()

courier_list = couriers.load_couriers()

order_list = orders.load_orders(courier_list, products_list)
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



while True:
    print_main_menu()
    user_input = input("Enter option: ")

    if user_input == "0":
        saveconf = input("Do you want to save your changes y/n: ")
        if saveconf == "y":
            products.save_products(products_list)
            couriers.save_couriers(courier_list)
            orders.save_orders(order_list)
            print("Saving and Exiting app...")
            exit()
            break

        elif saveconf == "n":
            print("Exiting app...")
            exit()
            break
        
        else:  
            print ("Invalid Input")
    
    elif user_input == "1":
        products.product_menu(products_list)

    elif user_input== "2":
        couriers.courier_menu(courier_list)
        
    elif user_input == "3":
        orders.order_menu(courier_list, products_list, order_list)
        # print(orders.__file__)
        # print(dir(orders))

    else:
        print("Invalid input ")
