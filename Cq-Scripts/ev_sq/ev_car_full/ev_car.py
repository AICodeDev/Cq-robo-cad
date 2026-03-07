import cadquery as cq
import math


axle_rod = (
    cq.Workplane("XY")    
    .rect(84, 7.2)
    .extrude(7.2).translate((0,0,50))
)
axle_rod=axle_rod.translate((80,0,0))

show_object(axle_rod)


chasis_motor_plae = (
    cq.Workplane("XY")    
    .rect(84-16, 24)
    .extrude(2).translate((0,0,0))
)
chasis_motor_plae=chasis_motor_plae.translate((80,0,0))
show_object(chasis_motor_plae)


hole_base = (
    cq.Workplane("XY")    
    .rect(8, 16)
    .extrude(8)
)
hole_base = (
    hole_base.faces(">Z")
    .workplane()
    .pushPoints([(0, -4), (0, 4)])  # Offset from center: X +/- 1, Z +6 (near top)
    .hole(3.96)                      # Drill 1.0 diameter holes
)
hole_base=hole_base.translate((-5,0,0))
show_object(hole_base)


bush_holder = (
    cq.Workplane("XY")    
    .rect(2, 16)
    .extrude(50+8+2)
)
show_object(bush_holder)

"""

# 1. Create the vertical plate
plate_vertical = (
    cq.Workplane("XY")    
    .rect(2.5, 16)
    .extrude(16)
)

hole_y_pos=4
# 2. Add two holes near the top edge
# We select the front face (">Y"), create a workplane, 
# then push two points near the top (Z=16) and drill holes.
plate_vertical = (
    plate_vertical.faces(">X")
    .workplane(centerOption="CenterOfMass")
    .pushPoints([(-4, hole_y_pos), (4, hole_y_pos)])  # Offset from center: X +/- 1, Z +6 (near top)
    .hole(3.95)                      # Drill 1.0 diameter holes
)


plate_vertical = plate_vertical.translate((32+4+1+1-0.2,4,0))
show_object(plate_vertical)


# ------------------------
# Parameters
# ------------------------
test_thick_less = 0
test_height_less = 0.5



outer_d = 10.8+3
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

main_bushing_core = (
    cq.Workplane("XY")
    .circle(outer_hole_dia / 2)
    .extrude(hole_len  - test_height_less)
)
extra_con =3

connector = (
    cq.Workplane("XY")    
    .rect(12+extra_con, 12+3)
    .extrude(3-test_thick_less)
    .translate( ((12+extra_con)/2, 0, 0))
)
show_object(connector)

main_bushing_core = main_bushing_core.union(connector)
show_object(main_bushing_core)
main_bushing_with_hole = (
    main_bushing_core
    .faces(">Z")
    .workplane()
    .circle(inner_hole_dia/2)
    .cutThruAll()
)


show_object(main_bushing_with_hole)


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
    
    .rect(plate_w, 24)
    .extrude(plate_t)
    .translate((plate_w / 2 + connector_w*1.5 + extra_con , 0, 0))
)
show_object(plate)





#plate_t

main_bushing_with_hole2 = main_bushing_with_hole #.translate((plate_w / 2, bush_outer_d/2 - plate_t/4, 0))

show_object(main_bushing_with_hole2)
#show_object(plate)

plate_with_holes1 = (
    plate
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .pushPoints([

               # (plate_w/2-hole_d,  hole_spacing/2),

        #( plate_w / 2 -hole_d,  hole_spacing/2), #4
        #( plate_w / 2 -hole_d, -hole_spacing/2),

        #toward  main bush
        ( plate_w / 2 -hole_d - hole_spacing,  0/2), # 20
        #//( plate_w / 2 -hole_d - hole_spacing,  hole_spacing/2), # 20
        #//( plate_w / 2 -hole_d - hole_spacing , -hole_spacing/2),

        #middle , middle
        #MM 
        ( plate_w / 2 -hole_d - hole_spacing/2,  0/2), #12
        ( plate_w / 2 -hole_d - hole_spacing/2,  hole_spacing/2), #12
        #( plate_w / 2 -hole_d - hole_spacing/2 , -hole_spacing/2),
        
        
       #//far - middle 
       #  ( plate_w / 2 -hole_d - 0/2,  0/2), #12
        # ( plate_w / 2 -hole_d - 0/2,  hole_spacing/2), #L
        #// ( plate_w / 2 -hole_d - 0/2 , -hole_spacing/2), #R
       



        
    ])
    .hole(hole_d)
)
show_object(plate_with_holes1)





final_wheel_holder = main_bushing_with_hole.union(plate_with_holes1).union(plate_vertical)
show_object(final_wheel_holder)
"""
