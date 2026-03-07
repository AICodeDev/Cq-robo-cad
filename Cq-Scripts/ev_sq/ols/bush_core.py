import cadquery as cq
import math

# ------------------------
# Parameters
# ------------------------
outer_d = 7.0
length = 3
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
show_object(bushing_core)

# ------------------------
# Cut hex hole
# ------------------------
bushing_with_hex = (
    bushing_core
    .faces(">Z")
    .workplane()
    .polygon(6, hex_radius*2)
    .cutThruAll()
)


bushing_with_hex2 = (
    bushing_core
    .faces(">Z")
    .workplane()
    .circle(hex_radius)
    #.cutThruAll()
)

show_object(bushing_with_hex2)


show_object(bushing_with_hex)
