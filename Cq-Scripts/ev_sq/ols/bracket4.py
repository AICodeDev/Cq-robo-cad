import cadquery as cq

# Plate size
plate_x = 120
plate_y = 88
thickness = 8

# Hole specs
hole_dia = 4
padding = 2
spacing = 8  # 4mm hole + 2mm + 2mm = 8mm spacing

x_count = 15
y_count = 11

cut_length = 84
cut_width = 52

# Dimensions (mm)
length = 120
width = 88
base_thickness = 8



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
show_object(plate, name="step1_base_plate_pencil", options={"alpha": 0.3})

# STEP 2: Add center cutout
print("Adding center cutout...")
plateCut = (
    plate
    .faces(">Z")
    .workplane()
    .rect(84, 52)
    .cutThruAll()
)
show_object(plateCut, name="step2_with_cutout", options={"alpha": 0.5})


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
    height=height/2,
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
    0               # Sitting on base
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
show_object(motor_left_positioned, name="motor_plate_left")
show_object(motor_right_positioned, name="motor_plate_right")
