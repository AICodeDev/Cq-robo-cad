import cadquery as cq
import math

# Ultrasound Hole 4 MM - distance 16 mm, width 24 mm , height 8 mm
# Gyro Hole 3 MM - distance 20 mm,len=25 width 15 mm , height 8 mm


plate_t = 6
hole_d =  3.9 #4mm
hole_d_small =  2.9 #4mm
cboreDiameter = 7 #SHOULD BE 7
cboreDepth = 2 # 2.5
cboreDepthBig = 2.8 # 2.5

ap_height=12+2

board_x_outer =104 +2
board_y_outer =72 +2
board_x_hole_d = 96 #+12 104
board_y_hole_d = 64 #+872

board_x_hole =board_x_hole_d/2
board_y_hole = board_y_hole_d/2

board_x_inner=board_x_hole_d -8-3
board_y_inner=board_y_hole_d -8-3

castor_board = (
    cq.Workplane("XY")    
    .rect(20, board_y_outer)
    .extrude(2.2)
    #.translate(( -(96-36+8-2-2-8+2+2),0,0))
)

castor_adap = (
    cq.Workplane("XY")    
    .rect(8, 16)
    .extrude(ap_height)
    #.translate(( 0 ,22,0))
)

cadap1=castor_adap.translate(( 0 ,24,0))
cadap2=castor_adap.translate(( 0 ,-24,0))

castor_adap_all=cadap1.union(cadap2)
#$show_object(castor_adap_all)

castor_board = castor_board.union(castor_adap_all)





castor_board= ( castor_board
            .faces(">Z")
            .workplane()
            .pushPoints([ 
               # (0 ,0 ),
                (0 ,4 ),
                (0 ,-4 ),


             (0 ,56/2 ),
             (0 ,-56/2 ),
             (0 ,20 ),
             (0 ,-20),   

             
            ])    
    .hole(diameter=hole_d)
    
        
     )

#show_object(castor_board)


sonic_conn_x = (
    cq.Workplane("XY")    
    .rect(30, 14+4)
    .extrude(2.5)
    .faces(">Z")
            .workplane()
            .pushPoints([ 
               # (0 ,0 ),
                (-7 ,0 ),
          

            

             
            ])    
    .hole(diameter=7.5)


)
sonic_conn_x = (sonic_conn_x.translate((- 25,0,0)) )
#show_object(sonic_conn_x)

sonic_conn_y = (
    cq.Workplane("XY")    
    .rect(10+2, 74)
    .extrude(2.5)
    .faces(">Z")
            .workplane()
            .pushPoints([ 
               # (0 ,0 ),
                (0 ,4 ),
                (0 ,-4 ),


             (0 ,56/2 ),
             (0 ,-56/2 ),
             (0 ,20 ),
             (0 ,-20),   

             
            ])    
    .hole(diameter=hole_d)

)
sonic_conn_y = (sonic_conn_y.translate((- 20,0,0)) )
#show_object(sonic_conn_y)

sonic_conn_xy = sonic_conn_x.union(sonic_conn_y)

sonic_con_x=24+3 #width
sonic_con_y=3 #thinkness
sonic_con_z=8+3 #height
sonic_con_plate_base = (
    cq.Workplane("XY")    
    .rect(sonic_con_x, sonic_con_y)  
    .extrude(sonic_con_z)
    .faces(">Y")
    .workplane()
    .pushPoints([
       ( -8,0+4+2 ),            
      ( +8,0+4 +2),
    ])
    .hole(hole_d)
)
#show_object(sonic_con_plate_base)
sonic_con_plate_hole_y = sonic_con_plate_base.rotate((0, 0, 0), (0, 0, 1), 90) 
sonic_con_plate_hole_y_final = sonic_con_plate_hole_y.translate( (-28-12 ,0,0)) 
sonic_con_plate_hole_x = sonic_con_plate_base.translate( ( -8-6 ,72/2+2.2,0))
sonic_con_plate_hole_x_couple = sonic_con_plate_hole_x.mirror(mirrorPlane="XZ", union=True)
sonic_con_plate_hole_x_triple=sonic_con_plate_hole_x_couple.union(sonic_con_plate_hole_y_final).union(sonic_conn_xy)

#show_object(sonic_con_plate_hole_x_triple)

ghole_d_small =  3 #4mm
gplate_y = 96 + 10     # width (X)
gplate_x = 30      # height (Z)
gap=6
gyro_plate = (
    cq.Workplane("XY")    
    .rect(32, 96 + 8)
    .extrude(3)
    .faces(">Z")
            .workplane()
            .pushPoints([

           ( -(10.1)  ,gplate_y/2-gap),
           (-(10.1)  ,-gplate_y/2+gap),
           ( +(10.1)  ,gplate_y/2-gap),
           (+(10.1)  ,-gplate_y/2+gap),

          
            ])

            .hole(ghole_d_small)    
)
#show_object(gyro_plate)
gplateCut = (
    cq.Workplane("XY")    
    .rect(32, 96 + 8 -(16*2) )
    .extrude(3) )
#show_object(gplateCut)

gyro_plate2 = gyro_plate.cut(gplateCut)
#show_object(gyro_plate2)

gyro_plate3 = gyro_plate2.translate((15+4+2,0,0))
#show_object(gyro_plate3)

castor_board_sonic_gyro=castor_board.union(sonic_con_plate_hole_x_triple).union(gyro_plate3)

castor_board_sonic_gyro= castor_board_sonic_gyro.translate(( -(96-36+8-2-2-8+2+2+3 -0.1),0,0))
show_object(castor_board_sonic_gyro)

battery_board = (
    cq.Workplane("XY")    
    .rect(board_x_outer, board_y_outer)
    .extrude(plate_t)
)

battery_board_16 = (
    cq.Workplane("XY")    
    .rect(board_x_outer, board_y_outer+16)
    .extrude(plate_t*3)
)

battery_board_thick = (
    cq.Workplane("XY")    
    .rect(board_x_outer, board_y_outer)
    .extrude(plate_t*3)
)


motor_board = (
    cq.Workplane("XY")    
    .rect(24+24+16+8+4, board_y_outer+16+6+16)
    .extrude(plate_t)
)
motor_board = motor_board.cut(battery_board)



y1d=board_y_hole +8+2+1+6;
y2d=-board_y_hole -8-2-1-6;


motor_board2= ( motor_board
            .faces("<Z")
            .workplane()
            .pushPoints([ 
 (0 ,y1d),
             (0 ,y2d ),
           #//  (8 ,y1d),
          # //  (8 ,y2d ),
             (16 ,y1d),
             (16 ,y2d ),
          # //  (24 ,y1d),
          # //  (24 ,y2d ),
             (32 ,y1d),
             (32 ,y2d ),

          #  // (-8 ,y1d),
           # // (-8 ,y2d ),
             (-16 ,y1d),
             (-16 ,y2d ),   
          #  // (-24 ,y1d),
          #  // (-24 ,y2d ),
              (-32 ,y1d),
             (-32 ,y2d ),
   

            ])    
    #.hole(hole_d) 
    .cboreHole(
        diameter=hole_d,
        cboreDiameter=cboreDiameter,
        cboreDepth=cboreDepthBig
    )
        
) 

motor_board2 = motor_board2.translate( (48+24,0,0))

nut_board = (
    cq.Workplane("XY")    
    .rect(16, board_y_outer+16+6)
    .extrude(plate_t*3).cut(battery_board_thick)
)




y1d=board_y_hole +8+2+1;
y2d=-board_y_hole -8-2-1;


nut_board_holes= ( nut_board
            .faces("<Z")
            .workplane()
            .pushPoints([ 
             (0 ,y1d),
             (0 ,y2d ),
             
             
   

            ])    
    #.hole(hole_d) 
    .cboreHole(
        diameter=hole_d,
        cboreDiameter=cboreDiameter,
        cboreDepth=cboreDepthBig
    )
        
) 



#extra_nuts = motor_board2.translate( (-48,0,0))         
#show_object(extra_nuts)
    
extra_nuts = nut_board_holes.translate( (-16,0,0))         
    



battery_board= ( battery_board
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
        cboreDiameter=cboreDiameter,
        cboreDepth=cboreDepthBig
    )
    
        
     )

motor_lenght =56

#show_object(battery_board)

battery_board = (
    battery_board
    .faces("<Z")          # bottom face
    .workplane()
    .pushPoints([


  #near the front (front motor)    


        #bottom
         (0, -board_y_hole), # for stand 
        (16 , -board_y_hole),
        (32 , -board_y_hole), 
        #(-8, -board_y_hole), #stand front
        
      
  #near the back (back motor)    

        (0, +board_y_hole), # for stand 
        (16, +board_y_hole),
        #(16+16 , +board_y_hole), #stand back
        (32 , +board_y_hole), #to hole


           
    ])
    .cboreHole(
        diameter=hole_d,
        cboreDiameter=cboreDiameter,
        cboreDepth=cboreDepthBig
    )
)





board_cut_inner = (
    cq.Workplane("XY")    
    .rect(board_x_inner, board_y_inner)
    .extrude(plate_t)
)


board_cut_inner2 = (
    cq.Workplane("XY")    
    .rect(board_x_inner+20, board_y_inner)
    .extrude(plate_t)
    .translate( (20,0,0))
)

board_cut_inner3 = (
    cq.Workplane("XY")    
    .rect(board_x_inner+20, board_y_inner)
    .extrude(plate_t)
    .translate( (20,0,0))
)



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
            
           
            ( 0,motor_con_z -4),
         
            
            ( 0,motor_con_z-4-16 ),
          

            ])

            .hole(hole_d) ) 

motor_hole_y = motor_hole
motor_hole_y_final = motor_hole_y

motor_plate2 = motor_hole.translate( (board_y_hole  ,-(board_y_outer/2) ,0))
motor_plate1 = motor_hole.translate( (board_y_hole-36-4  ,+(board_y_outer/2) ,0))
motor_plate_all=motor_plate1.union(motor_plate2)
board2cut= battery_board.cut(board_cut_inner)
board2cut= board2cut.cut(board_cut_inner2)
board2cut= board2cut.cut(board_cut_inner3)
show_object(board_cut_inner3)

robo_CHASIS_big=(board2cut).union(castor_board_sonic_gyro).union(motor_board2).union(extra_nuts)
robo_CHASIS_big= robo_CHASIS_big.cut(board_cut_inner)


show_object(robo_CHASIS_big)




