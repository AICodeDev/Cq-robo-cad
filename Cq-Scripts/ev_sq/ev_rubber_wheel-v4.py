import cadquery as cq
import math

import cadquery as cq
radius_hw = 4
radius_rod = math.sqrt(16+16)

# Parameters matching your gear

rim_width = 4

spoke_count = 6
spoke_thickness = 4 # Thickness of each spoke
rim_height=18
rim_thickness=2.4
outer_rim_radius = 68/2
root_radius = outer_rim_radius - rim_thickness

# Root diameter is roughly pitch - 2.5*module
root_diameter = root_radius*2
inner_rim_radius = (root_diameter / 2) - rim_width
hub_diameter = 10.5+4+2
hub_radius = hub_diameter / 2

hub_height = 16+2

# 1. Create the Hub
hub_base = cq.Workplane("XY").circle(hub_radius).extrude(hub_height)

hub = (
    hub_base
    .faces(">Z")
    .workplane()
    .circle(hub_radius-1).extrude(10+6)


)

show_object(hub)



# 2. Create a Single Spoke
# We calculate the length to span from the hub to the inner rim
spoke_length = root_radius - hub_radius +2

# Build one spoke centered on the X-axis
single_spoke = (
    cq.Workplane("XY")
    .rect(spoke_length, spoke_thickness)
    .extrude(5)
    .translate([(spoke_length/2) + hub_radius-1, 0, 0])
)
spoke_shape = single_spoke.val()
# 3. Create the Spoke Pattern
# Use polarArray to place the spoke 6 times
spokes = (
    cq.Workplane("XY")
    .polarArray(radius=0, startAngle=0, angle=360, count=spoke_count)
    # Use loc for the location provided by polarArray
    .eachpoint(lambda loc: spoke_shape.located(loc))
)

# 4. Combine everything
# You would union this with your RingGear object
spoke_system = hub.union(spokes)

# Create the Rim
# We use cicle().circle() to create a hollow ring in one operation
rim = (
    cq.Workplane("XY")
    .circle(outer_rim_radius)   # Outer edge
    .circle(root_radius)        # Inner hole
    .extrude(rim_height, combine=True)
)


wheel = rim.union(spoke_system)

wheel2 = (
    wheel
    .faces("<Z")
    .workplane()
    .circle(4/2)
    .cutThruAll()    
    .rect(8.15,8.15)
    .cutBlind(-hub_height-10-10)
    

    #.cutThruAll()
)
show_object(wheel2)
cq.exporters.export(wheel2, 'rub_wheel4.stl', tolerance=0.01, angularTolerance=0.05)



"""
after_hole2 = (
    after_hole
    .faces(">Z")
    .workplane()
    .circle(radius_rod +1).extrude(5)
    
)

show_object(after_hole2)
"""


