import random
import math

from constants import Constant
from utils import Utils

class Passenger:
    def __init__(self,ID, current_x_pos = None ,current_y_pos = None,end_x_pos = None,end_y_pos = None,color = None):
        self.ID = ID
        self.current_x_pos = random.randint(0,Constant.GRID_SIZE-1)
        self.current_y_pos = random.randint(0,Constant.GRID_SIZE-1)
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.max_distance = random.randint(1,Constant.MAX_PASSENGER_DISTANCE) # Generates a max distance for the end point
        self._generate_endpoint()
    
    def get_current_point(self):
        return (self.current_x_pos,self.current_y_pos)
    
    def get_end_point(self):
        return (self.end_x_pos,self.end_y_pos)

    def _generate_endpoint(self):
        self._generate_x_endpoint()
        self._generate_y_endpoint()
        if self.current_x_pos == self.end_x_pos and self.current_y_pos == self.end_y_pos:
            while self.current_x_pos == self.end_x_pos and self.current_y_pos == self.end_y_pos:
                self._generate_x_endpoint()
                self._generate_y_endpoint()
        print("Current: ", self.current_x_pos," ",self.current_y_pos)
        print("end: ", self.end_x_pos," ",self.end_y_pos)
        # Calculates the distance based on manhatten formula 
        manhatten_distance = Utils.calculate_manhatten_distance(self.current_x_pos,
                                                                self.end_x_pos,self.
                                                                current_y_pos,self.
                                                                end_y_pos) 
        print("Manhaten Distance: ",manhatten_distance)

    def _generate_x_endpoint(self):
        # Generates how much X Moves based on the Currenting max distance
        x_distance_deviation = random.randint(-self.max_distance,self.max_distance) 
        temp_x_end = self.current_x_pos - x_distance_deviation # Stores the new End point X 
        if (temp_x_end) >= Constant.GRID_SIZE: # Checks if the new X end point is inside the grid if not, we store the over_flow for when we move Y end point
            over_flow = temp_x_end - Constant.GRID_SIZE - 1 # over_flow incase our new generated point is outside our grid system
            self.max_distance = (self.max_distance - abs(x_distance_deviation)) + over_flow # We add back the over_flow back into the max distance to compensate
            self.end_x_pos = Constant.GRID_SIZE - 1 # We set the end point as the max column 
        elif (temp_x_end) < 0: # We do the same checks but for if the we get an over_flow but in the negative
            over_flow = 0 - temp_x_end 
            self.max_distance = (self.max_distance - abs(x_distance_deviation)) + over_flow
            self.end_x_pos = 0
        else:
            self.end_x_pos = temp_x_end # We set the new end point as the one we calculated earlier
            if (self.max_distance - abs(x_distance_deviation)) >= 0:
                self.max_distance = (self.max_distance - abs(x_distance_deviation)) # We subtract the distance traveled on the X axis from the max distance traveled
            else:
                self.max_distance = 0  
        

    def _generate_y_endpoint(self):
        # Generates how much Y Moves based on the Currenting max distance
        if self.max_distance > 0:
            y_distance_deviation = random.randint(-self.max_distance,self.max_distance)
            temp_y_end = self.current_y_pos - y_distance_deviation
            if (temp_y_end) >= Constant.GRID_SIZE: # Checks if the new Y end point is inside the grid if not, we store the over_flow for when we move Y end point
                over_flow = temp_y_end - Constant.GRID_SIZE - 1 # over_flow incase our new generated point is outside our grid system
                self.max_distance = (self.max_distance - abs(y_distance_deviation)) + over_flow # We add back the over_flow back into the max distance to compensate
                self.end_y_pos = Constant.GRID_SIZE - 1 # We set the end point as the max column 
            elif (temp_y_end) < 0: # We do the same checks but for if the we get an over_flow but in the negative
                over_flow = 0 - temp_y_end 
                self.max_distance = (self.max_distance - abs(y_distance_deviation)) + over_flow
                self.end_y_pos = 0
            else:
                self.end_y_pos = temp_y_end # We set the new end point as the one we calculated earlier
                self.max_distance = (self.max_distance - abs(y_distance_deviation)) # We subtract the distance traveled on the X axis from the max distance traveled
        else:
            self.end_y_pos = self.current_y_pos
        




        
