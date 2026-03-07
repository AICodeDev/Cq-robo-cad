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


def modify_grid_block_thickness(
    plate,
    grid_x,
    grid_y,
    cells_x=1,
    cells_y=1,
    plate_x=120,
    plate_y=88,
    cell=8,
    base_thickness=8,
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
        result = plate.union(extension)
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
        result = plate.cut(cut_box)
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
show_object(plate, name="step1_base_plate", options={"alpha": 0.3})

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
show_object(plateT, name="step3_thick_section", options={"alpha": 0.7})

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

# Alternative method - if above doesn't work, use this:
# Start completely fresh from the solid
plateHole2 = plateT
hole_positions = []

# Calculate all hole positions manually
start_x = -plate_x/2 + padding + hole_dia/2
start_y = -plate_y/2 + padding + hole_dia/2

for i in range(x_count):
    for j in range(y_count):
        x = start_x + i * spacing
        y = start_y + j * spacing
        hole_positions.append((x, y))

# Drill holes one by one from a fresh workplane
for pos in hole_positions:
    plateHole2 = (
        plateHole2
        .faces("<Z")
        .workplane(centerOption="CenterOfBoundBox")
        .center(pos[0], pos[1])
        .hole(hole_dia)
    )

show_object(plateHole2, name="alternative_with_manual_holes")


# ============================================
# ADD-ON CODE - L BRACKETS AND PENCIL HOLDER
# Place this AFTER your existing hole drilling code
# ============================================

def create_l_bracket(length=20, height=16, thickness=4):
    """
    Create L-shaped bracket.
    
    Parameters:
    -----------
    length : float - horizontal length of bracket
    height : float - vertical height of bracket wall
    thickness : float - thickness of bracket material
    """
    # Create horizontal base
    base = (
        cq.Workplane("XY")
        .box(length, thickness, thickness)
    )
    
    # Create vertical wall
    wall = (
        cq.Workplane("XY")
        .workplane(offset=thickness/2)
        .box(length, thickness, height)
        .translate((0, thickness/2, height/2))
    )
    
    # Combine base and wall
    bracket = base.union(wall)
    
    # Add mounting holes with threads (use 3.3mm for M4 self-tapping)
    # Holes in horizontal base for chassis attachment
    bracket = (
        bracket
        .faces("<Z")
        .workplane(centerOption="CenterOfBoundBox")
        .pushPoints([(-length/3, 0), (length/3, 0)])
        .hole(3.3, thickness)  # Threaded holes for M4 screws
    )
    
    # Holes in vertical wall for motor/device attachment
    bracket = (
        bracket
        .faces(">Y")
        .workplane(centerOption="CenterOfBoundBox")
        .pushPoints([(-length/3, height/2), (length/3, height/2)])
        .hole(3.3, thickness)  # Threaded holes for M4 screws
    )
    
    return bracket


def create_pencil_holder(inner_diameter=10, wall_thickness=3, height=50, 
                        base_size=20, base_thickness=8, extension=10):
    """
    Create pencil/dowel holder with mounting base.
    
    Parameters:
    -----------
    inner_diameter : float - inner diameter for pencil/dowel
    wall_thickness : float - wall thickness of cylinder
    height : float - height of holder cylinder
    base_size : float - size of square mounting base
    base_thickness : float - thickness of mounting base
    extension : float - how far to extend outside base plate
    """
    # Create mounting base (extends outward)
    base = (
        cq.Workplane("XY")
        .box(base_size + extension, base_size, base_thickness)
        .translate((extension/2, -20, 5))
    )
    
    # Create cylinder holder with through-hole
    outer_diameter = inner_diameter + 2 * wall_thickness
    
    holder = (
        cq.Workplane("XY")
        .workplane(offset=base_thickness/2)
        .circle(outer_diameter/2)
        .extrude(height)
        .faces(">Z")
        .workplane()
        .circle(inner_diameter/2)
        .cutThruAll()  # Complete through-hole for pencil
        .translate((extension, 0, 0))
    )
    
    # Combine base and holder
    result = base.union(holder)
    
    # Add mounting holes with threads
    result = (
        result
        .faces("<Z")
        .workplane(centerOption="CenterOfBoundBox")
        .pushPoints([(extension/4, 0), (extension/4 + 10, 0)])
        .hole(3.3, base_thickness)  # Threaded holes for M4 screws
    )
    
    return result


# ============================================
# ADD L-BRACKETS TO BACK (MIRRORED PAIR)
# ============================================

# Create one bracket
l_bracket = create_l_bracket(length=20, height=16, thickness=4)

# Position back-left bracket
bracket_left = (
    l_bracket
    .rotate((0, 0, 0), (0, 0, 1), 0)  # No rotation needed
    .translate((
        plate_x/2 - 10,          # Near back edge
        -plate_y/2 - 3,         # Left side
        base_thickness/2         # Sitting on base
    ))
)

# Position back-right bracket (mirror of left)
bracket_right = (
    l_bracket
    .rotate((0, 0, 0), (0, 0, 1), 0)
    .translate((
        plate_x/2 - 10,          # Near back edge
        plate_y/2,          # Right side (mirrored)
        base_thickness/2         # Sitting on base
    ))
)

# Union brackets with the plate
plateWithBrackets = plateHole2.union(bracket_left).union(bracket_right)
show_object(plateWithBrackets, name="with_brackets")


# ============================================
# ADD PENCIL HOLDER TO FRONT
# ============================================

# Create pencil holder
pencil_holder = create_pencil_holder(
    inner_diameter=10,
    wall_thickness=3,
    height=30,
    base_size=20,
    base_thickness=base_thickness,
    extension=15  # Extends 10mm outside base plate
)

# Position at front center (extending outward)
holder_positioned = (
    pencil_holder
    .rotate((0, 0, 0), (0, 0, 1), -90)  # Rotate to face outward
    .translate((
        -plate_x/2 ,              # Front edge
        15,                       # Center
        base_thickness/2         # Sitting on base
    ))
)

# Union holder with the assembly
final_assembly = plateWithBrackets.union(holder_positioned)
show_object(final_assembly, name="FINAL_COMPLETE_ASSEMBLY", options={"color": "steelblue"})


# ============================================
# OPTIONAL: Show individual components
# ============================================

# Uncomment to see individual parts
# show_object(create_l_bracket(), name="bracket_sample", options={"alpha": 0.7})
# show_object(create_pencil_holder(), name="holder_sample", options={"alpha": 0.7})

print("\n✅ L-Brackets and Pencil Holder Added!")
print("- Back brackets: 2 mirrored at back edges")
print("- Pencil holder: Front center, extends 10mm outside")
print("- All holes: 3.3mm for M4 self-tapping threads")


# ============================================
# EXPORT FINAL MODEL
# ============================================

# Uncomment to export
# cq.exporters.export(final_assembly, "complete_chassis.stl")
# cq.exporters.export(final_assembly, "complete_chassis.step")



print("\nDone! Check both versions.")
print(f"Spacing: {spacing}mm")
print(f"Grid: {x_count} x {y_count} holes")
print(f"Total holes: {len(hole_positions)}")