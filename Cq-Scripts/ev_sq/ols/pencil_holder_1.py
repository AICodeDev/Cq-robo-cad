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
# SIMPLE PENCIL HOLDER - RECT CUBE WITH HOLE
# ============================================

def create_simple_pencil_holder(width=16, length=16, height=40, hole_diameter=10):
    
    holder = (
        cq.Workplane("XY")
        .box(length, width, height)
        .faces(">Z")
        .workplane()
        .circle(hole_diameter/2)
        .cutThruAll()
    )
    return holder


# ============================================
# USAGE
# ============================================
height = 20 
# Create pencil holder
pencil_holder = create_simple_pencil_holder(height=height)

# Position at front center, 10mm outside the plate
holder_positioned = pencil_holder.translate((
    -plate_x/2 - 8 + (0.1),  # Front, outside by 10mm
    0,                # Center
    height/2          # Sitting on base
))

# Union with your plate
# final = plateHole2.union(holder_positioned)
# show_object(final, name="with_holder")

show_object(holder_positioned, name="pencil_holder")
