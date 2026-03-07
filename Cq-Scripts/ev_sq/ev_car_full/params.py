# params.py
#152, 7.9
#4+16
#wheel68
#10

# params.py
import math


    # Wheel Hard Dimensions
  


class CarParams:
    CAP_PIPE_HOLE_SIDE: float = 8.1    
    
    CAP_PIPE_DIA = 12.4
    CAP_PIPE_BUSH_HOLE_DIA = CAP_PIPE_DIA + 0.5
    
    CAP_PIPE_TOP_DIA: float = 11 + 2 -0.1 #small 12.9 
    CAP_PIPE_BASE_DIA: float =  CAP_PIPE_TOP_DIA + 2 -0.1 #Big #14.8
    CAP_PIPE_BASE_HEIGHT: float = 1.0
    CAP_PIPE_TOP_HEIGHT: float = 12
    
    
    

    # Gearbox (Left Part)
    MOTOR_GB_W = 16.0
    MOTOR_GB_L = 56.0
    MOTOR_GB_H = 24.0
    
    # Motor (Right Part)
    MOTOR_CYL_D = 36.0
    MOTOR_CYL_H = 28.0
    
    # Holes
    MOTOR_HOLE_D = 4.0

    
    WHEEL_HARD_OUTER_RIM_RADIUS = 68 / 2
    WHEEL_HARD_RIM_THICKNESS = 3.2
    WHEEL_HARD_RIM_HEIGHT = 18.0
    WHEEL_HARD_RIM_WIDTH = 4.0 # Used for inner rim calculation
    
    WHEEL_HARD_HUB_DIAMETER = 18.5 
    WHEEL_HARD_HUB_HEIGHT = 16.0 + 3
    WHEEL_HARD_HUB_EXTRUDE_ADD = 10.0
    
    WHEEL_HARD_SPOKE_COUNT = 6
    WHEEL_HARD_SPOKE_THICKNESS = 4.0
    WHEEL_HARD_SPOKE_HEIGHT = 9+1
    
    # Cutout Dimensions
    WHEEL_HARD_AXLE_HOLE_D = 4.15
    WHEEL_HARD_RECT_CUT_SIZE_MIN = 7.8
    WHEEL_HARD_RECT_CUT_SIZE = 7.85
    WHEEL_HARD_RECT_CUT_SIZE_CLEAR = 7.9
    WHEEL_HARD_RECT_CUT_SIZE_CLEAR_EASY = 7.95
    
    ##################### BIG 


    BWHEEL_HARD_OUTER_RIM_RADIUS = 72 / 2
    BWHEEL_HARD_RIM_THICKNESS = 2.4
    BWHEEL_HARD_RIM_HEIGHT = 35
    BWHEEL_HARD_RIM_WIDTH = 4.0 # Used for inner rim calculation
    
    BWHEEL_HARD_HEX_HEIGHT = 16.0
    
    
    BWHEEL_HARD_HUB_DIAMETER = 16  #16.5
    
    BWHEEL_HARD_HUB_HEIGHT = BWHEEL_HARD_RIM_HEIGHT
    
    BWHEEL_HARD_HUB_EXTRUDE_ADD = 10.0
    
    BWHEEL_HARD_SPOKE_COUNT  =6
    BWHEEL_HARD_SPOKE_THICKNESS = 4.0 -2
    BWHEEL_HARD_SPOKE_HEIGHT = BWHEEL_HARD_RIM_HEIGHT - BWHEEL_HARD_HEX_HEIGHT
    
    # Cutout Dimensions
    BWHEEL_HARD_AXLE_HOLE_D = 4.1
    BWHEEL_HARD_RECT_CUT_SIZE = 8.5
    BWHEEL_HARD_DIA = 7.5
    BWHEEL_HARD_RADIUS = BWHEEL_HARD_DIA/2
    BWHEEL_HARD_HEX_DIS = 6.7
    BWHEEL_HARD_HEX_HEIGHT = 15
    
    
    AXLE_LENGTH = 152
    AXLE_THICKNESS = 7.9
    AXLE_Z_HEIGHT = 50.0  # Your translate((0,0,50))
    AXLE_X_OFFSET = 80.0  # Your translate((80,0,0))
    
    
    
    GEAR_CUT_L = 20.0  # Length of the cutout (along X)
    GEAR_CUT_W = 12.0  # Width of the cutout (along Y)
     # Bush Holder Plate Dimensions
    BUSH_HOLDER_PLATE_L = 112  # (84 - 16)
    BUSH_HOLDER_PLATE_W = 24.0*8+24+18-24
    BUSH_HOLDER_PLATE_T = 3.2
    
    # Positioning for the Bush Holder
    BUSH_HOLDER_X_OFFSET = 80.0
    BUSH_HOLDER_Z_HEIGHT = 0.0
    
     # Bush Holder Plate

    
    # Matching Hole Pattern
    # This spacing is used by BOTH the bracket and the plate
    HOLE_SPACING_Y = 8.0 # (Total distance 8mm, so +/- 4mm from center)
    HOLE_X_OFFSET_FROM_CENTER = 20.0 # Where brackets sit on the plate
    
   # Bracket Base
    BUSH_HOLDER_BRACKET_BASE_W = 12
    BUSH_HOLDER_BRACKET_BASE_L = 24
    BUSH_HOLDER_BRACKET_BASE_H = 4
    BUSH_HOLDER_BRACKET_BASE_HOLE_D = 3.96
    BUSH_HOLDER_BRACKET_BASE_HOLE_OFFSET = 4.0 # Distance from center
    
    # Bracket Upright
    BUSH_HOLDER_BRACKET_UPRIGHT_W = 4.0
    BUSH_HOLDER_BRACKET_UPRIGHT_H = 28
    BUSH_HOLDER_BRACKET_AXLE_HOLE_D = 15
    BUSH_HOLDER_BRACKET_AXLE_Z = BUSH_HOLDER_BRACKET_UPRIGHT_H/2+4
    
    
    
    
    # Wheel Dimensions
  
    
    # Chassis Dimensions
    CHASSIS_LENGTH = 200.0
    CHASSIS_WIDTH = 100.0
    CHASSIS_THICKNESS = 10.0
    
    # Clearances (The "Gap" to make things fit)
    FIT_TOLERANCE = 0.5 
    WHEEL_OFFSET = 5.0  # Distance from chassis side to wheel
