import datetime

class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
    
    def age(self, current_year):
        current_date_time = datetime.datetime.now()
        current_year = currentdatetime.year
        return current_year - self.year
    
    def display_specs(self):
        return str(self.year) + " " + self.make + " " + self.model
    
    def is_vintage(self, years):
        if self.age(years) > 25:
            return True
        else:
            return False
    
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def increaseX(self):
        self.x += 1
        
    def increaseY(self):
        self.y += 1
        
    def decreaseX(self):
        self.x -= 1
        
    def decreaseY(self):
        self.y -= 1
        
    def to_string(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"
    
#Example of composition
class Turtle:
    def __init__(self):
        self.location = Point(0,0)
        
    def up(self):
        self.location.decreaseY()
        
    def down(self):
        self.location.increaseY()
        
    def right(self):
        self.location.increaseX()
        
    def left(self):
        self.location.decreaseX()
        
    def to_string(self):
        return self.location.to_string()

#Example 1
my_car = Vehicle("Chevy", "Cruze", 2003)
print(my_car.age(2025))
print(my_car.display_specs())
print(my_car.is_vintage(26))

#Example 2
franklin = Turtle()
print("Franklin starts at", franklin.to_string())

counter = 0
while counter < 5:
    franklin.down()
    franklin.right()
    print("The turtle is on the move!")
    counter += 1
print("Franklin ends at", franklin.to_string())