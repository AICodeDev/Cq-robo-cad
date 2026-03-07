import cadquery as cq
import math

# Ultrasound Hole 4 MM - distance 16 mm, width 24 mm , height 8 mm
# Gyro Hole 3 MM - distance 20 mm,len=25 width 15 mm , height 8 mm


plate_t = 1.5 
hole_d =  4 #4mm
hole_d_small =  2.8 #4mm

sonic_conn = (
    cq.Workplane("XY")    
    .rect(16, 16)
    .extrude(plate_t)
)
sonic_conn = (sonic_conn.translate((board_x_outer/2 + 8,0,0)) )
sonic_con_x=24
sonic_con_y=2.5 #thinkness
sonic_con_z=8+plate_t #height
sonic_con_plate_base = (
    cq.Workplane("XY")    
    .rect(sonic_con_x, sonic_con_y)  
    .extrude(sonic_con_z)
    .faces(">Y")
    .workplane()
    .pushPoints([
       ( -8,0+4 ),            
      ( +8,0+4 ),
    ])
    .hole(hole_d)
)
sonic_con_plate_hole_y = sonic_con_plate_base.rotate((0, 0, 0), (0, 0, 1), 90) 
sonic_con_plate_hole_y_final = sonic_con_plate_hole_y.translate( (104/2 + 8 +7 ,0,0)) 
sonic_con_plate_hole_x = sonic_con_plate_base.translate( ( 0 ,72/2+1.5,0))
sonic_con_plate_hole_x_couple = sonic_con_plate_hole_x.mirror(mirrorPlane="XZ", union=True)
sonic_con_plate_hole_x_triple=sonic_con_plate_hole_x_couple.union(sonic_con_plate_hole_y_final)
