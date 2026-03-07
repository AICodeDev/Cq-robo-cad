import cadquery as cq
import math

full_y=98
full_x=full_y * 2-18
half_y=full_y/2

hole_d =  4 #4mm
main_plate_y=88
half_main_plate_y = main_plate_y/2

L_plate_y=92
half_L_plate_y=L_plate_y/2

plate_y = full_y     # width (X)
plate_x = full_x      # height (Z)
plate_t = 3 

board_x_outer =104
board_y_outer =72
board_x_hole_d = 96 #+12 104
board_y_hole_d = 64 #+872

main_sq_hole_x =board_x_outer+24+12+6
main_sq_hole_y =board_y_outer




board_x_hole =board_x_hole_d/2
board_y_hole = board_y_hole_d/2

board_x_inner=board_x_hole_d -10
board_y_inner=board_y_hole_d -10







motor_sq_rod_x=32
motor_sq_rod_y=8
motor_sq_rod_z=3


motor_sqplate = (
    cq.Workplane("XY")    
    .rect(motor_sq_rod_x, motor_sq_rod_y)
  
    .extrude(motor_sq_rod_z)
)
#show_object(motor_sqplate)
#motor_sqplate_moved= motor_sqplate.translate((plate_x/2 -motor_sq_rod_x/2 , motor_hole_rect_y/2, 0))
#show_object(motor_sqplate_moved)




main_plate_adaptor_with_hole= ( motor_sqplate
            .faces(">Z")
            .workplane()
            .pushPoints([
            
            ( -4 ,0),
            ( -12 ,0),

            ( 4 ,0),
            ( 12 ,0),

            ])
            .hole(hole_d) ) 
show_object(main_plate_adaptor_with_hole)
