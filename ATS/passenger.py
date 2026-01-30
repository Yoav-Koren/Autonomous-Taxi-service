import random
import math

class Passenger:
    def __init__(self,ID, StartXPos = None ,StartYPos = None,EndXPos = None,EndYPos = None,Color = None):
        self.ID = ID
        self.StartXPos = random.randint(0,20000)
        self.StartYPos = random.randint(0,20000)
        self.Color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        
        Max_Distance = random.randint(1,2000) # Generates a max distance for the end point
        XDistanceDeviation = random.randint(-Max_Distance,Max_Distance) # Generates how much X Moves based on the starting max distance
        Temp_XEndPoint = self.StartXPos - XDistanceDeviation # Stores the new End point X 

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
        Temp_YEndPoint = self.StartYPos - YDistanceDeviation

        
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
        
        print("start: ", self.StartXPos," ",self.StartYPos)
        print("end: ", self.EndXPos," ",self.EndYPos)
        StartPoint = (self.StartXPos,self.StartYPos)
        EndPoint = (self.EndXPos,self.EndYPos)
        Distance_Traveled = int(math.dist(StartPoint,EndPoint)) # Calculates the distance between 2 points using \(d=\sqrt{(x_{2}-x_{1})^{2}+(y_{2}-y_{1})^{2}}\)
        print("Distance To Destination: ",Distance_Traveled)



        
    def get_start_point(self):
        return (self.StartXPos,self.StartYPos)
    def get_end_point(self):
        return (self.EndXPos,self.EndYPos)