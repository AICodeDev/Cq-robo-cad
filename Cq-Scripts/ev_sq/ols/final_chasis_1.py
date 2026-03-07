import cadquery as cq
import sys
# Plate size
plate_x = 120
plate_y = 88
thickness = 4
cell=8
cell2=cell+1


# Hole specs
hole_dia = 4
hole_dia_final = 3.6
padding = 2
spacing = 8  # 4mm hole + 2mm + 2mm = 8mm spacing

x_count = 15
y_count = 11

cut_length = 84+2
cut_width = 52+2

# Dimensions (mm)
length = 120
width = 88
base_thickness = 3.5
factor_motor = 8.5 /3.5
factor_castor = 15 /3.5

##########
# Define parameters for pencil holder
rect_width = 10
rect_height = 15
semicircle_radius = rect_width/2
base_extrusion = 2.5
cylinder_radius = rect_width/2
cylinder_height = 10
hole_radius = 3.5

# Calculate positions
semicircle_center_y = rect_height / 2
castor_extrude =10
motor_extrude =5





def modify_grid_block_thickness(
    plate,
    grid_x,
    grid_y,
    cells_x=1,
    cells_y=1,
    plate_x=120,
    plate_y=88,
    cell=8,
    base_thickness=4,
    factor=1.0
):
    """
    Grid origin: TOP-LEFT corner of plate
    grid_x=0, grid_y=0 -> top-left cell
    
    FIXED: Always returns a result that maintains the original coordinate system
    """

    delta = base_thickness * (factor - 1.0)

    block_w = cells_x * cell
    block_h = cells_y * cell

    # Convert top-left grid to CadQuery center coordinates
    x_center = (
        -plate_x / 2
        + grid_x * cell
        + block_w / 2
    )

    y_center = (
        plate_y / 2
        - grid_y * cell
        - block_h / 2
    )

    if delta > 0:
        # EXTRUDE: Create a box and union it
        extension = (
            cq.Workplane("XY")
            
            .workplane(offset=base_thickness)  # Start at top of base
            .center(x_center, y_center)
            .rect(block_w, block_h)
            .extrude(delta)
        )
        result = plate.workplaneFromTagged("plateBase").union(extension)
        return result
        
    elif delta < 0:
        # CUT: Create a box and subtract it
        cut_box = (
            cq.Workplane("XY")
            .workplane(offset=base_thickness + delta)  # Start from desired height
            .center(x_center, y_center)
            .rect(block_w, block_h)
            .extrude(abs(delta))
        )
        result = plate.workplaneFromTagged("plateBase").cut(cut_box)
        return result
        
    else:
        return plate


# ============================================
# BUILD STEP BY STEP
# ============================================

# STEP 1: Base plate
print("Creating base plate...")
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
show_object(plateCut, name="step2_with_cutout11", options={"alpha": 0.5})

plateCut = plateCut.tag("plateBase")

show_object(plateCut, name="step2_with_cutout211", options={"alpha": 0.5})
print(plateCut)

oversize= (    
    plateCut
    .faces(">Z")
    .workplaneFromTagged("plateBase")
    .center(cell *6.5 , -cell *2 )
    .rect(cell*2,cell*1.5)
    .extrude(castor_extrude)
   

    
)




show_object(oversize, name="oversize", options={"alpha": 0.5})


oversize= (    
    oversize
    .workplaneFromTagged("plateBase")
    .faces(">Z")    
    .center(cell *6.5 , +cell *2 )
    .rect(cell*2,cell*1.5)
    .extrude(castor_extrude)  
)
show_object(oversize, name="oversize2", options={"alpha": 0.5})

oversize= (    
    oversize
    .faces(">Z")
    .workplaneFromTagged("plateBase")
    .center(-length/2 + (cell*4) , width/2 - cell )
    .rect(cell*8,cell*2)
    .extrude(motor_extrude)
   

    
)

show_object(oversize, name="motor1", options={"alpha": 0.5})

oversize= (    
    oversize
    .faces(">Z")
    .workplaneFromTagged("plateBase")
    .center(-length/2 + (cell*4) , - (width/2 - cell) )
    .rect(cell*8,cell*2)
    .extrude(motor_extrude)
   

    
)

show_object(oversize, name="motor2", options={"alpha": 0.5})

"""
result = (
    cq.Workplane("XY")
    # create and tag the base workplane
    .box(10, 10, 10)
    .faces(">Z")
    .workplane()
    .tag("baseplane")
    # extrude a cylinder
    .center(-3, 0)
    .circle(1)
    .extrude(3)
    # to reselect the base workplane, simply
    .workplaneFromTagged("plateBase")
    # extrude a second cylinder
    .center(3, 0)
    .circle(1)
    .extrude(2)
)
"""







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
plateHole = (
    plateT
    .faces("<Z")  # Select bottom face
    .workplane(centerOption="CenterOfBoundBox")  # Force center at bounding box center
    .rarray(spacing, spacing, x_count, y_count)
    .hole(hole_dia)
)
show_object(plateHole, name="step4_final_with_holes")



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

# Create pencil holder
height = 20  # Define height variable

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