import random
import math
from constants import Constant
from passenger import Passenger
from utils import Utils

class Taxi:
    def __init__(self,ID ,current_x_pos = None ,current_y_pos = None , color = None , speed = Constant.TAXI_SPEED, is_driving = False, picked_up_passenger = False ,own_passenger : Passenger = None):
        self.ID = ID
        self.current_x_pos = random.randint(0,Constant.GRID_SIZE-1)
        self.current_y_pos = random.randint(0,Constant.GRID_SIZE-1)
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.speed = speed
        self.is_driving = is_driving
        self.picked_up_passenger = picked_up_passenger
        self.own_passenger = own_passenger

    def get_current_position(self):
        return (self.current_x_pos,self.current_y_pos)
    
    def has_passenger_assigned(self):
        return self.own_passenger is not None 
    
    # Checks if the taxis location is the same as the passenger because that would mean they pick them up
    def has_passenger_picked_up(self): 
        if (self.current_x_pos == self.own_passenger.current_x_pos and self.current_y_pos == self.own_passenger.current_y_pos) and self.picked_up_passenger == False and self.own_passenger is not None:
            if self.current_x_pos == self.own_passenger.current_x_pos and self.current_y_pos == self.own_passenger.current_y_pos:
                print("Taxi ", self.ID, " has reached passenger at:", self.own_passenger.get_current_point())
                self.picked_up_passenger = True
            else:
                self.picked_up_passenger = False
        return self.picked_up_passenger

    # Checks if the taxis location is the same as the passenger and that we are at the end point  
    def has_order_finished(self): 
        if self.has_passenger_picked_up() and (self.current_x_pos == self.own_passenger.end_x_pos and self.current_y_pos == self.own_passenger.end_y_pos):
            print("Passenger Dropped Off, freeing taxi:",self.ID)
            self.own_passenger = None
            self.picked_up_passenger = False
            return True
        else:
            return False
    
    # Returns if the taxi is currently driving
    def is__currently_driving(self):
        if self.own_passenger is not None: # If the taxi is assigned a passenger
            if self.has_passenger_picked_up() == False: # If the taxis current location is different from the passenger that would mean that we have to drive there
                self.is_driving = True
            elif self.is_driving_to_dropoff(): # Checks if the taxi is driving to the passenger dropoff
                self.is_driving =  True
            elif self.has_order_finished(): # Checks if the taxi and the passenger are at the drop off
                self.is_driving =  False
        else:
            self.is_driving =  False
        return self.is_driving
    
    def _drive_to_passenger(self):
            distance_x = self.own_passenger.current_x_pos - self.current_x_pos # Calculates the distance between current passenger X and current taxi X
            distance_y = self.own_passenger.current_y_pos - self.current_y_pos # Calculates the distance between current passenger Y and current taxi Y
            if abs(distance_x) >= abs(distance_y): # Checks which distance between X or Y is bigger
                # If X distance is bigger:
                move_distance_clamp = min(self.speed, distance_x) # Returns which every is smaller, speed or distance to X as to make sure i dont overshoot
                move_distance = max(-self.speed, move_distance_clamp) # Returns which ever is greater, speed in the oppsite direcation or negetive speed, -speed ≤ movement ≤ speed
                if (self.current_x_pos + move_distance) > Constant.GRID_SIZE:
                    self.current_x_pos = Constant.GRID_SIZE - 1
                else:
                    self.current_x_pos += move_distance
                print("Taxi ", self.ID, " Moved ",move_distance, " along the X axis and has reached: ",self.get_current_position())
            else: 
                # If Y distance is bigger:
                move_distance_clamp = min(self.speed, distance_y)
                move_distance = max(-self.speed, move_distance_clamp)
                if (self.current_y_pos + move_distance) > Constant.GRID_SIZE:
                    self.current_y_pos = Constant.GRID_SIZE  - 1
                else:
                    self.current_y_pos += move_distance
                print("Taxi ", self.ID, " Moved ",move_distance, " along the Y axis and has reached: ",self.get_current_position())
            manhatten_distance = Utils.calculate_manhatten_distance(self.current_x_pos,
                                                                    self.own_passenger.current_x_pos,
                                                                    self.current_y_pos,
                                                                    self.own_passenger.current_y_pos)
            print("Manhatten Distance:", manhatten_distance," To Passenger:",self.own_passenger.get_current_point())
            self.has_passenger_picked_up() # Checks if by the end of the current drive the taxi reached the passenger

    def _drive_to_endpoint(self):
            distance_x = self.own_passenger.end_x_pos - self.current_x_pos 
            distance_y = self.own_passenger.end_y_pos - self.current_y_pos
            if abs(distance_x) >= abs(distance_y): # Checks which distance between X or Y is bigger
                # If X distance is bigger:
                move_distance_clamp = min(self.speed, distance_x) # Returns which every is smaller, speed or distance to X as to make sure i dont overshoot
                move_distance = max(-self.speed, move_distance_clamp) # Returns which ever is greater, speed in the oppsite direcation or negetive speed, -speed ≤ movement ≤ speed
                if (self.current_x_pos + move_distance) >= Constant.GRID_SIZE:
                    self.current_x_pos = Constant.GRID_SIZE - 1
                    self.own_passenger.current_x_pos = Constant.GRID_SIZE -1
                else:
                    self.current_x_pos += move_distance
                    self.own_passenger.current_x_pos += move_distance
                print("Taxi ", self.ID, " Moved ",move_distance, " along the X axis and has reached: ",self.get_current_position())
            else: 
                # If Y distance is bigger:
                move_distance_clamp = min(self.speed, distance_y)
                move_distance = max(-self.speed, move_distance_clamp)
                if (self.current_y_pos + move_distance) >= Constant.GRID_SIZE:
                    self.current_y_pos = Constant.GRID_SIZE-1
                    self.own_passenger.current_y_pos = Constant.GRID_SIZE-1
                else:
                    self.current_y_pos += move_distance
                    self.own_passenger.current_y_pos += move_distance
                
                print("Taxi ", self.ID, " Moved ",move_distance, " along the Y axis and has reached: ",self.get_current_position())
            manhatten_distance =  Utils.calculate_manhatten_distance(self.current_x_pos,
                                                                     self.own_passenger.end_x_pos,
                                                                     self.current_y_pos,
                                                                     self.own_passenger.end_y_pos)
            print("Manhatten Distance:", manhatten_distance, " To End Point:",self.own_passenger.get_end_point())
            self.has_order_finished() 
        
    def drive(self):
        if self.own_passenger is None: # If the Taxi has no passenger it is not driving 
            print("Taxi number ", self.ID," has no passenger")
        elif self.picked_up_passenger == False: # If the taxi is driving to pick up a passenger
            self._drive_to_passenger()
        elif self.picked_up_passenger: # Checks if the passenger has been picked up and the taxi is moving to the end point
            self._drive_to_endpoint()


                        
  


            
            
    
    