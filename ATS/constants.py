class Constant: 
    
    SCREEN_W, SCREEN_H = 1280, 720  

    TIME_SCALE = 1

    GRID_SIZE = 20_000   

    BASE_CELL_SIZE = 32   

    MAX_PASSENGER_DISTANCE = 2000  
    
    TAXI_SPEED = 20
       
    MIN_ZOOM = 0.1
           
    MAX_ZOOM = 4.0  
               
    CAMERA_SPEED = 800              
     
    GRID_COLOR = (80, 80, 80)    

    BG_COLOR = (25, 25, 25)   

    TAXI_AMOUNT = 10

    # Interval of which to spawn a new Passenger in seconds
    NEW_PASSENGER_TIMER_INTERVAL = 20.0

    # Interval of which to assign a taxi to a passenger in seconds
    ASSIGN_TAXI_TIMER_INTERVAL = 1.0

    # Interval of which a taxi will drive, move in seconds
    DRIVE_TAXI_TIMER_INTERVAL = 1.0

    # Interval of that dictates who often to update the camera to follow a taxi in seconds
    FOLLOW_TAXI_TIMER_INTERVAL = 1.0

    WINDOW_CAPTION = "Taxi Service"