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
bush_thinkness = 2

bush_inner_d= outer_d +bush_clear
bush_outer_d= bush_inner_d + bush_thinkness


length = 10
hex_af = 5.0  # across flats

# Convert AF to circumradius for CadQuery polygon
hex_radius = hex_af / math.sqrt(3)
#hex_radius = 2.886 
# ------------------------
# Create cylinder
# ------------------------
bushing_core = (
    cq.Workplane("XY")
    .circle(outer_d / 2)
    .extrude(length)
)


main_bushing_core = (
    cq.Workplane("XY")
    .circle(bush_outer_d / 2)
    .extrude(length)
)

show_object(main_bushing_core)

main_bushing_with_hole = (
    main_bushing_core
    .faces(">Z")
    .workplane()
    .circle(bush_inner_d/2)
    .cutThruAll()
)
show_object(main_bushing_with_hole)



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

