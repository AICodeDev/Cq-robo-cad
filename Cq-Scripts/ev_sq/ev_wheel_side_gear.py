import cadquery as cq
import math
from cq_gears  import BevelGear, SpurGear

# ------------------------
# Parameters
# ------------------------
motor_shaft_d = 6        # motor shaft diameter
hub_d = 6.2 + 6+2+1                # hub cylinder outer diameter
hub_height = 25.6 -10+2         # hub height
gear_module = 1.25
teeth_number = 18
cone_angle = 45
face_width = 6
pressure_angle = 20
helix_angle = 0
set_screw_d = 3          # optional radial screw
module = 2              # gear module




# --- Desired pitch radius ---
pitch_radius = 12  # mm
pitch_diameter = pitch_radius * 2

# --- Gear parameters ---
module = 2
teeth_number = 12 # int(pitch_diameter / module)  # teeth = 22/2 = 11
pressure_angle = 24
face_width = 20-10-2
total_height =25.8

# --- Create the spur gear ---


gear = SpurGear(
    teeth_number=20,#was 25
    module=0.99,
    pressure_angle=pressure_angle,#24
    width=face_width,
    helix_angle=0 # straight teeth
)
gear_solid = gear.build()
show_object(gear_solid)



# ------------------------
# Create Hub Cylinder
# ------------------------
hub = cq.Workplane("XY").circle(hub_d/2).extrude(hub_height)
show_object(hub)

hub = (
    hub
    .faces(">Z")              # Start at the top face
    .workplane(offset=-4) # Move to the vertical middle of the hub
    .transformed(rotate=(0, 90, 0))  # Rotate to face the side wall
    .circle(2)                # 4mm diameter hole
     .cutThruAll()  # T
)

show_object(hub)

# ------------------------
# Combine Gear + Hub
# ------------------------
gear_wp = cq.Workplane("XY").add(gear_solid)   # wrap solid in workplane
gear_with_hub = gear_wp.union(hub)
gear_with_hub = gear_wp

# ------------------------
# Parameters
# ------------------------
outer_d = 7.0 #

outer_d = 7.2 #

length = 60



# ------------------------
# Cut hex hole
# ------------------------
gear_with_hole = (
    gear_with_hub
    .faces(">Z")
    .workplane()
    .rect(8.15,8.15)
    .cutThruAll()
)
show_object(gear_with_hole)






