import cadquery as cq
from cq_gears import BevelGear

# ------------------------
# Parameters
# ------------------------
motor_shaft_d = 6        # motor shaft diameter
hub_d = 8                # hub cylinder outer diameter
hub_height = 9           # hub height
gear_module = 1.25
teeth_number = 18
cone_angle = 45
face_width = 6
pressure_angle = 20
helix_angle = 0
set_screw_d = 3          # optional radial screw

# ------------------------
# Build Bevel Gear
# ------------------------
gear = BevelGear(
    module=gear_module,
    teeth_number=teeth_number,
    cone_angle=cone_angle,
    face_width=face_width,
    pressure_angle=pressure_angle,
    helix_angle=helix_angle
)

gear_solid = gear.build()

# ------------------------
# Create Hub Cylinder
# ------------------------
hub = cq.Workplane("XY").circle(hub_d/2).extrude(hub_height)

# ------------------------
# Combine Gear + Hub
# ------------------------
gear_wp = cq.Workplane("XY").add(gear_solid)   # wrap solid in workplane
gear_with_hub = gear_wp.union(hub)

# ------------------------
# Cut D-shaped hole
# ------------------------
# Cylinder part of D
d_cyl = cq.Workplane("XY").circle(motor_shaft_d/2).extrude(hub_height + face_width)

# Flat cut for D
d_flat = (
    cq.Workplane("XY")
    .rect(motor_shaft_d, motor_shaft_d)  # square bigger than D flat
    .extrude(hub_height + face_width)
    .translate((0, -motor_shaft_d/2, 0))
)

# Cut D from hub+gear
gear_with_d_hole = gear_with_hub.cut(d_cyl.union(d_flat))

# ------------------------
# Optional radial screw hole
# ------------------------
gear_final = (
    gear_with_d_hole
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .transformed(offset=(0, 0, hub_height/2))
    .hole(set_screw_d)
)

# ------------------------
# Show final object
# ------------------------
show_object(gear_final)
