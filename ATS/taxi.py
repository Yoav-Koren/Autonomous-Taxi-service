import random
import math
from passenger import Passenger

class Taxi:
    def __init__(self,ID ,CurrentXPos = None ,CurrentYPos = None , Color = None , Speed = 20, IsDriving = False, PickedUpPassenger = False ,OwnPassenger : Passenger = None):
        self.ID = ID
        self.CurrentXPos = random.randint(0,20000)
        self.CurrentYPos = random.randint(0,20000)
        self.Color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.Speed = Speed
        self.IsDriving = IsDriving
        self.PickedUpPassenger = PickedUpPassenger
        self.OwnPassenger = OwnPassenger

    def get_current_position(self):
        return (self.CurrentXPos,self.CurrentYPos)
    
    def has_passenger_assigned(self):
        return self.OwnPassenger is not None 
    
    def has_passenger_picked_up(self): # Checks if the taxis location is the same as the passenger because that would mean they pick them up 
        if self.CurrentXPos == self.OwnPassenger.CurrentXPos and self.CurrentYPos == self.OwnPassenger.CurrentYPos:
            self.PickedUpPassenger = True
            print("Taxi ", self.ID, " has reached passenger at:", self.OwnPassenger.get_current_point())
        else:
            self.PickedUpPassenger = False
        return self.PickedUpPassenger

        
    def is_driving_to_dropoff(self): # Checks if the taxis location is the same as the passenger and that we are not at the end point
        if self.has_passenger_picked_up() and (self.CurrentXPos != self.OwnPassenger.EndXPos and self.CurrentYPos != self.OwnPassenger.EndYPos):
            return True
        else:
            return False
        
    def has_order_finished(self): # Checks if the taxis location is the same as the passenger and that we are at the end point
        if self.has_passenger_picked_up() and (self.CurrentXPos == self.OwnPassenger.EndXPos and self.CurrentYPos == self.OwnPassenger.EndYPos):
            self.OwnPassenger = None
            return True
        else:
            return False

    def is_driving(self):
        if self.OwnPassenger is not None: # If the taxi is assigned a passenger
            if self.has_passenger_picked_up() == False: # If the taxis current location is different from the passenger that would mean that we have to drive there
                self.IsDriving = True
            elif self.is_driving_to_dropoff(): # Checks if the taxi is driving to the passenger dropoff
                self.IsDriving =  True
            elif self.has_order_finished(): # Checks if the taxi and the passenger are at the drop off
                self.IsDriving =  False
        else:
            self.IsDriving =  False
        return self.IsDriving
        
    def drive(self):
        if self.OwnPassenger is None:
            print("Taxi number ", self.ID," has no passenger")
        elif self.has_passenger_picked_up() == False:
            distanceX = self.OwnPassenger.CurrentXPos - self.CurrentXPos # Calculates the distance between current taxi X and current taxi X
            distanceY = self.OwnPassenger.CurrentYPos - self.CurrentYPos # Calculates the distance between current taxi Y and current taxi Y
            if abs(distanceX) >= abs(distanceY): # Checks which distance between X or Y is bigger
                # If X distance is bigger:
                move_distance_clamp = min(self.Speed, distanceX) # Returns which every is smaller, speed or distance to X as to make sure i dont overshoot
                move_distance = max(-self.Speed, move_distance_clamp) # Returns which ever is greater, speed in the oppsite direcation or negetive speed, -speed ≤ movement ≤ speed
                self.CurrentXPos += move_distance
                print("Taxi ", self.ID, " Moved ",move_distance, " along the X axis and has reached: ",self.get_current_position())
            else: 
                # If Y distance is bigger:
                move_distance_clamp = min(self.Speed, distanceY)
                move_distance = max(-self.Speed, move_distance_clamp)
                self.CurrentYPos+= move_distance
                print("Taxi ", self.ID, " Moved ",move_distance, " along the Y axis and has reached: ",self.get_current_position())
            
            #
            Manhatten_Distance = abs(self.CurrentXPos - self.OwnPassenger.CurrentXPos) + abs(self.CurrentYPos - self.OwnPassenger.CurrentYPos)
            print(" Manhatten Distance:", Manhatten_Distance)
            self.has_passenger_picked_up()
     
            
            
    
    