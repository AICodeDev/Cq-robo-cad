import cadquery as cq

# ============================================
# CUSTOMIZABLE PARAMETERS
# ============================================

# Wheel dimensions
outer_radius = 35.0          # Outer radius of the wheel (mm)
inner_radius = 12.0          # Inner hub radius (mm)
wheel_thickness = 2.0        # Wall thickness of outer wheel rim (mm) - start with 2mm for testing
wheel_width = 10.0           # Width of the wheel (mm)

# Hub (center cylinder) dimensions
hub_height = 10.0            # Height of inner cylinder (>8mm as required)
hub_radius = 4.0             # Radius of the hub/center cylinder (mm)

# Motor shaft specifications (550 motor typically has 3.17mm or 4mm shaft)
motor_shaft_diameter = 3.2   # Diameter of motor shaft hole (mm)
d_cut_depth = 0.8            # Depth of D-cut flat (mm) - creates flat side for motor shaft

# M2 screw hole (for set screw to secure to motor shaft)
m2_screw_diameter = 2.2      # M2 screw hole diameter (mm) - slightly larger for tap/clearance
m2_screw_offset_height = 5.0 # Height from base where M2 screw hole is located (mm)

# Spokes/supports between hub and rim
number_of_spokes = 8         # Number of spokes in circular pattern

# ============================================
# WHEEL CONSTRUCTION
# ============================================

# Step 1: Create outer wheel rim (hollow cylinder)
wheel = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(outer_radius - wheel_thickness)
    .extrude(wheel_width)
)

show_object(wheel,"disk")


# Step 2: Create solid disk connecting hub to inner radius for spoke cutting
spoke_disk = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(wheel_width)
)

# Step 3: Create triangular cutouts between spokes
# Calculate angle for each spoke section
angle_per_spoke = 360 / number_of_spokes

# Create the cutout pattern by cutting triangular sections
for i in range(number_of_spokes):
    # Calculate the angles for this cutout (between spokes)
    start_angle = i * angle_per_spoke + (angle_per_spoke * 0.15)  # 15% offset for spoke width
    end_angle = (i + 1) * angle_per_spoke - (angle_per_spoke * 0.15)  # 15% offset for spoke width
    
    # Create triangular cutout using arc
    cutout = (
        cq.Workplane("XY")
        .moveTo(0, 0)
        .polarLine(inner_radius * 1.1, start_angle)
        .polarLine(inner_radius * 0.3, end_angle - start_angle)
        .polarLine(inner_radius * 1.1, 180 + start_angle)
        .close()
        .extrude(wheel_width)
    )
    
    spoke_disk = spoke_disk.cut(cutout)

# Step 4: Create the center hub cylinder
hub = (
    cq.Workplane("XY")
    .circle(hub_radius)
    .extrude(hub_height)
)

# Step 5: Create motor shaft hole
shaft_hole = (
    cq.Workplane("XY")
    .circle(motor_shaft_diameter / 2)
    .extrude(hub_height)
)

# Step 6: Create D-cut (flat side) for motor shaft
d_cut = (
    cq.Workplane("YZ")
    .workplane(offset=motor_shaft_diameter / 2 - d_cut_depth)
    .rect(motor_shaft_diameter * 2, hub_height * 2)
    .extrude(motor_shaft_diameter)
)

# Step 7: Create M2 screw hole (perpendicular to shaft)
m2_hole = (
    cq.Workplane("XZ")
    .workplane(offset=0)
    .center(0, m2_screw_offset_height)
    .circle(m2_screw_diameter / 2)
    .extrude(hub_radius * 2)
)

# Step 8: Cut holes from hub
hub = hub.cut(shaft_hole).cut(d_cut).cut(m2_hole)

# Step 9: Combine all components
final_wheel = wheel.union(spoke_disk).union(hub)

# ============================================
# EXPORT
# ============================================

# Show the result
show_object(final_wheel)

# To export as STL for 3D printing, uncomment the line below:
# cq.exporters.export(final_wheel, "robot_wheel.stl")

# ============================================
# PRINTING NOTES FOR CARBON FIBER
# ============================================
# 1. Print with wheel flat on bed (XY plane) for best strength
# 2. Use 100% infill for spokes and hub
# 3. Carbon fiber requires hardened nozzle (steel/ruby)
# 4. Print temperature: typically 240-260°C for CF-filled filaments
# 5. Bed temperature: 80-100°C
# 6. First layer: slow speed (20-30mm/s)
# 7. Consider printing multiple wheels to test fitment
# 8. Increase wall_thickness gradually (2mm → 3mm → 4mm) after testing