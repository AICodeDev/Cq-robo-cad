import cadquery as cq
import math
"""
26	+26+ 36 =88 (inner plate
Hole	34+64=98
26	
36	
88	
"""

hole_d=3.9
"""
wheel_con_x=24
wheel_con_y=3
wheel_con_z=24


wheel_con_plate = (
    cq.Workplane("XY")    
    .rect(wheel_con_x, wheel_con_y)  
    .extrude(wheel_con_z)
)

wheel_con_plate_hole= ( wheel_con_plate
            .faces(">Y")
            .workplane()
            .pushPoints([
            #( 0,0),
            #Middle Row
            ( 0,0+4),
            ( 0,0+4+8) ,
            ( 0,0+4+16),
            #Left Row
            ( -8,0+4),
            ( -8,0+4+8) ,
            ( -8,0+4+16),
            
            ( +8,0+4),
            ( +8,0+4+8) ,
            ( +8,0+4+16),
           

            ])

            .hole(hole_d) ) 

show_object(wheel_con_plate_hole)
"""

new_x=72
new_y=8+8
new_full_height=16

main_rod = (
    cq.Workplane("XY")    
    .rect(new_x, new_y)
    .extrude(new_full_height)
)
show_object(main_rod)

cut_rod2 = (
    cq.Workplane("XY")    
    .rect(new_x-16+2, new_y)
    .extrude(new_full_height-4)
)
show_object(cut_rod2)

cut_rod3 = (
    cq.Workplane("XY")    
    .rect(new_x, new_y/2)
    .extrude(new_full_height-4)
    .translate((0,-4,0))
)
show_object(cut_rod3)


main_rod_c1=main_rod.cut(cut_rod2)
main_rod_c2=main_rod_c1.cut(cut_rod3)



rv_front_holder= ( main_rod_c2
            .faces(">Z")
            .workplane()
            .pushPoints([ 
            # (0 ,4),
             #(0 ,-4),
  
             (40/2,0),
             (-40/2,0),
             (56/2,-4),
             (-56/2,-4),
             (64/2,4),
             (-64/2,4),   

            ]).hole(hole_d) )


show_object(rv_front_holder)
result = rv_front_holder.mirror(mirrorPlane="XY")
show_object(result)

"""

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

main_sq_hole = (
    cq.Workplane("XY")    
    .rect(main_sq_hole_x, main_sq_hole_y)
    .extrude(plate_t)
)
#show_object(main_sq_hole)

board_x_hole =board_x_hole_d/2
board_y_hole = board_y_hole_d/2

board_x_inner=board_x_hole_d -10
board_y_inner=board_y_hole_d -10

board_cut_inner = (
    cq.Workplane("XY")    
    .rect(board_x_inner, board_y_inner)
    .extrude(plate_t)
)
#show_object(board_cut_inner)
board = (
    cq.Workplane("XY")    
    .rect(board_x_outer, board_y_outer)
    .extrude(plate_t)
)

board= ( board
            .faces(">Z")
            .workplane()
            .pushPoints([ 
             (board_x_hole ,board_y_hole ),
             (-board_x_hole ,-board_y_hole ),
              (board_x_hole ,-board_y_hole ),
             (-board_x_hole ,+board_y_hole )  

            ]).hole(hole_d) )


board = board.cut(board_cut_inner)





board = board.translate( (-21,0,0))

show_object(board)



motor_hole_rect_y= 98- (34*2)# 30 = 15 Up and 15 down from center+


motor_hole_rect=(
    cq.Workplane("XY")  
    .rect(plate_x, motor_hole_rect_y)
    

)
plate = (
    cq.Workplane("XY")    
    .rect(plate_x, plate_y)
    .extrude(plate_t)
)
plate= plate.cut(main_sq_hole)


motor_sq_rod_x=24
motor_sq_rod_y=8
motor_sq_rod_z=8


motor_sqplate = (
    cq.Workplane("XY")    
    .rect(motor_sq_rod_x, motor_sq_rod_y)
  
    .extrude(motor_sq_rod_z+plate_t)
)
#show_object(motor_sqplate)
motor_sqplate_moved= motor_sqplate.translate((plate_x/2 -motor_sq_rod_x/2 , motor_hole_rect_y/2, 0))
#show_object(motor_sqplate_moved)

plate_join= plate.union(motor_sqplate_moved)


main_plate_with_hole= ( plate_join
            .faces(">Z")
            .workplane()
            .pushPoints([
            ( plate_x/2-4 ,15),
            ( plate_x/2-4 -16 ,15)
            ])

            .hole(hole_d) ) 
show_object(main_plate_with_hole)

#56.40

main_plate_with_hole2= ( main_plate_with_hole
            .faces(">Z")
            .workplane()
            .pushPoints([
            (  -(plate_x/2-4) ,0),
            (  -(plate_x/2-4) ,20),
            (  -(plate_x/2-4) ,-20),
            (  -(plate_x/2-4) ,56/2),
            (  -(plate_x/2-4) ,-56/2),
            (  -(plate_x/2-12) ,56/2),
            (  -(plate_x/2-12) ,-56/2),
            (  -(plate_x/2-12) ,32/2),
            (  -(plate_x/2-12) ,-32/2),


            ( -(plate_x/2-12)  ,0),

            
           ( -(0)  ,plate_y/2-4),
           (-(0)  ,-plate_y/2+4),

            ( -(8)  ,plate_y/2-4),
           (-(8)  ,-plate_y/2+4),
            ( -(16)  ,plate_y/2-4),
           (-(16)  ,-plate_y/2+4),
            ( -(24)  ,plate_y/2-4),
           (-(24)  ,-plate_y/2+4),


            
          ( +(plate_x/2 -4)  ,plate_y/2-4-8),
           (+( plate_x/2 -4 )  ,-plate_y/2+4+8),
            ( +(plate_x/2 -12)  ,plate_y/2-4-8),
           (+( plate_x/2 -12 )  ,-plate_y/2+4+8),

            ])

            .hole(hole_d) ) 
show_object(main_plate_with_hole2)


#show_object(motor_hole_rect)





wheel_con_plate_hole2 = wheel_con_plate_hole.translate( (full_x/2 -12 ,full_y/2-1.5,plate_t))
#show_object(wheel_con_plate_hole2)
wheel_con_plate_hole_couple = wheel_con_plate_hole2.mirror(mirrorPlane="XZ", union=True)
show_object(wheel_con_plate_hole_couple)

final_chasis_ev=main_plate_with_hole2.union(wheel_con_plate_hole_couple).union(board)

show_object(final_chasis_ev)
"""