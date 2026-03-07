import cadquery as cq
import math

# Ultrasound Hole 4 MM - distance 16 mm, width 24 mm , height 8 mm
# Gyro Hole 3 MM - distance 20 mm,len=25 width 15 mm , height 8 mm


plate_t = 1.2
hole_d =  4 #4mm
hole_d_small =  2.8 #4mm


board_x_outer =104 
board_y_outer =72 
board_x_hole_d = 96 #+12 104
board_y_hole_d = 64 #+872

board_x_hole =board_x_hole_d/2
board_y_hole = board_y_hole_d/2

board_x_inner=board_x_hole_d -8
board_y_inner=board_y_hole_d -8

board_ext = (
    cq.Workplane("XY")    
    .rect(16, board_y_outer)
    .extrude(1.5)
    #.translate(( -(96-36+8-2-2-8+2+2),0,0))
)

adap = (
    cq.Workplane("XY")    
    .rect(16, board_y_outer)
    .extrude(1.5)
    #.translate(( -(96-36+8-2-2-8+2+2),0,0))
)
show_object(board_ext2)


board_ext= ( board_ext
            .faces(">Z")
            .workplane()
            .pushPoints([ 
             (0 ,56/2 ),
             (0 ,-56/2 ),
             (0 ,20 ),
             (0 ,-20),   

             
            ])    
    .hole(diameter=hole_d)
    
        
     )



board_ext2= board_ext.translate(( -(96-36+8-2-2-8+2+2),0,0))
show_object(board_ext2)
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

            ])    
    .cboreHole(
        diameter=hole_d,
        cboreDiameter=7.25,
        cboreDepth=2
    )
    
        
     )

motor_lenght =56

#show_object(board)

board = (
    board
    .faces("<Z")          # bottom face
    .workplane()
    .pushPoints([
        #bottom
        (0-8, -board_y_hole),
        (0-8+16, -board_y_hole),
        (0-8+16+16, -board_y_hole), # for stand 

      
       ##// (-board_x_hole+56, +board_y_hole),
        ##//(-board_x_hole+56+16, +board_y_hole),
        (12-16, +board_y_hole), # for stand 
        (12, +board_y_hole),
        (12+16, +board_y_hole),
        (12+16+16, +board_y_hole),


           
    ])
    .cboreHole(
        diameter=hole_d,
        cboreDiameter=7.25,
        cboreDepth=2.5
    )
)


show_object(board)


#i
#board = board.translate( (-21,0,0))

#show_object(board)

board_cut_inner = (
    cq.Workplane("XY")    
    .rect(board_x_inner, board_y_inner)
    .extrude(plate_t)
)


board_cut_inner2 = (
    cq.Workplane("XY")    
    .rect(board_x_inner+20, board_y_inner)
    .extrude(plate_t)
    .translate( (0,0,2))
)
#show_object(board_cut_inner2)




full_y=board_y_outer + 48+16
full_x=12
half_y=full_y/2
half_x=full_x/2




main_plate_y=88
half_main_plate_y = main_plate_y/2

L_plate_y=92
half_L_plate_y=L_plate_y/2

plate_y = full_y     # width (X)
plate_x = full_x      # height (Z)










    




#56.40


#show_object(main_gyro_plate_with_hole2)


#show_object(motor_hole_rect)




motor_con_x=8
motor_con_y=2.5 #thinkness
motor_con_z=24+plate_t #height


motor_plate = (
    cq.Workplane("XY")    
    .rect(motor_con_x, motor_con_y)  
    .extrude(motor_con_z)
)

motor_hole= ( motor_plate
            .faces(">Y")
            .workplane()
            .pushPoints([
            
           
            #Left Row
            ( 0,motor_con_z -4),
            #( -6,0+4+8 ) ,
         
            
            ( 0,motor_con_z-4-16 ),
            #( +6,0+4+8) ,
          
           

            ])

            .hole(hole_d) ) 

#show_object(motor_hole)


motor_hole_y = motor_hole


motor_hole_y_final = motor_hole_y

#show_object(wheel_con_plate_hole_y_final)



#motor_plate1 = motor_hole.translate( (board_y_hole-18+4  ,+board_y_outer/2+1 ,0))
motor_plate2 = motor_hole.translate( (board_y_hole-4  ,-(board_y_outer/2+1) ,0))


#show_object(motor_plate1)
#show_object(motor_plate2)

motor_plate1 = motor_hole.translate( (board_y_hole-4-36  ,+(board_y_outer/2+1) ,0))


#show_object(motor_plate1)
#show_object(motor_plate1)


#motor_plate_couple = motor_plate.mirror(mirrorPlane="XZ", union=False)
motor_plate_all=motor_plate1.union(motor_plate2)

#show_object(wheel_con_plate_hole_couple)
board2cut= board.cut(board_cut_inner)
board2cut= board2cut.cut(board_cut_inner2)

#show_object(board2cut)


#final_chasis_ev2= final_chasis_ev.cut(board_cut_inner).union(conn).union(motor_hole_y_final)
#show_object(final_chasis_ev2)

robo_gyro=(motor_plate_all).union(board2cut)
show_object(robo_gyro)




