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
outer_d = 7.0
bush_clear = 1.5
bush_thinkness = 3

bush_inner_d= outer_d +bush_clear
bush_outer_d= bush_inner_d + bush_thinkness


length = 24
hex_af = 5.0  # across flats

# Convert AF to circumradius for CadQuery polygon
# hex_radius = hex_af / math.sqrt(3)

main_bushing_core = (
    cq.Workplane("XY")
    .circle(bush_outer_d / 2)
    .extrude(length)
)

connector = (
    cq.Workplane("XY")    
    .rect(12, 12)
    .extrude(3)
    .translate( (6, 0, 0))
)
show_object(connector)

main_bushing_core = main_bushing_core.union(connector)

main_bushing_with_hole = (
    main_bushing_core
    .faces(">Z")
    .workplane()
    .circle(bush_inner_d/2)
    .cutThruAll()
)


show_object(main_bushing_with_hole)


connector_w = 8

plate_w = 56     # width (X)
plate_h = 24      # height (Z)
plate_t = 3       # thickness (Y)

plate_len=plate_w

connector_h = 24
connector_t = plate_t



hole_d = 4
hole_spacing = 16

"""
plate = (
    cq.Workplane("XY")
    .rect(plate_w, plate_t/2)
    .extrude(plate_h)
    .translate((plate_w / 2, bush_outer_d/2 - plate_t/4, 0))
)
"""

plate = (
    cq.Workplane("XY")
    
    .rect(plate_w, 24)
    .extrude(plate_t)
    .translate((plate_w / 2 + connector_w*1.5, 0, 0))
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

        ( plate_w / 2 -hole_d - hole_spacing/2,  hole_spacing/2), #12
        ( plate_w / 2 -hole_d - hole_spacing/2 , -hole_spacing/2),

        ( plate_w / 2 -hole_d - hole_spacing,  hole_spacing/2), # 20
        ( plate_w / 2 -hole_d - hole_spacing , -hole_spacing/2),
        
        ( plate_w / 2 -hole_d - hole_spacing *  1.5,  hole_spacing/2), #28
        ( plate_w / 2 -hole_d - hole_spacing *  1.5,  -hole_spacing/2),



        
    ])
    .hole(hole_d)
)
show_object(plate_with_holes1)



plate_with_holes2 = (
    plate_with_holes1
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .pushPoints([
        #//(plate_w / 2 -hole_d ,  0),
        #(plate_w / 2 -hole_d*2 ,  0),
        (-plate_w / 2 +hole_d*3 ,  0),


        
    ])
    .hole(hole_d*2.25)
)
show_object(plate_with_holes2)

final = main_bushing_with_hole.union(plate_with_holes2)
show_object(final)
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

