from easygui import *
import sys

class Item:
    def __init__(self, name, price, quantity):
        self.item_name = name
        self.item_price = price
        self.quantity = quantity
        
    def get_price(self):
        return self.item_price
    
    def get_quantity(self):
        return self.quantity

class VendingMachine:
    def __init__(self):
        self.stored_products = {}
        
    def add_item(self, item):
        self.stored_products[item.item_name] = item.item_price
        
    def get_items(self):
        return self.stored_products
    
    def get_item_name(self, item):
        #Mr.Bowe's version of the method is below
        #return self.store_products[item].name
        if item.item_name in self.stored_products:
            return item.item_name
        else:
            return "Item not found!"
        
    def get_item_price(self, item):
        if item.item_name in self.stored_products:
            return item.item_price
        else:
            return "Item not found!"
        
    def calculate_change(self, buy_price, dollars, cents):
        converted_buy = buy_price * 100
        converted_dollars = dollars * 100
        if converted_dollars + cents > converted_buy:
            change_owed = (converted_dollars + cents) - converted_buy
            change = {"quarters": 0, "dimes": 0, "nickels": 0, "pennies": 0}
            while change_owed > 0:
                if change_owed % 25 == 0:
                    change_owed -= 25
                    change["quarters"] += 1
                elif change_owed % 10 == 0:
                    change_owed -= 10
                    change["dimes"] += 1
                elif change_owed % 5 == 0:
                    change_owed -= 5
                    change["nickels"] += 1
                elif change_owed % 1 == 0:
                    change_owed -= 1
                    change["pennies"] += 1
                else:
                    return "Error!"
            return change
        elif converted_dollars + cents == converted_buy:
            return "0. Exact change was given. Thank you!"
        else:
            return "Not enough money."

class VendingApp:
    def __init__(self):
        self.machine = VendingMachine()
        self.money = 0
    
    def populate(self):
        product1 = Item("candybar", 0.65, 3)
        product2 = Item("chips", 0.75, 5)
        product3 = Item("soda", 0.99, 1)
        self.machine.add_item(product1)
        self.machine.add_item(product2)
        self.machine.add_item(product3)
        return product1, product2, product3

    def get_money(self):
        try:
            while True:
                user_money = multenterbox("How much would you like to put in the machine? Please use whole numbers, not decimals.",
                                          "Virtual Vending Machine v.1.0.0",
                                          ["Dollars", "Cents"])
                if user_money == None:
                    sys.exit()
                else:
                    user_dollars = int(user_money[0])
                    user_cents = int(user_money[1])
                    money_list = [user_dollars, user_cents]
                if user_dollars + user_cents == 0:
                    msgbox("You didn't enter any money. Please try again.", "Virtual Vending Machine v.1.0.0")
                else:
                    return money_list
        except ValueError:
            msgbox("You decide not to use the vending machine and slowly walk away...", "Virtual Vending Machine v.1.0.0")
            sys.exit()

    def run(self):
        #Adds items to vending machine then returns an object list so they can be passed to buy_items for quantity checks
        products = test_app.populate()
        while True:
            option_menu = buttonbox("Ever used a virtual vending machine to buy virtual food?"
                                    " Now you can! Welcome to the future!",
                                    "Virtual Vending Machine v.1.0.0",
                                    ["Insert money", "Buy items", "Exit"])     
            if option_menu == "Insert money":
                if self.money != 0:
                    add_more = self.get_money()
                    self.money[0] += add_more[0]
                    self.money[1] += add_more[1]
                else:
                    self.money = self.get_money()
            elif option_menu == "Buy items":
                self.buy_items(products)
            elif option_menu == "Exit":
                sys.exit()
            else:
                sys.exit()
                
    def buy_items(self, products_list):
        #Mr.Bowe created a new list with a for loop, then appended it with the item, price and quantity
        #all of this info was displayed in the choicebox instead of just the product name
        show_products = self.machine.get_items()
        item_reference = None
        item_quantity = 0
        item_price = 0
        item_choice = choicebox("Shown below is a list of all the products you can buy! Choose wisely!",
                                "Virtual Vending Machine v.1.0.0", show_products)
        
        #Iterates through the list of objects to find where the user's choice is == the checked item's attribute "item_name"
        #If the choice matches the return value of the get_item_name method, which takes an item object as a parameter
        #and returns the object's name, then it retrieves that object's quantity as well
        for i in range(0, len(products_list)):
            if item_choice == self.machine.get_item_name(products_list[i]):
                item_quantity = products_list[i].get_quantity()
                item_reference = products_list[i]
                break
            elif item_choice == None:
                msgbox("Transaction cancelled! Exiting program...", "Virtual Vending Machine v.1.0.0")
                sys.exit()
            else:
                continue
                
        #Accesses the value of the show_products dictionary using the item_choice as a key
        #Then adds both price and quantity information to a string that passes to a confirmation box
        item_msg = "Price of item: $" + str(show_products[item_choice]) + " | In stock: " + str(item_quantity)
        item_price = show_products[item_choice]
        confirm = buttonbox(item_msg, "Virtual Vending Machine v.1.0.0", ["BUY NOW", "CANCEL"])
        
        if confirm == "BUY NOW" and self.money == 0:
            error_msg = msgbox("You don't have any money! Please go back and insert enough into the machine.",
                               "Virtual Vending Machine v.1.0.0")
        elif confirm == "BUY NOW" and (self.money[0] + self.money[1] / 100) >= item_price and item_reference.quantity > 0:
            change = self.machine.calculate_change(item_price, self.money[0], self.money[1])
            change_msg = "Your change: " + str(change)
            change_display = msgbox(change_msg, "Virtual Vending Machine v.1.0.0")
            item_reference.quantity -= 1
            self.money = 0
        elif confirm == "BUY NOW" and item_reference.quantity <= 0:
            sorry_msg = msgbox("Out of stock! Please select another item!", "Virtual Vending Machine v.1.0.0")
        elif confirm == "CANCEL":
            cancel_msg = msgbox("Transaction cancelled. Returning to main menu.", "Virtual Vending Machine v.1.0.0")
        else:
            error = msgbox("Not enough money! Please add more.", "Virtual Vending Machine v.1.0.0")


#Creating a VendingApp object to see if my composition works
test_app = VendingApp()

#Testing the main menu
test_app.run()

#Final thoughts: I really had to think through this one. It's challenging but I enjoyed it.
#It also ties together all the concepts we used this semester in a satisfying way.
#Overall, great exercise! I hope you keep it for future classes.