import cadquery as cq



# Step 1: Create the profile: rectangle with semicircle on one side
profile = (cq.Workplane("XY")
           .moveTo(0, -10)  # Start at bottom center
           .lineTo(5, -10)   # Bottom right
           .lineTo(5, 10)    # Right side up
           .threePointArc((0, 15), (-5, 10))  # Semicircle at top
           .lineTo(-5, -10)  # Left side down
           .close()          # Close the shape
           .extrude(4))      # Extrude by 4mm

# Step 2: Select the center of the semicircle, draw cylinder with 5mm radius
result = (profile
          .faces(">Z")      # Select top face
          .workplane()
          .center(0, 10)    # Move to center of semicircle
          .circle(5)        # Draw circle with 5mm radius
          .extrude(10)      # Extrude cylinder upward by 10mm
          .faces(">Z")      # Select top face of cylinder
          .workplane()
          .circle(3)        # Draw hole with 3mm radius
          .cutThruAll())    # Cut hole through everything

# Display the result
show_object(result)