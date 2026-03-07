import cadquery as cq

# Plate size
plate_x = 120
plate_y = 88
thickness = 8

# Hole specs
hole_dia = 4
padding = 2
spacing = hole_dia + padding + padding   # 6 mm

x_count = 15
y_count = 11

cut_length = 40
cut_width = 20
cut_depth = 3

import cadquery as cq

# Dimensions (mm)
length = 120
width = 88
base_thickness = 8


# Base plate
plate = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(base_thickness)
)

show_object(plate)

plate2 = (
    plate
    .faces(">Z")
    .workplane()
    .rect(84, 52)
    .cutThruAll()
)
show_object(plate2)





plate3 = (
    plate2
    .faces(">Z")
    .workplane()
    .rarray(spacing, spacing, x_count, y_count)
    .hole(hole_dia)
)

show_object(plate3)