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
    """
    Rectangular pencil holder with center hole and 4 corner holes for weight reduction.
    
    Parameters:
    -----------
    width : float - width of cube
    length : float - length of cube  
    height : float - height of cube
    hole_diameter : float - diameter of center pencil hole
    corner_hole_diameter : float - diameter of corner weight reduction holes
    """
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

# Position at front center, 10mm outside the plate
holder_positioned = pencil_holder.translate((
    -plate_x/2 - 6 + 0.1,  # Front, outside by 10mm
    0,                     # Center
    height/2               # Sitting on base
))

# Show result
show_object(holder_positioned, name="pencil_holder_with_corners")

# Union with your plate (uncomment to use)
# final = plateHole2.union(holder_positioned)
# show_object(final, name="complete_assembly")
