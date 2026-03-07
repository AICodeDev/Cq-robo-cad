import cadquery as cq
import math

# Ultrasound Hole 4 MM - distance 16 mm, width 24 mm , height 8 mm
# Gyro Hole 3 MM - distance 20 mm,len=25 width 15 mm , height 8 mm


plate_t = 1.5 
hole_d =  4 #4mm
hole_d_small =  3 #4mm


plate_y = hole_d_small +2      # width (X)
plate_x = 20+5      # height (Z)

plate = (
    cq.Workplane("XY")    
    .rect(plate_x, plate_y)
    .extrude(1.5)
)
#show_object(plate)
holes= ( plate
            .faces(">Z")
            .workplane()
            .pushPoints([
          
           (-10  ,0),
           ( +10  ,0)          
          
            ])
            .hole(hole_d_small ) 
            ) 
show_object(holes)

"""

"""
