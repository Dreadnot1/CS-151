import sys

levels = {1: 100, 2: 250, 3: 500}


class Player:
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.maxHp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.xp = 0
        self.level = 0

        self.currentRoom = None
        self.inventory = []   # list of Item objects

    def moveTo(self, newRoom):
        self.currentRoom = newRoom
        print("\nYou move to: " + newRoom.name)

    def takeDamage(self, amount):
        actual = max(0, amount - self.defense)
        self.hp -= actual
        if self.hp < 0:
            self.hp = 0
        print(self.name + " takes " + str(actual) +
              " damage! (HP: " + str(self.hp) + "/" + str(self.maxHp) + ")")
        print("~-~-~-~-~-~-~-~-~-~-~-~")

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.maxHp:
            self.hp = self.maxHp
        print(self.name + " heals " + str(amount) +
              " HP. (HP: " + str(self.hp) + "/" + str(self.maxHp) + ")")

    def isAlive(self):
        return self.hp > 0

    def showStats(self):
        print("==== Player Stats ====")
        print("Name:    " + self.name)
        print("HP:      " + str(self.hp) + "/" + str(self.maxHp))
        print("Level:   " + str(self.level))
        print("Attack:  " + str(self.attack))
        print("Defense: " + str(self.defense))
        print("======================")

    def showInventory(self):
        print("==== Inventory ====")
        if len(self.inventory) == 0:
            print("You are carrying nothing.")
        else:
            for item in self.inventory:
                print(item.name + ": " + item.description)
        print("===================")
    
    def gainXp(self):
        self.xp += 100
        for key in levels:
            if self.xp >= levels[key]:
                self.level += 1
                del levels[key]
                print("LEVEL UP!")
                print("You're now level", self.level)
                print("~-~-~-~-~-~-~-~-~-~-~-~-")
                break


class Item:
    def __init__(self, name, description, kind, amount):
        self.name = name
        self.description = description
        self.kind = kind #can be "heal", "attack", "defense", or "none"
        self.amount = amount
        pass

    def use(self, player):
        if self.kind == "heal":
            print(player.name, "drank a health potion!")
            player.heal(self.amount)
        elif self.kind == "attack":
            print(player.name, "increased their attack by", self.amount)
            player.attack += self.amount
        elif self.kind == "defense":
            print(player.name, "increased their defense by", self.amount)
            player.defense += self.amount
        else:
            print("What the heck is this thing?")


class Enemy:
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.hp = hp
        self.maxHp = hp
        self.attack = attack
        self.defense = defense

    def takeDamage(self, amount):
        actual = max(0, amount - self.defense)
        self.hp -= actual
        if self.hp < 0:
            self.hp = 0
        print(self.name + " takes " + str(actual) +
              " damage! (HP: " + str(self.hp) + "/" + str(self.maxHp) + ")")

    def attackPlayer(self, player):
        print(self.name, "attacks for", self.attack, "damage!")
        player.takeDamage(self.attack)

    def isAlive(self):
        return self.hp > 0


class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description

        self.exits = {}
        self.items = []      # list of Item objects
        self.enemies = []    # list of Enemy objects

    def connect(self, direction, otherRoom):
        self.exits[direction] = otherRoom

    def getExit(self, direction):
        return self.exits.get(direction)

    def describe(self):
        text = ""
        text += "Now visiting the " + self.name + "\n"
        text += self.description + "\n"

        if len(self.exits) > 0:
            text += "Exits: " + ", ".join(self.exits.keys()) + "\n"

        if len(self.items) > 0:
            text += "Items here: " + ", ".join([i.name for i in self.items]) + "\n"

        if len(self.enemies) > 0:
            text += "Enemies here: " + ", ".join([e.name for e in self.enemies]) + "\n"

        return text


def attackEnemy(player, enemyName):
    room = player.currentRoom
    enemy = None

    #Finds the enemy in the room
    for e in room.enemies:
        if e.name.lower() == enemyName:
            enemy = e
            print(player.name, "attacks the enemy.")
            break

    if enemy is None:
        print("There is no enemy named " + enemyName + " here.\n")
        return

    #Player attacks enemy
    enemy.takeDamage(player.attack)
    
    #If enemy survives, it attacks the player
    if enemy.isAlive() == True:
        print("It survives the attack!")
        print("~-~-~-~-~-~-~-~-~-~-~-~")
        enemy.attackPlayer(player)
    #If enemy dies, it's removed from the room's list of enemies
    else:
        print("It dies from the attack!")
        print("~-~-~-~-~-~-~-~-~-~-~-~-")
        if enemyName == "eternus":
            print("You lay the old King's spirit to rest. The House of Eterna is now free of spirits.")
            print("But as for demons...")
            print("'HAHAHAHA! THERE'S NOTHING I LOVE MORE THAN TO EAT THE SOULS OF THE DAMNED!'")
            print("You drop the blade and take a huge step back, watching it carefully.")
            print("It appears you've unleashed a new evil on the House of Eterna.")
            sys.exit("You've won, but at what cost?")
        else:
            room.enemies.remove(enemy)
            player.gainXp()

    #If player dies, it's game over
    if player.isAlive() == False:
        sys.exit("You die in combat. GAME OVER!")


def createWorld():
    #Basic rooms with their descriptions
    foyer = Room("Foyer", "An entryway with a purple rug and a small endtable. There's an old chandelier hanging above.")
    hall = Room("Hall", "The walls are covered with family portaits. The faces seem familiar but you're unsure why. "
                "Your head feels fuzzy as you stand around, waiting.")
    kitchen = Room("Kitchen", "Sacks of flour sit quietly next to a chef's table. Metal cooking utentsils are scattered "
                   "everywhere. Towards the south of the room, you spot a piece of\n floor that looks slightly different "
                   "than the rest.")
    dining = Room("Dining", "A huge wooden table stretches out from one side of the room to the other. "
                  "You notice a half-eaten turkey resting on a white dinner plate. "
                  "There's a fork sticking out from it. Why didn't someone finish it, you wonder?")
    throne = Room("Throneroom", "An throne made of smooth obsidian and topped with sparkling jewels sits atop a raised platform. "
                  "It's looks as if no King has sat in it for\n quite a long time now. "
                  "And yet...you feel something strange lingering in the air. Something evil. "
                  "Something tells you that if the evil is released, the House of Eterna will finally be free.")
    hidden = Room("Armory", "A dusty hatch in the floor reveals a secret armory underneath the kitchen. "
                  "A long forgotten blade whispers from the darkness: 'Take me. Please.\n I'm thirsty for blood.' "
                  "You begin to ask it a question but realize that you'd be talking to an inanimate object. "
                  "Maybe you were just hearing things, you tell yourself. "
                  "Hanging on the wall next to it, you see a crescent-shaped shield glowing in the darkness. "
                  "It shines like a marble floor.")

    #Basic navigation
    foyer.connect("north", hall)
    hall.connect("south", foyer)
    hall.connect("east", kitchen)
    hall.connect("west", dining)
    hall.connect("north", throne)
    dining.connect("east", hall)
    kitchen.connect("west", hall)
    kitchen.connect("hatch", hidden)
    hidden.connect("ladder", kitchen)

    #Populating rooms with various items
    foyer.items.append(Item("mysterious vial", "a sparkling liquid swirls around the glass as if it's alive", "heal", 20))
    dining.items.append(Item("silver fork", "useful for eating, but can also stab things you don't like", "attack", 3))
    dining.items.append(Item("leftover turkey", "it's perfectly cooked but cold to the touch, unfortunately", "heal", 16))
    throne.items.append(Item("black crown", "a heavy crown carved from obsidian", "defense", 2))
    hidden.items.append(Item("Darksun", "an obsidian blade likely possessed by a demonic entity", "attack", 10))
    hidden.items.append(Item("Brightmoon", "a crescent-shaped shield that glows eternally", "defense", 5))

    #Populating rooms with scary enemies
    hall.enemies.append(Enemy("Amnesiac", 8, 3, 1))
    throne.enemies.append(Enemy("Eternus", 50, 23, 3))
    kitchen.enemies.append(Enemy("Zurkey", 14, 13, 1))
    hidden.enemies.append(Enemy("Dweller", 20, 15, 2))
    dining.enemies.append(Enemy("Shadow", 10, 5, 5))

    #Starting position for player
    return foyer


def gameLoop(player):
    print("~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~")
    print("You awaken from what feels like an eternal slumber...")
    print("As your eyes fully open and you stumble to your feet, you feel a warm, welcoming presence.")
    print("It seems to impart knowledge directly into your mind:")
    print("Welcome to the House of Eterna, stranger. You've entered a new world, one full of ancient mysteries.")
    print("There is plenty of treasure to be found, but not without a fight.")
    print("Fear not though, for I've left you a small gift to protect you on your journey.")
    print("Type 'help' if you're ever lost, and my spirit will guide you.")
    print("Otherwise, good luck on your adventure. Farewell!")
    print("~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~")

    while True:
        room = player.currentRoom
        print(room.describe())

        command = input("> ").strip().lower()

        if command == "help":
            print("Commands:")
            print("  go <direction>")
            print("  look")
            print("  stats")
            print("  inventory")
            print("  take <item>")
            print("  use <item>")
            print("  attack <enemy>")
            print("  quit\n")

        elif command.startswith("go "):
            direction = command[3:]
            nextRoom = room.getExit(direction)
            if nextRoom is None:
                print("You can't go that way.\n")
            else:
                player.moveTo(nextRoom)

        elif command == "look":
            print(room.describe())

        elif command == "stats":
            player.showStats()

        elif command == "inventory":
            player.showInventory()

        elif command.startswith("take "):
            itemName = command[5:]
            found = None
            for item in room.items:
                if item.name.lower() == itemName:
                    found = item
                    break
            if found is None:
                print("That item is not here.\n")
            else:
                player.inventory.append(found)
                room.items.remove(found)
                print("You pick up " + found.name + ".\n")

        elif command.startswith("use "):
            itemName = command[4:]
            found = None
            for item in player.inventory:
                if item.name.lower() == itemName:
                    found = item
                    break
            if found is None:
                print("You don't have that item.\n")
            else:
                found.use(player)
                player.inventory.remove(found)
                print()

        elif command.startswith("attack "):
            enemyName = command[7:]
            attackEnemy(player, enemyName)

        elif command == "quit":
            print("Goodbye!")
            break

        else:
            print("I don't understand that command.\n")


def playGame():
    if __name__ == "__main__":
        player = Player("Glennis", 20, 5, 2)
        start = createWorld()
        player.moveTo(start)
        gameLoop(player)


#START HERE
playGame()