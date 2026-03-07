import cadquery as cq
import math

# Ultrasound Hole 4 MM - distance 16 mm, width 24 mm , height 8 mm
# Gyro Hole 3 MM - distance 20 mm,len=25 width 15 mm , height 8 mm


ghole_d_small =  3 #4mm
gplate_y = 96 + 48     # width (X)
gplate_x = 30      # height (Z)
gplate2 = (
    cq.Workplane("XY")    
    .rect(30, 96 + 48)
    .extrude(2.5)
    .faces(">Z")
            .workplane()
            .pushPoints([

           ( -(10.1)  ,gplate_y/2-8),
           (-(10.1)  ,-gplate_y/2+8),
           ( +(10.1)  ,gplate_y/2-8),
           (+(10.1)  ,-gplate_y/2+8),

          
            ])

            .hole(ghole_d_small)    
)
show_object(gplate2)
