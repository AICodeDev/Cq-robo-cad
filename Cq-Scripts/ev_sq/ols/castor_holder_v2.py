import cadquery as cq
import math

"""
Axle - 5mm innner
hole 8 mm
holder - 10 mm to 12 mm, block at 11 MM

10 mm 

Motor Base - 56 = 16*3.5 X 24
8,8,8

12 mm distave from hole

4, 16
36+20 verticle hole



"""




# ------------------------
# Parameters
# ------------------------
test_thick_less = 0
test_height_less = 0.5



outer_d = 5
bush_clear = 1.5
bush_thinkness = 3+2+0.5

bush_inner_d= outer_d +bush_clear
bush_outer_d= bush_inner_d + bush_thinkness

print("bush",bush_outer_d)

stoper_dia =12
shaft_dia =stoper_dia -2
max_height = 18

clear = 1.2

hole_thick = 2  #diameter factor

inner_hole_dia = shaft_dia +clear
outer_hole_dia  = inner_hole_dia + (hole_thick*2)


length = max_height * 2/3 #12
hole_len = max_height * 2/3 
extra_len = 0

hex_af = 5.0  # across flats

# Convert AF to circumradius for CadQuery polygon
# hex_radius = hex_af / math.sqrt(3)


extra_con =3



#show_object(main_bushing_with_hole)


connector_w = 8

plate_w = 24     # width (X)
plate_h = 24      # height (Z)
plate_t = 3 - test_thick_less       # thickness (Y)

plate_len=plate_w

connector_h = 24
connector_t = plate_t



hole_d = 4
hole_spacing = 16



plate = (
    cq.Workplane("XY")
    
    .rect(50, 8)
    .extrude(8+6+6)
    #.translate((plate_w / 2 + connector_w*1.5 + extra_con , 0, 0))
)
show_object(plate)

plate2 = (
    cq.Workplane("XY")
    
    .rect(30, 8)
    .extrude(8+6)
    .translate((0 , 0, 6))
)
show_object(plate2)


plateY = (
    cq.Workplane("XY")    
    .rect(8, 8 + 16 + 16 )
    .extrude(1.2)
    #.translate((0 , 0, 6))
)
show_object(plateY)


platey_with_holes = (
    plateY
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .pushPoints([

       (0,0),

                   
        
         (0   , 16), #R

           (0   , -16), #R



        
    ])
    .hole(4)
)
show_object(platey_with_holes)


#plate_t

#show_object(main_bushing_with_hole2)
#show_object(plate)

plate_w = 50
hole_d =4

plate_with_holes1 = (
    plate
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .pushPoints([

       (0,0),

                   
        
         (20   , 0), #R

           (-20   , 0), #R



        
    ])
    .hole(4)
)
show_object(plate_with_holes1)

castor_holder= plate_with_holes1.cut(plate2)

show_object(castor_holder)

castor_holder2 = castor_holder.union(platey_with_holes)

show_object(castor_holder2)


#final_wheel_holder = main_bushing_with_hole.union(plate_with_holes1)
#show_object(final_wheel_holder)
"""

tight_bushing_with_hex = (
    bushing_core
    .faces(">Z")
    .workplane()
    .polygon(6, hex_radius*2)
    .cutThruAll()
)
"""


"""
c = (
    bushing_core
    .faces(">Z")
    .workplane()
    .circle(hex_radius)
    #.cutThruAll()
)

show_object(c)
"""

#show_object(tight_bushing_with_hex)

