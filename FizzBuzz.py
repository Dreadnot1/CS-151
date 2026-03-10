def while_badger(num):
    counter = 1
    print("Your number was", num)
    while counter <= num:
        if (counter % 3 == 0) and (counter % 5 == 0):
            print("SNAKE!!!!")
            counter += 1
        elif (counter % 3 == 0):
            print("Badger!")
            counter += 1
        elif (counter % 5 == 0):
            print("Mushroom!")
            counter += 1
        else:
            print(counter)
            counter += 1

while_badger(4)