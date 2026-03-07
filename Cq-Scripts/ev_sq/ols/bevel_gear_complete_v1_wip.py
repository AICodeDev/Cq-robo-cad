import cadquery as cq
from cq_gears  import BevelGear, SpurGear

# ------------------------
# Parameters
# ------------------------
motor_shaft_d = 6        # motor shaft diameter
hub_d = 8                # hub cylinder outer diameter
hub_height = 12           # hub height
gear_module = 1.25
teeth_number = 18
cone_angle = 45
face_width = 6
pressure_angle = 20
helix_angle = 0
set_screw_d = 3          # optional radial screw
module = 2              # gear module
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




# --- Desired pitch radius ---
pitch_radius = 12  # mm
pitch_diameter = pitch_radius * 2

# --- Gear parameters ---
module = 2
teeth_number = int(pitch_diameter / module)  # teeth = 22/2 = 11
pressure_angle = 20
face_width = 5






gear_solid = gear.build()
show_object(gear_solid)
# ------------------------
# Create Hub Cylinder
# ------------------------
hub = cq.Workplane("XY").circle(hub_d/2).extrude(hub_height)

# ------------------------
# Combine Gear + Hub
# ------------------------
gear_wp = cq.Workplane("XY").add(gear_solid)   # wrap solid in workplane
gear_with_hub = gear_wp.union(hub)


# Parameters
motor_shaft_d = 6.0         # shaft diameter
motor_flat_offset = 0.1     # clearance
motor_d_radius = motor_shaft_d / 2 + motor_flat_offset
motor_side_len = 9.0        # depth of D-hole (along Z-axis)

# --- Create D-shaped profile ---
motor_d_female = (
    cq.Workplane("XY")
    .moveTo(-motor_d_radius, 0)
    .radiusArc((0, motor_d_radius), motor_d_radius)
    .radiusArc((motor_d_radius, 0), motor_d_radius)
    .radiusArc((0, -motor_d_radius), motor_d_radius)
    .lineTo(-motor_d_radius, 0)
    .close()
    .extrude(motor_side_len*2)
)

show_object(motor_d_female)



# Cut D from hub+gear
gear_with_d_hole = gear_with_hub.cut(motor_d_female)

# ------------------------
# Optional radial screw hole
# ------------------------


# ------------------------
# Show final object
# ------------------------
show_object(gear_with_d_hole)

gear_final=gear_with_d_hole

# ========================
# ADDITIONAL FEATURES
# ========================
# ========================
# FIX: RADIAL SET SCREW HOLE
# ========================

set_screw_d = 2.2   # M2 clearance
cap_thickness = 2.0

# ========================
# SIMPLE CLOSING DISK WITH HOLE
# ========================



# ========================
# SIMPLE CLOSING DISK WITH HOLE
# ========================

cap_thickness = 2.0
set_screw_d = 2.2   # M2 clearance (use 3.2 for M3)
# --- Closing disk ---
closing_disk = (
    cq.Workplane("XY")
    .circle(hub_d / 2)
    .extrude(cap_thickness)
    .faces(">Z")               # select the top face
    .workplane()               # create a workplane on the top
    .circle(set_screw_d / 2)  # draw the hole
    .cutThruAll()              # cut through the disk
)

show_object(closing_disk);


# --- Move disk to far side of gear ---
#closing_disk2 = closing_disk.translate(
#    (0, 0, hub_height + face_width - cap_thickness)
#)

#show_object(closing_disk2);

spur_gear_complete = gear_final.union(closing_disk)
show_object(spur_gear_complete)

# --- Union with existing geometry ---
#gear_complete = gear_final.union(closing_disk)

#show_object(gear_complete)
