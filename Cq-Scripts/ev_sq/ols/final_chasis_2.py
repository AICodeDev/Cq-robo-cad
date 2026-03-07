import cadquery as cq
import sys
# Plate size
plate_x = 120
plate_y = 88
thickness = 3
cell=8
cell2=cell+1


# Hole specs
hole_dia = 4
hole_dia_final = 3.75
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


oversize= (    
    plateCut
    .faces(">Z")
    .workplaneFromTagged("plateBase")
    .center(cell *6.5 , -cell *2 )
    .rect(cell*2,cell*1.5)
    .extrude(castor_extrude)
)

oversize2= (    
    oversize
    .workplaneFromTagged("plateBase")
    #.faces(">Z")    
    .center(cell *6.5 , +cell *2 )
    .rect(cell*2,cell*1.5)
    .extrude(castor_extrude)  
)


oversize3= (    
    oversize2
    #.faces(">Z")
    .workplaneFromTagged("plateBase")
    .center(-length/2 + (cell*4) , width/2 - cell )
    .rect(cell*8,cell*2)
    .extrude(motor_extrude)
)



oversize4= (    
    oversize3
    .faces(">Z")
    .workplaneFromTagged("plateBase")
    .center(-length/2 + (cell*4) , - (width/2 - cell) )
    .rect(cell*8,cell*2)
    .extrude(motor_extrude)
   
)




plateHole = (
    oversize4
    .faces("<Z")  # Select bottom face
    .workplane(centerOption="CenterOfBoundBox")
    .rarray(spacing, spacing, x_count, y_count)
    .hole(hole_dia)
)
show_object(plateHole, name="step4_final_with_holes")

# Step 1: Create the profile: rectangle with semicircle on one side
holder_profile = (cq.Workplane("XY")
           .moveTo(0, -rect_height/2)  # Start at bottom center
           .lineTo(rect_width/2, -rect_height/2)   # Bottom right
           .lineTo(rect_width/2, rect_height/2)    # Right side up
           .threePointArc((0, rect_height/2 + semicircle_radius), 
                         (-rect_width/2, rect_height/2))  # Semicircle at top
           .lineTo(-rect_width/2, -rect_height/2)  # Left side down
           .close()          # Close the shape
           .extrude(base_extrusion))      # Extrude by 4mm

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
    (plate_x/2 )+cell -0.2 ,  # Front, outside by 10mm
    0,                     # Center
    0               # Sitting on base
))
show_object(holder_positioned)



all = plateHole.union(holder_positioned)
show_object(all, name="all")

"""




# STEP 3: Increase thickness of front-left section
print("Increasing front-left section thickness...")
plateT = modify_grid_block_thickness(
    plateCut, 
    grid_x=0, 
    grid_y=3, 
    cells_x=2,
    cells_y=5, 
    factor=2.5,
    plate_x=plate_x,
    plate_y=plate_y,
    cell=8,
    base_thickness=base_thickness
)
#show_object(plateT, name="step3_thick_section", options={"alpha": 0.7})

# STEP 4: Add holes - NOW WITH FRESH WORKPLANE FROM SCRATCH
print("Adding holes...")

# Get the bounding box to verify centering
bb = plateT.val().BoundingBox()
print(f"Bounding box center: X={((bb.xmin + bb.xmax)/2):.2f}, Y={((bb.ymin + bb.ymax)/2):.2f}")

# Create holes using a FRESH workplane selection




# ============================================
# PENCIL HOLDER WITH CORNER WEIGHT REDUCTION HOLES
# ============================================

def create_simple_pencil_holder(width=16, length=16, height=40, hole_diameter=10, corner_hole_diameter=4):
    
    # Create rect cube and cut center hole through it
    holder = (
        cq.Workplane("XY")
        .box(length, width, height)
        .faces(">Z")
        .workplane()
        .circle(hole_diameter/2)
        .cutThruAll()
    )
    
    # Add 4 corner holes for weight reduction
    corner_offset = length/3  # Distance from center to corner holes
    holder = (
        holder
        .faces(">Z")
        .workplane()
        .pushPoints([
            (-corner_offset, -corner_offset),  # Bottom-left
            (corner_offset, -corner_offset),   # Bottom-right
            (-corner_offset, corner_offset),   # Top-left
            (corner_offset, corner_offset)     # Top-right
        ])
        .circle(corner_hole_diameter/2)
        .cutThruAll()
    )
    
    return holder


# ============================================
# USAGE
# ============================================



pencil_holder = create_simple_pencil_holder(
    width=12,
    length=12,
    height=height,
    hole_diameter=7,
    corner_hole_diameter=2.5  # 4mm corner holes
)

pencil_holder_connector = create_simple_pencil_holder(
    width=12,
    length=12,
    height=base_thickness,
    hole_diameter=4,
    corner_hole_diameter=2  # 4mm corner holes
)

# Position at front center, 10mm outside the plate
holder_positioned = pencil_holder.translate((
    -plate_x/2 - 6 + 0.1 -10 ,  # Front, outside by 10mm
    0,                     # Center
    height/2               # Sitting on base
))

holder_con_positioned = pencil_holder_connector.translate((
    -plate_x/2 - 6 + 0.1  ,  # Front, outside by 10mm
    0,                     # Center
    4               # Sitting on base
))
show_object(holder_con_positioned, name="pencil_holder_with_corners_con")

# Show result
show_object(holder_positioned, name="pencil_holder_with_corners")

def create_motor_plate(length=24, width=16, thickness=4, hole_diameter=3.2, 
                       hole_spacing=8, x_count=4, y_count=4):
    
    plate = (
        cq.Workplane("YZ")
        .box(thickness, length, length)
    )
    
    # Add holes using rarray
    plate = (
        plate
        .faces(">Y")
        .workplane(centerOption="CenterOfBoundBox")
        .rarray(hole_spacing, hole_spacing, x_count, y_count)
        .hole(hole_diameter, thickness)
    )
    
    return plate


# Create LEFT motor plate (facing RIGHT/inward)
motor_plate_left = create_motor_plate(
    length=32,
    width=32,
    thickness=2,
    hole_diameter=3.2,
    hole_spacing=3.2*1.5,
    x_count=8,
    y_count=8
)

# Create RIGHT motor plate (facing LEFT/inward - mirrored)
motor_plate_right = create_motor_plate(
    length=32,
    width=32,
    thickness=2,
    hole_diameter=3.2,
    hole_spacing=3.2*1.5,
    x_count=8,
    y_count=8
)

# Position LEFT motor plate (facing inward to the right)
motor_left_positioned = motor_plate_left.translate((
    plate_x/2 -16,                      # Center in X
    -plate_y/2 -2 + 0.1 +1,        # Left side, 2mm from edge
    16+0.1                    # Height above base
))

# Position RIGHT motor plate (facing inward to the left - mirrored)
# Rotate 180 degrees so it faces the left plate
motor_right_positioned = motor_plate_right.rotate((0, 0, 0), (0, 0, 1), 180).translate((
    plate_x/2-16,                      # Center in X
    plate_y/2  +2 -1- 0.1,         # Right side, 2mm from edge
    16+0.1                     # Height above base
))

# Show motor plates
#show_object(motor_left_positioned, name="motor_plate_left")
#show_object(motor_right_positioned, name="motor_plate_right")


final = plateHole.union(holder_positioned).union(holder_con_positioned).union(motor_left_positioned).union(motor_right_positioned)

show_object(final, name="final")
"""