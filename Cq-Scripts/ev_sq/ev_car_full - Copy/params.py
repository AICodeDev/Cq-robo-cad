# params.py

class CarParams:
    
    AXLE_LENGTH = 96.0
    AXLE_THICKNESS = 7.2
    AXLE_Z_HEIGHT = 50.0  # Your translate((0,0,50))
    AXLE_X_OFFSET = 80.0  # Your translate((80,0,0))
    
    
    
     # Bush Holder Plate Dimensions
    BUSH_HOLDER_PLATE_L = 68.0  # (84 - 16)
    BUSH_HOLDER_PLATE_W = 24.0
    BUSH_HOLDER_PLATE_T = 2.0
    
    # Positioning for the Bush Holder
    BUSH_HOLDER_X_OFFSET = 80.0
    BUSH_HOLDER_Z_HEIGHT = 0.0
    
    
    
   # Bracket Base
    BUSH_HOLDER_BRACKET_BASE_W = 8.0
    BUSH_HOLDER_BRACKET_BASE_L = 16.0
    BUSH_HOLDER_BRACKET_BASE_H = 8.0
    BUSH_HOLDER_BRACKET_BASE_HOLE_D = 3.96
    BUSH_HOLDER_BRACKET_BASE_HOLE_OFFSET = 4.0 # Distance from center
    
    # Bracket Upright
    BUSH_HOLDER_BRACKET_UPRIGHT_W = 3.0
    BUSH_HOLDER_BRACKET_UPRIGHT_H = 60.0 
    BUSH_HOLDER_BRACKET_AXLE_HOLE_D = 12.0
    BUSH_HOLDER_BRACKET_AXLE_Z = 50.0
    
    
    
    
    # Wheel Dimensions
    WHEEL_DIAMETER = 60.0
    WHEEL_WIDTH = 25.0
    AXLE_DIAMETER = 5.0
    
    # Chassis Dimensions
    CHASSIS_LENGTH = 200.0
    CHASSIS_WIDTH = 100.0
    CHASSIS_THICKNESS = 10.0
    
    # Clearances (The "Gap" to make things fit)
    FIT_TOLERANCE = 0.5 
    WHEEL_OFFSET = 5.0  # Distance from chassis side to wheel
