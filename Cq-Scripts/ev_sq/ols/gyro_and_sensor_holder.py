import cadquery as cq
import math

# Ultrasound Hole 4 MM - distance 16 mm, width 24 mm , height 8 mm
# Gyro Hole 3 MM - distance 20 mm,len=25 width 15 mm , height 8 mm


plate_t = 1.5 
hole_d =  4 #4mm
hole_d_small =  2.8 #4mm


board_x_outer =104 
board_y_outer =72 
board_x_hole_d = 96 #+12 104
board_y_hole_d = 64 #+872

board_x_hole =board_x_hole_d/2
board_y_hole = board_y_hole_d/2

board_x_inner=board_x_hole_d -10
board_y_inner=board_y_hole_d -10

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



#i
#board = board.translate( (-21,0,0))

#show_object(board)

board_cut_inner = (
    cq.Workplane("XY")    
    .rect(board_x_inner, board_y_inner)
    .extrude(plate_t)
)
#show_object(board_cut_inner)
#board_cut = board.cut(board_cut_inner)

#show_object(board_cut)


#board = board.cut(board_cut_inner)

conn = (
    cq.Workplane("XY")    
    .rect(16, 16)
    .extrude(plate_t)
)
#show_object(conn)
conn = (conn.translate((board_x_outer/2 + 8,0,0)) )
#show_object(conn)

full_y=board_y_outer + 48
full_x=30
half_y=full_y/2
half_x=full_x/2




main_plate_y=88
half_main_plate_y = main_plate_y/2

L_plate_y=92
half_L_plate_y=L_plate_y/2

plate_y = full_y     # width (X)
plate_x = full_x      # height (Z)










    


plate = (
    cq.Workplane("XY")    
    .rect(plate_x, plate_y)
    .extrude(plate_t)
)


plate_join= plate




#56.40

main_gyro_plate_with_hole2= ( plate_join
            .faces(">Z")
            .workplane()
            .pushPoints([

            
          

           ( -(10)  ,plate_y/2-4-4),
           (-(10)  ,-plate_y/2+4+4),
           ( +(10)  ,plate_y/2-4-4),
           (+(10)  ,-plate_y/2+4+4),

          
            ])

            .hole(hole_d_small) ) 
#show_object(main_gyro_plate_with_hole2)


#show_object(motor_hole_rect)




wheel_con_x=24
wheel_con_y=2.5 #thinkness
wheel_con_z=8+plate_t #height


wheel_con_plate = (
    cq.Workplane("XY")    
    .rect(wheel_con_x, wheel_con_y)  
    .extrude(wheel_con_z)
)

wheel_con_plate_hole= ( wheel_con_plate
            .faces(">Y")
            .workplane()
            .pushPoints([
            
           
            #Left Row
            ( -8,0+4 ),
            #( -6,0+4+8 ) ,
         
            
            ( +8,0+4 ),
            #( +6,0+4+8) ,
          
           

            ])

            .hole(hole_d) ) 

wheel_con_plate_hole_y = wheel_con_plate_hole.rotate((0, 0, 0), (0, 0, 1), 90) 

#show_object(wheel_con_plate_hole_y)

wheel_con_plate_hole_y_final = wheel_con_plate_hole_y.translate( (board_x_outer/2 + 8 +4+2+1 ,0,0)) 

#show_object(wheel_con_plate_hole_y_final)



wheel_con_plate_hole2 = wheel_con_plate_hole.translate( (full_x/2 -12 ,full_y/2-1.5,0))

#show_object(wheel_con_plate_hole2)
wheel_con_plate_hole_couple = wheel_con_plate_hole2.mirror(mirrorPlane="XZ", union=True)
#show_object(wheel_con_plate_hole_couple)

final_chasis_ev=main_gyro_plate_with_hole2.union(wheel_con_plate_hole_couple).union(board)

#show_object(final_chasis_ev)

final_chasis_ev2= final_chasis_ev.cut(board_cut_inner).union(conn).union(wheel_con_plate_hole_y_final)
show_object(final_chasis_ev2)

