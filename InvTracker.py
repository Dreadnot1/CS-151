from easygui import *
import sys


inventory = {}


def selection_menu():
    while True:
        option_menu = buttonbox("An extremely simple inventory tracker made with Python."
                                " You can add or delete items, set or change quantities, or view your inventory."
                                " Please note, at least 2 items must be in the database before you can check inventory."
                                " All data is saved upon Exiting. No need to remember doing it manually!",
                                "Inventory Tracker v.3.0.0",
                                ["Check inventory", "Update stock", "Add items", "Delete items", "Exit"])     
        if option_menu == "Check inventory":
            check_inventory()
        elif option_menu == "Update stock":
            update_quantity()
        elif option_menu == "Add items":
            add_items()
        elif option_menu == "Delete items":
            delete_items()
        elif option_menu == "Exit":
            save_data(file_path)
            sys.exit()


def add_items():
    try:
        product_info = multenterbox("Enter product information below:",
                                    "Inventory Tracker v.3.0.0",
                                    ["Product Name", "Quantity"])
        if product_info[0] in inventory:
            error_message = msgbox("Item already exists in the database!",
                            "WARNING - Unable to Process Request - WARNING",
                            "Go Back")
        else:
            inventory[product_info[0]] = product_info[1]
    except TypeError:
        error = msgbox("Operation cancelled! Returning to Main Menu...")
        

#EasyGUI requires at least two choices for choicebox so I had to work around that limitation
def check_inventory():
    counter = 0
    for item in inventory:
        counter += 1
    if counter >= 2:
        select_item = choicebox("Shown below is a list of all your tracked products:",
                                "Inventory Tracker v.3.0.0", inventory)
        check_quantity = "Quantity in stock: " + str(inventory[select_item])
        display_quantity = msgbox(check_quantity, "Inventory Tracker v.3.0.0")
    else:
        error_message = msgbox("Database needs at least 2 items! Please add more data.",
                                "WARNING - Unable to Process Request - WARNING",
                                "Go Back")


def update_quantity():
    item_chosen = enterbox("Which item would you like to edit?", "Inventory Tracker v.3.0.0")
    if item_chosen in inventory:
        quantity_change = integerbox("Enter the new quantity", "Inventory Tracker v.3.0.0")
        inventory[item_chosen] = quantity_change
        update_success = msgbox("Quantity successfully updated!", "Inventory Tracker v.3.0.0")
    else:
        update_failure = msgbox("Quantity failed to update! Does the item exist?", "Inventory Tracker v.3.0.0")


def delete_items():
    item_chosen = enterbox("Which item would you like to delete?", "Inventory Tracker v.3.0.0")
    if item_chosen in inventory:
        del inventory[item_chosen]
        update_success = msgbox("Item successfully deleted!", "Inventory Tracker v.3.0.0")
    else:
        update_failure = msgbox("Item failed to delete! Does it exist?", "Inventory Tracker v.3.0.0")


def path_finder():
    response = ynbox("Would you like to import a file?", "Inventory Tracker v.3.0.0")
    if response == True:
        file_name = fileopenbox("Choose a file:", "File")
        if file_name == None:
            msgbox("WARNING: Couldn't load file data! Now creating an empty database...", "Inventory Tracker v.3.0.0")
            return False
        else:
            return file_name
    else:
        return False


#File format used is item:quantity\n
def load_file(path):
    with open(path, "r") as file:
        for line in file:
            remove_newlines = line.rstrip()
            split_values = remove_newlines.split(":")
            inventory[split_values[0]] = split_values[1]


def save_data(path):
    if path == False:
        save_path = filesavebox("Choose a location to save your file:", "File")
        if save_path == None:
            msgbox("WARNING: Operation cancelled! File data not saved.", "Inventory Tracker v.3.0.0")
            return False
        with open(save_path, "w") as file:
            for item in inventory:
                file.writelines(item + ":" + str(inventory[item]) + "\n")
    else:
        with open(path, "w") as file:
            for item in inventory:
                file.writelines(item + ":" + str(inventory[item]) + "\n")
            

#Start of program
file_path = path_finder()

if file_path == False:
    selection_menu()
else:
    load_file(file_path)
    selection_menu()
