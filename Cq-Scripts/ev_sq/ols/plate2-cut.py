import cadquery as cq
import sys
# Plate size
plate_x = 120
plate_y = 88
thickness = 9
cell=8
cell2=cell+1


# Hole specs
hole_dia = 4
hole_dia_final = 3.8
padding = 2
spacing = 8  # 4mm hole + 2mm + 2mm = 8mm spacing

x_count = 15
y_count = 11

cut_length = 84+2
cut_width = 52+2

# Dimensions (mm)
length = 120
width = 88
base_thickness = 3
factor_motor = 8.5 /3.5
factor_castor = 15 /3.5

##########
# Define parameters for pencil holder
rect_width = 10
rect_height = 20
semicircle_radius = 5
base_extrusion = 2.5
cylinder_radius = 4.5
cylinder_height = 12
hole_radius = 3.5

# Calculate positions
semicircle_center_y = rect_height / 2
castor_extrude =7.5
motor_extrude =4.5


plate = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(base_thickness)
)
#show_object(plate, name="step1_base_plate", options={"alpha": 0.3})

# STEP 2: Add center cutout
print("Adding center cutout...")
plateCut = (
    plate
    .faces(">Z")
    .workplane()
    .rect(cut_length, cut_width)
    .cutThruAll()
)

plateCut.faces(">Z").workplane().tag("plateBase")
how_object(plate_cut)