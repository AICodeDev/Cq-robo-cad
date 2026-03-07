import cadquery as cq
import sys

# Plate size
plate_x = 120
plate_y = 88
thickness = 9
cell = 8
cell2 = cell + 1

# Hole specs
hole_dia = 4
hole_dia_final = 3.8
padding = 2
spacing = 8  # 4mm hole + 2mm + 2mm = 8mm spacing

x_count = 15
y_count = 11



# Dimensions (mm)
length = plate_x
width = plate_y
base_thickness = thickness
factor_motor = 8.5 / 3.5
factor_castor = 15 / 3.5

##########
# Define parameters for pencil holder
rect_width = 18
rect_height = 36
semicircle_radius = 5
base_extrusion = 2.5
hole_radius = 5
cylinder_radius = hole_radius + 2.5
cylinder_height = 16


# Calculate positions
semicircle_center_y = rect_height / 2-4
castor_extrude = 7.5
motor_extrude = 4.5
extra_cut=16


# STEP 1: Create base plate
print("Creating base plate...")
plate = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(base_thickness)
)

plate.faces(">Z").workplane().tag("plateBase")

# STEP 2: Add cutouts in left and right halves
print("Adding center cutouts...")

# Calculate center positions for each half
# Plate is centered at origin, so extends from -60 to +60 in X
left_half_center_x = -30   # Center of left half (30mm left of origin)
right_half_center_x = 30   # Center of right half (30mm right of origin)

# Cut dimensions for right side (base cut)
cut_length_right = 42
cut_width_right = 52

#center
plateCut = (
    plate.workplaneFromTagged("plateBase")
    
    .rect(20, cut_width_right+extra_cut)
    .cutThruAll()
)

#left
# Make cut in right half
plateCut = (
    plateCut.workplaneFromTagged("plateBase")
    .center(-right_half_center_x, 0)  # Move to right half center
    .rect(cut_length_right, cut_width_right+extra_cut)
    .cutThruAll()
)
#right
plateCut = (
    plateCut.workplaneFromTagged("plateBase")
    .center(right_half_center_x, 0)  # Move to right half center
    .rect(cut_length_right, cut_width_right)
    .cutThruAll()
)

#left of right

plateCut = (
    plateCut.workplaneFromTagged("plateBase")
    .center(right_half_center_x-12, 0)  # Move to right half center
    .rect(cut_length_right/2, cut_width_right+extra_cut)
    .cutThruAll()
)
show_object(plateCut)

caster1= (    
    plateCut    
    .workplaneFromTagged("plateBase")
    .center(cell *7 , -cell *2 )
    .rect(cell,cell*1.5)
    .extrude(castor_extrude)
)
show_object(caster1)



caster2= (    
    caster1
    .workplaneFromTagged("plateBase")
    #.faces(">Z")    
    .center(cell *7 , +cell *2 )
    .rect(cell,cell*1.5)
    .extrude(castor_extrude)  
)
show_object(caster2)


plateHole = (
    caster2
    .faces("<Z")  # Select bottom face
    .workplane(centerOption="CenterOfBoundBox")
    .rarray(spacing, spacing, x_count, y_count)
    .hole(hole_dia)
)
show_object(plateHole, name="step4_final_with_holes")


"""
# Make cut in left half
plateCut = (
    plateCut
    .faces(">Z")
    .workplane()
    .center(left_half_center_x, 0)  # Move to left half center
    .rect(cut_length_left, cut_width_left)
    .cutThruAll()
)
"""

# Step 1: Create the profile: rectangle with semicircle on one side
holder_profile = (cq.Workplane("XY")
           .moveTo(0, -rect_height/2)  # Start at bottom center
           .lineTo(rect_width/2, -rect_height/2)   # Bottom right
           .lineTo(rect_width/2, rect_height/2)    # Right side up
           .threePointArc((0, rect_height/2 + semicircle_radius), 
                         (-rect_width/2, rect_height/2))  # Semicircle at top
           .lineTo(-rect_width/2, -rect_height/2)  # Left side down
           .close()          # Close the shape
           .extrude(5))      # Extrude by 4mm

# Step 2: Select the center of the semicircle, draw cylinder and create hole
pencile_holder = (holder_profile
          .faces(">Z")      # Select top face
          .workplane()
          .center(0, semicircle_center_y)    # Move to center of semicircle
          .circle(cylinder_radius)        # Draw circle for cylinder
          .extrude(cylinder_height)      # Extrude cylinder upward
          .faces(">Z")      # Select top face of cylinder
          .workplane()
          .circle(hole_radius)        # Draw hole
          .cutThruAll())    # Cut hole through everything

# Display the result
#show_object(result)
# Create pencil holder
height = 20  # Define height variable
holder_positioned = pencile_holder .rotate((0,0,0), (0,0,1), -90) .translate((
    (plate_x/2 )+cell +9 ,  # Front, outside by 10mm
    0,                     # Center
    0               # Sitting on base
))
show_object(holder_positioned)



all = plateHole.union(holder_positioned)
show_object(all, name="all")



