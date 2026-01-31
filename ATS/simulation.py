import random
import pygame
import sys
import math
from passenger import Passenger
from taxi import Taxi

# Initialize Pygame 
pygame.init()  

# Window size in pixels
SCREEN_W, SCREEN_H = 1280, 720   

# Grid size 
GRID_SIZE = 20_000   

# Base size of one cell
BASE_CELL_SIZE = 32      

# Minimum zoom       
MIN_ZOOM = 0.1

# Maximum zoom           
MAX_ZOOM = 4.0  

# Camera move speed                
CAMERA_SPEED = 800              
 
# Grid line color 
GRID_COLOR = (80, 80, 80)    

# Background color (dark gray)
BG_COLOR = (25, 25, 25)   

# Taxi number
TAXI_NUMBER = 10

# Passenger Increment
PASSENGER_NUMBER = 0

# Create the window
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))  
# Names Window
pygame.display.set_caption("Taxi Service") 

# Clock to control frame rate
clock = pygame.time.Clock()  

# Starting Camera Position
camera_x = 0.0
camera_y = 0.0

# Starting zoom level
zoom = 1.0
zoom_sensitivity = 0.15

# Starting Taxi array
taxi_list: list[Taxi] =[]
passenger_que: list[Passenger] =[]

# Generate Random Taxis
for i in range(TAXI_NUMBER):
    temp = Taxi(i)
    print(temp.ID, temp.get_current_position())
    taxi_list.append(temp)


# Timer for functions
NEW_PASSENGER_TIMER = 0.0
NEW_PASSENGER_TIMER_INTERVAL =20.0

ASSIGN_TAXI_TIMER = 0.0
ASSIGN_TAXI_TIMER_INTERVAL = 1.0

DRIVE_TAXI_TIMER = 0.0
DRIVE_TAXI_TIMER_INTERVAL = 1.0

running = True
while running:
    dt = clock.tick(60) / 1000.0 # Delta Time so events are fps driven not clock driven
    NEW_PASSENGER_TIMER += dt
    ASSIGN_TAXI_TIMER += dt
    DRIVE_TAXI_TIMER += dt

    # Events:
    for event in pygame.event.get():

        # Exit loop when window is closed
        if event.type == pygame.QUIT:
            running = False  

        # Listens to mousewheel events and changes zoom accordingly
        if event.type == pygame.MOUSEWHEEL:
            old_zoom = zoom  
            zoom += event.y * zoom_sensitivity # Adjusts zoom based on scroll 
            zoom = max(MIN_ZOOM, min(MAX_ZOOM, zoom))  # Keeps zoom between max and min zoom

            # Zoom toward mouse position
            mx, my = pygame.mouse.get_pos()  # Mouse position on screen
            camera_x = (camera_x + mx) * (zoom / old_zoom) - mx
            camera_y = (camera_y + my) * (zoom / old_zoom) - my



    # Listens to keyboard for keys for camera movement
    keys = pygame.key.get_pressed()
    move = CAMERA_SPEED * dt  # How many pixels to move camera based on delta time

    if keys[pygame.K_a]:  # Move left
        camera_x -= move
    if keys[pygame.K_d]:  # Move right
        camera_x += move
    if keys[pygame.K_w]:  # Move up
        camera_y -= move
    if keys[pygame.K_s]:  # Move down
        camera_y += move
    if keys[pygame.K_x]:
        try:
            # Ask user for input in the console
            row_input = input("Enter row number (0 to {}): ".format(GRID_SIZE-1))
            col_input = input("Enter column number (0 to {}): ".format(GRID_SIZE-1))
            
            row = int(row_input)
            col = int(col_input)

            # Clamp values so they stay inside grid
            row = max(0, min(GRID_SIZE-1, row))
            col = max(0, min(GRID_SIZE-1, col))

            # Move camera so that the cell is at the top-left of the screen
            cell_size = BASE_CELL_SIZE * zoom
            camera_x = col * cell_size
            camera_y = row * cell_size

        except ValueError:
            print("Invalid input! Please enter integers.")

    # Keeps Camera Inside Grid
    camera_x = max(0, min(camera_x, GRID_SIZE * BASE_CELL_SIZE * zoom))
    camera_y = max(0, min(camera_y, GRID_SIZE * BASE_CELL_SIZE * zoom))

    
    screen.fill(BG_COLOR)  # Clear screen
    cell_size = BASE_CELL_SIZE * zoom  # Calculates cell size based on current zoom

    # Checks how many and which cells are currently visible
    start_col = int(camera_x // cell_size) # Checks the first column is currently visable by dividing the current place of the camera in the world by the size of a simple cell
    start_row = int(camera_y // cell_size) # Checks the first row is currently visable by dividing the current place of the camera in the world by the size of a simple cell
    end_col = int((camera_x + SCREEN_W) // cell_size) + 1 # Checks which column is currently the last by dividing the current place of the camera in the world by the size of the screen and also by the size of the cell
    end_row = int((camera_y + SCREEN_H) // cell_size) + 1 # Checks which row is currently the last by dividing the current place of the camera in the world by the size of the screen and also by the size of the cell

    # Clamp visible cells to the grid size
    start_col = max(0, start_col)
    start_row = max(0, start_row)
    end_col = min(GRID_SIZE, end_col)
    end_row = min(GRID_SIZE, end_row)

    # Draw only visible cells
    for row in range(start_row, end_row):

        for col in range(start_col, end_col):
            x = col * cell_size - camera_x  # Convert world X to screen X
            y = row * cell_size - camera_y  # Convert world Y to screen Y
            rect = pygame.Rect(x, y, cell_size, cell_size)

            # Draw grid lines if zoomed in enough
            if cell_size >= 5:
                pygame.draw.rect(screen, GRID_COLOR, rect, 1)

            # Checks if the cell is a taxi position cell and paints it
            if cell_size >= 5:
                for taxi in taxi_list: 
                    if taxi.get_current_position() == (row, col):
                        rect_taxi = pygame.Rect(x, y, cell_size, cell_size)
                        pygame.draw.rect(screen, taxi.Color, rect_taxi)
            
            # Checks if the cell is a passenger and draws a circle
            if cell_size >= 5:
                for passenger in passenger_que: # Checks for unassigned passengers
                    if passenger.get_current_point() == (row,col):
                        pygame.draw.circle(screen, passenger.Color, (x + cell_size // 2, y + cell_size // 2), cell_size // 2)
                for taxi in taxi_list: # Checks for passengers
                   if taxi.has_passenger_assigned():
                        if taxi.OwnPassenger.get_current_point() == (row,col):
                            pygame.draw.circle(screen, taxi.OwnPassenger.Color, (x + cell_size // 2, y + cell_size // 2), cell_size // 2)

               

            # Checks if the cell is a passenger end point and draws a star
            if cell_size >= 5:
                for passenger in passenger_que: # Checks for unassigned passengers
                    if passenger.get_end_point() == (row,col):
                        pygame.draw.polygon(        
                            screen,
                            passenger.Color,
                            [
                                (x + cell_size * 0.5, y),                    
                                (x + cell_size * 0.6, y + cell_size * 0.35),
                                (x + cell_size,       y + cell_size * 0.4),
                                (x + cell_size * 0.7, y + cell_size * 0.65),
                                (x + cell_size * 0.8, y + cell_size),
                                (x + cell_size * 0.5, y + cell_size * 0.8),
                                (x + cell_size * 0.2, y + cell_size),
                                (x + cell_size * 0.3, y + cell_size * 0.65),
                                (x,                   y + cell_size * 0.4),
                                (x + cell_size * 0.4, y + cell_size * 0.35),
                            ]
                        )
                for taxi in taxi_list: # Checks for passengers
                    if taxi.has_passenger_assigned():  
                        if taxi.OwnPassenger.get_end_point() == (row,col):
                            pygame.draw.polygon(        
                                screen,
                                taxi.OwnPassenger.Color,
                                [
                                    (x + cell_size * 0.5, y),                    
                                    (x + cell_size * 0.6, y + cell_size * 0.35),
                                    (x + cell_size,       y + cell_size * 0.4),
                                    (x + cell_size * 0.7, y + cell_size * 0.65),
                                    (x + cell_size * 0.8, y + cell_size),
                                    (x + cell_size * 0.5, y + cell_size * 0.8),
                                    (x + cell_size * 0.2, y + cell_size),
                                    (x + cell_size * 0.3, y + cell_size * 0.65),
                                    (x,                   y + cell_size * 0.4),
                                    (x + cell_size * 0.4, y + cell_size * 0.35),
                                ]
                        )

    # Creates a passenger every 20 seconds and also increments the id
    if NEW_PASSENGER_TIMER >= NEW_PASSENGER_TIMER_INTERVAL:   
        temp_passenger = Passenger(PASSENGER_NUMBER) # Creates a new passenger
        passenger_que.append(temp_passenger) # Adds the passenger to the que
        print("Que: ",len(passenger_que))
        PASSENGER_NUMBER = PASSENGER_NUMBER + 1 # Id increment
        NEW_PASSENGER_TIMER -= NEW_PASSENGER_TIMER_INTERVAL  # subtract instead of reset to prevent drift

    # Checks every second if there are passengers in the que, if there are, we check the distance to the first passenger in the que, and assign the closes taxi to him, and also removing them from the que
    if ASSIGN_TAXI_TIMER >= ASSIGN_TAXI_TIMER_INTERVAL: 
        if len(passenger_que) > 0: # Checks if the que is not empty
            empty_taxi_list : list[Taxi]= [] 
            for taxi in taxi_list:
                if taxi.has_passenger_assigned() == False:
                    empty_taxi_list.append(taxi) # Creates and adds all empty taxis to the list because we dont need to calculate the distance to occupied taxis
            print("Empty Taxis: ",len(empty_taxi_list))
            if len(empty_taxi_list) > 0: 
                closest_taxi:Taxi  = empty_taxi_list[0] # Stores the closest taxi as the first one just so i dont have to deal with Null
                # current_smallest_distance = int(math.dist(passenger_que[0].get_current_point(),closest_taxi.get_current_position())) 
                current_smallest_distance = abs(closest_taxi.CurrentXPos - passenger_que[0].CurrentXPos) + abs(closest_taxi.CurrentYPos - passenger_que[0].CurrentYPos) # Calculates the distance and stores the distance of the closest taxi 
                for empty_taxi  in empty_taxi_list: # For each empty Taxi i run a check to see if the distance between the passenger and this empty taxi is smaller than the one already stored
                    # distance = int(math.dist(passenger_que[0].get_current_point(),empty_taxi.get_current_position())) 
                    distance = abs(empty_taxi.CurrentXPos - passenger_que[0].CurrentXPos) + abs(empty_taxi.CurrentYPos - passenger_que[0].CurrentYPos)# Calculates the distance to the passenger
                    print("Taxi: ",empty_taxi.ID, empty_taxi.get_current_position()) 
                    print("Distance to Passenger: ",distance)
                    if current_smallest_distance > distance: # If the current closest taxi is actually farther than the the distance of the newly calculated one i just replace the closest taxi and its distance with the closest one
                        closest_taxi = empty_taxi
                        current_smallest_distance = distance
                print("Closest Taxi: ",closest_taxi.ID, closest_taxi.get_current_position())
                print("Distance: ", current_smallest_distance)
                if taxi_list[closest_taxi.ID].OwnPassenger is None:
                    empty_taxi_list.clear() # Clears all the taxis as for next check
                    taxi_list[closest_taxi.ID].OwnPassenger = passenger_que[0] # Asigns the closest taxi this new passenger
                    passenger_que.pop() # Removes passenger from que as it has been handled
        ASSIGN_TAXI_TIMER -= ASSIGN_TAXI_TIMER_INTERVAL 

    if DRIVE_TAXI_TIMER >= DRIVE_TAXI_TIMER_INTERVAL:
        for taxi in taxi_list:
            taxi.drive()
        DRIVE_TAXI_TIMER -= DRIVE_TAXI_TIMER_INTERVAL 

    pygame.display.flip()  # Update screen 

#Closes simulation
pygame.quit()  
sys.exit()     