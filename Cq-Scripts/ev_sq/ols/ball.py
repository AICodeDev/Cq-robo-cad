import cadquery as cq

# PARAMETERS - Customize these
BALL_DIAMETER = 12  # mm - adjust to your needs (15, 20, 25, 30mm common)

# Create the sphere
ball = cq.Workplane("XY").sphere(BALL_DIAMETER / 2)

# Export to STL
# cq.exporters.export(ball, f'caster_ball_{BALL_DIAMETER}mm.stl')

# Display the ball (if using CQ-Editor or similar)
show_object(ball)