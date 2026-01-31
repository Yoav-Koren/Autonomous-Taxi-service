import random
import math

class Passenger:
    def __init__(self,ID, CurrentXPos = None ,CurrentYPos = None,EndXPos = None,EndYPos = None,Color = None):
        self.ID = ID
        self.CurrentXPos = random.randint(0,20000)
        self.CurrentYPos = random.randint(0,20000)
        self.Color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        
        Max_Distance = random.randint(1,2000) # Generates a max distance for the end point
        XDistanceDeviation = random.randint(-Max_Distance,Max_Distance) # Generates how much X Moves based on the Currenting max distance
        Temp_XEndPoint = self.CurrentXPos - XDistanceDeviation # Stores the new End point X 

        if (Temp_XEndPoint) > 20000: # Checks if the new X end point is inside the grid if not, we store the overflow for when we move Y end point
            OverFlow = Temp_XEndPoint - 20000 # Overflow incase our new generated point is outside our grid system
            Max_Distance = (Max_Distance - abs(XDistanceDeviation)) + OverFlow # We add back the overflow back into the max distance to compensate
            self.EndXPos = 20000 # We set the end point as the max column 
        elif (Temp_XEndPoint) < 0: # We do the same checks but for if the we get an overflow but in the negative
            OverFlow = 0 - Temp_XEndPoint 
            Max_Distance = (Max_Distance - abs(XDistanceDeviation)) + OverFlow
            self.EndXPos = 1
        else:
            self.EndXPos = Temp_XEndPoint # We set the new end point as the one we calculated earlier
            Max_Distance = (Max_Distance - abs(XDistanceDeviation)) # We subtract the distance traveled on the X axis from the max distance traveled

        YDistanceDeviation = random.randint(-Max_Distance,Max_Distance)
        Temp_YEndPoint = self.CurrentYPos - YDistanceDeviation

        
        if (Temp_YEndPoint) > 20000: # Checks if the new X end point is inside the grid if not, we store the overflow for when we move Y end point
            OverFlow = Temp_YEndPoint - 20000 # Overflow incase our new generated point is outside our grid system
            Max_Distance = (Max_Distance - abs(YDistanceDeviation)) + OverFlow # We add back the overflow back into the max distance to compensate
            self.EndYPos = 20000 # We set the end point as the max column 
        elif (Temp_YEndPoint) < 0: # We do the same checks but for if the we get an overflow but in the negative
            OverFlow = 0 - Temp_YEndPoint 
            Max_Distance = (Max_Distance - abs(YDistanceDeviation)) + OverFlow
            self.EndYPos = 1
        else:
            self.EndYPos = Temp_YEndPoint # We set the new end point as the one we calculated earlier
            Max_Distance = (Max_Distance - abs(YDistanceDeviation)) # We subtract the distance traveled on the X axis from the max distance traveled
        
        print("Current: ", self.CurrentXPos," ",self.CurrentYPos)
        print("end: ", self.EndXPos," ",self.EndYPos)
        Manhatten_Distance = abs(self.CurrentXPos - self.EndXPos) + abs(self.CurrentYPos - self.EndYPos) # Calculates the distance based on manhatten formula 
        print("Manhaten Distance: ",Manhatten_Distance)



        
    def get_current_point(self):
        return (self.CurrentXPos,self.CurrentYPos)
    def get_end_point(self):
        return (self.EndXPos,self.EndYPos)