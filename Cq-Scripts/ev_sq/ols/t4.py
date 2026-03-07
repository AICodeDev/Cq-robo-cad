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

cut_length = 84
cut_width = 52
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

plateCut = (
    plate
    .faces(">Z")
    .workplane()
    .rect(84, 52)
    .cutThruAll()
)
show_object(plateCut)





plateHole = (
    plateCut
    .faces(">Z")
    .workplane()
    .rarray(spacing, spacing, x_count, y_count)
    .hole(hole_dia)
)

show_object(plateHole)