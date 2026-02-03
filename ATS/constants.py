class Constant: 
    
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
    CAMERA_speed = 800              
    
    # Grid line color 
    GRID_color = (80, 80, 80)    

    # Background color (dark gray)
    BG_color = (25, 25, 25)   

    # Taxi number
    TAXI_AMOUNT = 10

    # Interval of which to spawn a new Passenger
    NEW_PASSENGER_TIMER_INTERVAL = 20.0

    # Interval of which to assign a taxi to a passenger
    ASSIGN_TAXI_TIMER_INTERVAL = 1.0

    # Interval of which a taxi will drive, move 
    DRIVE_TAXI_TIMER_INTERVAL = 1.0

    # Interval of that dictates who often to update the camera to follow a taxi
    FOLLOW_TAXI_TIMER_INTERVAL = 1.0

    WINDOW_CAPTION = "Taxi Service"