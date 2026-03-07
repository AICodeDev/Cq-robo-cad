import cadquery as cq

# Define parameters
rect_width = 10
rect_height = 15
semicircle_radius = rect_width/2
base_extrusion = 2.5
cylinder_radius = rect_width/2
cylinder_height = 10
hole_radius = 3.5

# Calculate positions
semicircle_center_y = rect_height / 2

# Step 1: Create the profile: rectangle with semicircle on one side
profile = (cq.Workplane("XY")
           .moveTo(0, -rect_height/2)  # Start at bottom center
           .lineTo(rect_width/2, -rect_height/2)   # Bottom right
           .lineTo(rect_width/2, rect_height/2)    # Right side up
           .threePointArc((0, rect_height/2 + semicircle_radius), 
                         (-rect_width/2, rect_height/2))  # Semicircle at top
           .lineTo(-rect_width/2, -rect_height/2)  # Left side down
           .close()          # Close the shape
           .extrude(base_extrusion))      # Extrude by 4mm

# Step 2: Select the center of the semicircle, draw cylinder and create hole
result = (profile
          .faces(">Z")      # Select top face
          .workplane()
          .center(0, semicircle_center_y)    # Move to center of semicircle
          .circle(cylinder_radius)        # Draw circle for cylinder
          .extrude(cylinder_height)      # Extrude cylinder upward
          .faces(">Z")      # Select top face of cylinder
          .workplane()
          .circle(hole_radius)        # Draw hole
          .cutThruAll())    # Cut hole through everything

# Display the result
show_object(result)