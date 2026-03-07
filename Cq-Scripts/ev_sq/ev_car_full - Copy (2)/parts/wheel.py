import cadquery as cq

def make_wheel(diameter=30, width=10):
    # Use tags to make assembly easier later
    wheel = (cq.Workplane("XY")
             .circle(diameter / 2).extrude(width)
             .faces(">Z").tag("axle_mate")) # Tagging for assembly
    return wheel
