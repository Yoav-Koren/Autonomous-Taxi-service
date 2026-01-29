import random

class Taxi:
    def __init__(self,CurrentXPos,CurrentYPos, Color, Speed = 20, GoalXPos = None, GoalYPos = None):
        self.CurrentXPos = CurrentXPos
        self.CurrentYPos = CurrentYPos
        self.Color = Color

    def get_current_position(self):
        return (self.CurrentXPos,self.CurrentYPos)
    
    