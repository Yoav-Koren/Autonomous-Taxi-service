import random
import pygame
import sys
import math
from constants import Constant
from passenger import Passenger
from taxi import Taxi
from utils import Utils


class Simulation:

    def __init__(self):

        # Pygame environment
        self.screen = None
        self.clock = None

        # Passenger Increment
        self.passenger_id_incrementor = 0

        # Timer for functions
        self.new_passenger_spawn_timer = 0.0
        self.assign_taxi_timer = 0.0
        self.drive_taxi_timer = 0.0
        self.follow_taxi_timer = 0.0

        # Follow function
        self.do_follow = True
        self.follow_id = None
        

        # Starting Camera Position
        self.camera_x = 0.0
        self.camera_y = 0.0

        # Starting zoom level
        self.zoom = 1.0
        self.zoom_sensitivity = 0.15
        
        # Starting Taxi and Passenger arrays
        self.taxi_list: list[Taxi] =[]
        self.passenger_que: list[Passenger] =[]

        # Simulation loop
        self.running = True

        # Delta Time
        self.dt = 0

        # Current cell size based on zoom
        self.cell_size = Constant.BASE_CELL_SIZE
    

    def pygame_setup(self):

        # Initialize Pygame 
        pygame.init()  

        # Create the window
        self.screen = pygame.display.set_mode((Constant.SCREEN_W, Constant.SCREEN_H)) 

        # Names Window
        pygame.display.set_caption(Constant.WINDOW_CAPTION) 

        # Clock to control frame rate
        self.clock = pygame.time.Clock()  

    def create_taxis(self):
      # Generate Random Taxis
        for i in range(Constant.TAXI_AMOUNT):
            temp = Taxi(i)
            print(temp.ID, temp.get_current_position())
            self.taxi_list.append(temp)  
     
    # Updates the timers
    def _update_timers(self):
            self.new_passenger_spawn_timer += self.dt
            self.assign_taxi_timer +=  self.dt
            self.drive_taxi_timer +=  self.dt
            self.follow_taxi_timer +=  self.dt

    def _check_pygame_events(self):
            # Events:
            for event in pygame.event.get():

            # Exit loop when window is closed
                if event.type == pygame.QUIT:
                    self.running = False  

                # Listens to mousewheel events and changes zoom accordingly
                if event.type == pygame.MOUSEWHEEL:
                    old_zoom = self.zoom  
                    self.zoom += event.y * self.zoom_sensitivity # Adjusts zoom based on scroll 
                    self.zoom = max(Constant.MIN_ZOOM, min(Constant.MAX_ZOOM, self.zoom))  # Keeps zoom between max and min zoom

                    # Zoom toward mouse position
                    mx, my = pygame.mouse.get_pos()  # Mouse position on screen
                    self.camera_x = (self.camera_x + mx) * (self.zoom / old_zoom) - mx
                    self.camera_y = (self.camera_y + my) * (self.zoom / old_zoom) - my

    def _check_keyboard_events(self):

        # Listens to keyboard for keys for camera movement
        keys = pygame.key.get_pressed()
        move = Constant.CAMERA_SPEED * self.dt  # How many pixels to move camera based on delta time

        if keys[pygame.K_a]:  # Move left
            self.camera_x -= move
        if keys[pygame.K_d]:  # Move right
            self.camera_x += move
        if keys[pygame.K_w]:  # Move up
            self.camera_y -= move
        if keys[pygame.K_s]:  # Move down
            self.camera_y += move
        if keys[pygame.K_f]:  # Follow
            self.do_follow = True
            self.follow_id = int(input("Enter taxi id number: "))
        if keys[pygame.K_g]:  # Un Follow
            self.do_follow = False
        if keys[pygame.K_x]:
            try:

                # Ask user for input in the console
                row_input = input("Enter row number (0 to {}): ".format(Constant.GRID_SIZE-1))
                col_input = input("Enter column number (0 to {}): ".format(Constant.GRID_SIZE-1))
            
                row = int(row_input)
                col = int(col_input)

                # Clamp values so they stay inside grid
                row = max(0, min(Constant.GRID_SIZE-1, row))
                col = max(0, min(Constant.GRID_SIZE-1, col))

                # Move camera so that the cell is at the top-left of the screen
                self.cell_size = Constant.BASE_CELL_SIZE * self.zoom
                self.camera_x = col * self.cell_size
                self.camera_y = row * self.cell_size

            except ValueError:
                print("Invalid input! Please enter integers.")


    def _rending_loop(self):
            
            # Keeps Camera Inside Grid
            self.camera_x = max(0, min(self.camera_x, Constant.GRID_SIZE * Constant.BASE_CELL_SIZE * self.zoom))
            self.camera_y = max(0, min(self.camera_y, Constant.GRID_SIZE * Constant.BASE_CELL_SIZE * self.zoom))

                
            self.screen.fill(Constant.BG_COLOR)  # Clear screen
            self.cell_size = Constant.BASE_CELL_SIZE * self.zoom  # Calculates cell size based on current zoom

            # Checks how many and which cells are currently visible
            start_col = int(self.camera_x // self.cell_size) # Checks the first column is currently visable by dividing the current place of the camera in the world by the size of a simple cell
            start_row = int(self.camera_y // self.cell_size) # Checks the first row is currently visable by dividing the current place of the camera in the world by the size of a simple cell
            end_col = int((self.camera_x + Constant.SCREEN_W) // self.cell_size) + 1 # Checks which column is currently the last by dividing the current place of the camera in the world by the size of the screen and also by the size of the cell
            end_row = int((self.camera_y + Constant.SCREEN_H) // self.cell_size) + 1 # Checks which row is currently the last by dividing the current place of the camera in the world by the size of the screen and also by the size of the cell
            
            # Clamp visible cells to the grid size
            start_col = max(0, start_col)
            start_row = max(0, start_row)
            end_col = min(Constant.GRID_SIZE, end_col)
            end_row = min(Constant.GRID_SIZE, end_row)

            # Grabs only visible cells
            for row in range(start_row, end_row):
                for col in range(start_col, end_col):
                    x = col * self.cell_size - self.camera_x  # Convert world X to screen X
                    y = row * self.cell_size - self.camera_y  # Convert world Y to screen Y
                    rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                    
                    # Draw grid lines if zoomed in enough
                    if self.cell_size >= 5:
                        pygame.draw.rect(self.screen, Constant.GRID_COLOR, rect, 1)
                        self._taxi_tile_rendering(row, col, x, y)
                        self._passenger_tile_rendering(row, col, x, y)
                        self._passenger_end_point_tile_rendering(row, col, x, y)


    # Checks if the cell is a passenger end point and draws a star
    def _passenger_end_point_tile_rendering(self, row, col, x, y):
        for passenger in self.passenger_que: # Checks for unassigned passengers
            if passenger.get_end_point() == (row,col):
                pygame.draw.polygon(        
                            self.screen,
                            passenger.Color,
                            [
                                (x + self.cell_size * 0.5, y),                    
                                (x + self.cell_size * 0.6, y + self.cell_size * 0.35),
                                (x + self.cell_size,       y + self.cell_size * 0.4),
                                (x + self.cell_size * 0.7, y + self.cell_size * 0.65),
                                (x + self.cell_size * 0.8, y + self.cell_size),
                                (x + self.cell_size * 0.5, y + self.cell_size * 0.8),
                                (x + self.cell_size * 0.2, y + self.cell_size),
                                (x + self.cell_size * 0.3, y + self.cell_size * 0.65),
                                (x,                   y + self.cell_size * 0.4),
                                (x + self.cell_size * 0.4, y + self.cell_size * 0.35),
                            ]
                        )
        for taxi in self.taxi_list: # Checks for passengers
            if taxi.has_passenger_assigned():  
                if taxi.OwnPassenger.get_end_point() == (row,col):
                    pygame.draw.polygon(        
                                self.screen,
                                taxi.OwnPassenger.Color,
                                [
                                    (x + self.cell_size * 0.5, y),                    
                                    (x + self.cell_size * 0.6, y + self.cell_size * 0.35),
                                    (x + self.cell_size,       y + self.cell_size * 0.4),
                                    (x + self.cell_size * 0.7, y + self.cell_size * 0.65),
                                    (x + self.cell_size * 0.8, y + self.cell_size),
                                    (x + self.cell_size * 0.5, y + self.cell_size * 0.8),
                                    (x + self.cell_size * 0.2, y + self.cell_size),
                                    (x + self.cell_size * 0.3, y + self.cell_size * 0.65),
                                    (x,                   y + self.cell_size * 0.4),
                                    (x + self.cell_size * 0.4, y + self.cell_size * 0.35),
                                ]
                        )

    # Checks if the cell is a taxi position cell and paints it
    def _passenger_tile_rendering(self, row, col, x, y):
        for passenger in self.passenger_que: # Checks for unassigned passengers
            if passenger.get_current_point() == (row,col):
                pygame.draw.circle(self.screen, passenger.Color, (x + self.cell_size // 2, y + self.cell_size // 2), self.cell_size // 2)
        for taxi in self.taxi_list: # Checks for assigned passengers
           if taxi.has_passenger_assigned():
                if taxi.OwnPassenger.get_current_point() == (row,col):
                    pygame.draw.circle(self.screen, taxi.OwnPassenger.Color, (x + self.cell_size // 2, y + self.cell_size // 2), self.cell_size // 2)

    # Checks if the cell is a passenger and draws a circle
    def _taxi_tile_rendering(self, row, col, x, y):
        for taxi in self.taxi_list: 
            if taxi.get_current_position() == (row, col):
                rect_taxi = pygame.Rect(x, y, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, taxi.Color, rect_taxi)

    def _run_timers(self):
        self._spawn_new_passenger()
        self._assign_passengers()
        self._update_all_taxis()
        self._follow_camera_loop()



    # Checks every second if there are passengers in the que, 
    # if there are, we check the distance to the first passenger in the que, 
    # and assign the closes taxi to him,
    # and also removing them from the que
    def _assign_passengers(self):    
        if self.assign_taxi_timer >= Constant.ASSIGN_TAXI_TIMER_INTERVAL: 
            print("Que: ",len(self.passenger_que))
            empty_taxi_list = self._grab_empty_taxis()
            if len(empty_taxi_list) > 0: 
                closest_taxi:Taxi  = empty_taxi_list[0] # Stores the closest taxi as the first one just so i dont have to deal with Null
                current_smallest_distance = Utils._calculate_manhatten_distance(closest_taxi.CurrentXPos, 
                                                                               self.passenger_que[0].CurrentXPos,
                                                                               closest_taxi.CurrentYPos, 
                                                                               self.passenger_que[0].CurrentYPos) # Calculates the distance and stores the distance of the closest taxi 
                closest_taxi = self._calculate_closest_taxi(empty_taxi_list, current_smallest_distance)
                if self.taxi_list[closest_taxi.ID].OwnPassenger is None:
                    print("Closest Taxi: ",closest_taxi.ID, closest_taxi.get_current_position())
                    empty_taxi_list.clear() # Clears all the taxis as for next check
                    self.taxi_list[closest_taxi.ID].OwnPassenger = self.passenger_que[0] # Asigns the closest taxi this new passenger
                    self.passenger_que.pop() # Removes passenger from que as it has been handled
            self.assign_taxi_timer -= Constant.ASSIGN_TAXI_TIMER_INTERVAL 

    def _calculate_closest_taxi(self, empty_taxi_list, current_smallest_distance) -> Taxi:
        closest_taxi = empty_taxi_list[0]
        for empty_taxi  in empty_taxi_list: # For each empty Taxi i run a check to see if the distance between the passenger and this empty taxi is smaller than the one already stored
            # Calculates the distance to the passenger
            distance = Utils._calculate_manhatten_distance(empty_taxi.CurrentXPos,
                                                                  self.passenger_que[0].CurrentXPos,
                                                                  empty_taxi.CurrentYPos, 
                                                                  self.passenger_que[0].CurrentYPos)
            print("Taxi: ",empty_taxi.ID, empty_taxi.get_current_position()) 
            print("Distance to Passenger: ",distance)
            if current_smallest_distance > distance: # If the current closest taxi is actually farther than the the distance of the newly calculated one i just replace the closest taxi and its distance with the closest one
                closest_taxi = empty_taxi
                current_smallest_distance = distance
        print("Smallest Distance: ", current_smallest_distance)        
        return closest_taxi  
        
    
    def _update_all_taxis(self):
        if self.drive_taxi_timer >= Constant.DRIVE_TAXI_TIMER_INTERVAL:
            for taxi in self.taxi_list:
                taxi.drive()
            self.drive_taxi_timer -= Constant.DRIVE_TAXI_TIMER_INTERVAL 

    # Creates and adds all empty taxis to the list because we dont need to calculate the distance to occupied taxis
    def _grab_empty_taxis(self):
        empty_taxi_list : list[Taxi]= [] 
        if len(self.passenger_que) > 0: # Checks if the que is not empty
            for taxi in self.taxi_list:
                if taxi.has_passenger_assigned() == False:
                    empty_taxi_list.append(taxi) 
        print("Empty Taxis: ",len(empty_taxi_list))
        return empty_taxi_list

    # Creates a passenger every 20 seconds and also increments the id
    def _spawn_new_passenger(self):
        if self.new_passenger_spawn_timer >= Constant.NEW_PASSENGER_TIMER_INTERVAL:   
            temp_passenger = Passenger(self.passenger_id_incrementor) # Creates a new passenger
            self.passenger_que.append(temp_passenger) # Adds the passenger to the que
            print("Que: ",len(self.passenger_que))
            self.passenger_id_incrementor += 1 # Id increment
            self.new_passenger_spawn_timer -= Constant.NEW_PASSENGER_TIMER_INTERVAL  # subtract instead of reset to prevent drift


    def _follow_camera_loop(self):
        if self.follow_taxi_timer >= Constant.FOLLOW_TAXI_TIMER_INTERVAL and self.do_follow == True:
            try:
                if self.follow_id is not None:
                    row = self.taxi_list[self.follow_id].CurrentXPos
                    col = self.taxi_list[self.follow_id].CurrentYPos

                    # Clamp taxi position to grid
                    row = max(0, min(Constant.GRID_SIZE - 1, row))
                    col = max(0, min(Constant.GRID_SIZE - 1, col))

                    # Cell size with zoom applied
                    self.cell_size = Constant.BASE_CELL_SIZE * self.zoom

                    # World size of the map
                    map_width = Constant.GRID_SIZE * self.cell_size
                    map_height = Constant.GRID_SIZE * self.cell_size

                    # Taxi world position (center of its cell)
                    taxi_world_x = col * self.cell_size + self.cell_size / 2
                    taxi_world_y = row * self.cell_size + self.cell_size / 2

                    # Camera position (top-left of the screen in world coords)
                    self.camera_x = taxi_world_x - Constant.SCREEN_W / 2
                    self.camera_y = taxi_world_y - Constant.SCREEN_H / 2

                    # Clamp camera to map bounds
                    self.camera_x = max(0, min(map_width - Constant.SCREEN_W, self.camera_x))
                    self.camera_y = max(0, min(map_height - Constant.SCREEN_H, self.camera_y))
            except ValueError:
                print("Invalid Taxi Number!")
            self.follow_taxi_timer -= Constant.FOLLOW_TAXI_TIMER_INTERVAL 

    def start_simulation(self):
        self.pygame_setup()
        self.create_taxis()
        while self.running:
            self.dt = self.clock.tick(60) / 1000.0 # Delta Time so events are fps driven not clock driven
            self._update_timers()
            self._check_pygame_events()
            self._check_keyboard_events()
            self._rending_loop()
            self._run_timers()

            pygame.display.flip()  # Update screen 

        #Closes simulation
        pygame.quit()  
        sys.exit() 


def main():
    sim = Simulation()
    sim.start_simulation()

if __name__ == "__main__":
    main()
