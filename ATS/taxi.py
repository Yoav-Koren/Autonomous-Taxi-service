import random

class Taxi:
    def __init__(self,ID ,CurrentXPos = None ,CurrentYPos = None , Color =None , Speed = 20, ):
        self.ID = ID
        self.CurrentXPos = random.randint(0,20000)
        self.CurrentYPos = random.randint(0,20000)
        self.Color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.Speed = Speed

    def get_current_position(self):
        return (self.CurrentXPos,self.CurrentYPos)
    
    