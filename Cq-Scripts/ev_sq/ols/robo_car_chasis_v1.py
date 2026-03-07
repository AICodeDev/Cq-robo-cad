import cadquery as cq
import sys

# Plate size
plate_x = 120 -16
plate_y = 88 - 16
thickness = 8
cell = 8
cell2 = cell + 1

# Hole specs
hole_dia = 4
hole_dia_final = 3.8
padding = 2
spacing = 8  # 4mm hole + 2mm + 2mm = 8mm spacing

x_count = 15
y_count = 11

extrude_wall =3



# Dimensions (mm)
length = plate_x
width = plate_y
base_thickness = thickness
factor_motor = 8.5 / 3.5
factor_castor = 15 / 3.5

##########
# Define parameters for pencil holder
prect_width = 16-2-2
prect_height = 24
phole_radius = 3.7
semicircle_radius = phole_radius
base_extrusion = 2.5
cylinder_radius = phole_radius + 2.5
cylinder_height = 16-2


# Calculate positions
semicircle_center_y = prect_height / 2-4
castor_extrude = 8
motor_extrude = 4.5
extra_cut=16


# STEP 1: Create base plate
print("Creating base plate...")
plate = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(base_thickness)
)
show_object(plate, name="base_plate")
plate.faces(">Z").workplane().tag("plateBase")

plate_inner = (
    cq.Workplane("XY")
    .rect(length-8-8, width-8-8)
    .extrude(base_thickness)
)
show_object(plate_inner, name="plate_inner")

plateCut = plate.cut(plate_inner)

show_object(plateCut, name="plate_after_cut")

plateHole = (
    plateCut
    .faces("<Z")  # Select bottom face
    .workplane(centerOption="CenterOfBoundBox")
    .pushPoints([
       (0,0),

        (length/2-4, width/2-4),
        (length/2-4, -width/2+4), 

        (-length/2+4, +width/2-4),       
        (-length/2+4, -width/2+4),  
        

    
        (length/2-4-16, width/2-4),
        
    ])
    

    .hole(hole_dia)
)

show_object(plateHole, name="plateHole")

