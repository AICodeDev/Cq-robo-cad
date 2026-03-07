import cadquery as cq
import sys

# Plate size
plate_x = 120
plate_y = 88
thickness = 8
cell = 8
cell2 = cell + 1

# Hole specs
hole_dia = 4
hole_dia_final = 3.8
padding = 2
spacing = 8  # 4mm hole + 2mm + 2mm = 8mm spacing

x_count = 15
y_count = 11

extrude_wall =3



# Dimensions (mm)
length = plate_x
width = plate_y
base_thickness = thickness
factor_motor = 8.5 / 3.5
factor_castor = 15 / 3.5

##########
# Define parameters for pencil holder
prect_width = 16-2-2
prect_height = 24
phole_radius = 3.7
semicircle_radius = phole_radius
base_extrusion = 2.5
cylinder_radius = phole_radius + 2.5
cylinder_height = 16-2


# Calculate positions
semicircle_center_y = prect_height / 2-4
castor_extrude = 8
motor_extrude = 4.5
extra_cut=16


# STEP 1: Create base plate
print("Creating base plate...")
plate = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(base_thickness)
)

plate.faces(">Z").workplane().tag("plateBase")

# STEP 2: Add cutouts in left and right halves
print("Adding center cutouts...")

# Calculate center positions for each half
# Plate is centered at origin, so extends from -60 to +60 in X
left_half_center_x = -30   # Center of left half (30mm left of origin)
right_half_center_x = 30   # Center of right half (30mm right of origin)

# Cut dimensions for right side (base cut)
cut_length_right = 42
cut_width_right = 52

cut_length = cut_length_right *1.2
cut_width = cut_width_right

#center
plateCut = (
    plate.workplaneFromTagged("plateBase")
    
    .rect(20, cut_width_right+extra_cut)
    .cutThruAll()
)

#left
# Make cut in right half
plateCut = (
    plateCut.workplaneFromTagged("plateBase")
    .center(-right_half_center_x, 0)  # Move to right half center
    .rect(cut_length_right, cut_width_right+extra_cut)
    .cutThruAll()
)
#right
plateCut = (
    plateCut.workplaneFromTagged("plateBase")
    .center(right_half_center_x, 0)  # Move to right half center
    .rect(cut_length_right, cut_width_right)
    .cutThruAll()
)

#left of right

plateCut = (
    plateCut.workplaneFromTagged("plateBase")
    .center(right_half_center_x-12, 0)  # Move to right half center
    .rect(cut_length_right/2, cut_width_right+extra_cut)
    .cutThruAll()
)
#show_object(plateCut)

caster1= (    
    plateCut    
    .workplaneFromTagged("plateBase")
    .center(cell *7 , -cell *2 )
    .rect(cell,cell*1.5)
    .extrude(castor_extrude)
)
#show_object(caster1, name='Castor Ext' )



caster2= (    
    caster1
    .workplaneFromTagged("plateBase")
    #.faces(">Z")    
    .center(cell *7 , +cell *2 )
    .rect(cell,cell*1.5)
    .extrude(castor_extrude)  
)
#show_object(caster2)


plateHole = (
    caster2
    .faces("<Z")  # Select bottom face
    .workplane(centerOption="CenterOfBoundBox")
    .rarray(spacing, spacing, x_count, y_count)
    .hole(hole_dia)
)
#show_object(plateHole, name="step4_final_with_holes")

#y = width snall

def is_inner_wall_y(f):
    bb = f.BoundingBox()
    xlen = bb.xlen
    ylen = bb.ylen
    t = bb.zlen
    print(bb,xlen,ylen,t)
    return t == 8 and 54 <= ylen <= 68

walls_inner_y = (
    plateHole
    .faces("|X ")   # outer + inner vertical walls
    .filter(is_inner_wall_y)
)

show_object(walls_inner_y, name="walls_inner_y")
"""
walls_inner_y = (
    plateHole
    .faces("|Y ")   # outer + inner vertical walls
    .filter(
        lambda f: (
            abs(f.Center().x) < plate_y -3 and
            abs(f.Center().x) > plate_y/2 +10    
        )
    )
)

show_object(walls_inner_y, name="walls_inner_y")
"""
result = plateHole  # start with original solid
for f in walls_inner_y:
    bb = f.BoundingBox()
    xlen = bb.xlen  # width along X
    ylen = bb.ylen  # width along Y
    t = bb.zlen

    print ("Face Y Size", xlen,ylen,t, f.Center().x )
      
    # extrude along this vector
    result = result.union(
        cq.Workplane(obj=f)
        #.faces("|X ")
        .workplane(centerOption="CenterOfMass")
        #.rect(f.BoundingBox().xlen, f.BoundingBox().ylen)   # or your desired rectangle for rib
        .rect(plate_y-16,thickness)        
        .extrude(extrude_wall)
    )

show_object(result, name="inner_walls_extrudedx")


def is_inner_wall_x(f):
    bb = f.BoundingBox()
    xlen = bb.xlen
    ylen = bb.ylen
    t = bb.zlen
    print("is_inner_wall_x",xlen,ylen,t)
    return t == 8 and 54 <= xlen <= plate_x -10

walls_inner_x = (
    result
    .faces("|Y ")   # outer + inner vertical walls
    .filter(is_inner_wall_x)
)

show_object(walls_inner_x, name="walls_inner_x")
show_object(result, name="before")


for f in walls_inner_x:
    bb = f.BoundingBox()
    xlen = bb.xlen  # width along X
    ylen = bb.ylen  # width along Y
    t = bb.zlen

    print ("Face Y Size", xlen,ylen,t, f.Center().x )
      
    # extrude along this vector
    result = result.union(
        cq.Workplane(obj=f)
        #.faces("|X ")
        .workplane(centerOption="CenterOfMass")
        #.rect(f.BoundingBox().xlen, f.BoundingBox().ylen)   # or your desired rectangle for rib
        .rect(plate_y-8,thickness)        
        .extrude(extrude_wall)
    )

show_object(result, name="inner_walls_extrudedy-longside")



# Step 1: Create the profile: rectangle with semicircle on one side
holder_profile = (cq.Workplane("XY")
           .moveTo(0, -prect_height/2)  # Start at bottom center
           .lineTo(prect_width/2, -prect_height/2)   # Bottom right
           .lineTo(prect_width/2, prect_height/2)    # Right side up
           .threePointArc((0, prect_height/2 + semicircle_radius), 
                         (-prect_width/2, prect_height/2))  # Semicircle at top
           .lineTo(-prect_width/2, -prect_height/2)  # Left side down
           .close()          # Close the shape
           .extrude(5))      # Extrude by 4mm

# Step 2: Select the center of the semicircle, draw cylinder and create hole
pencile_holder = (holder_profile
          .faces(">Z")      # Select top face
          .workplane()
          .center(0, semicircle_center_y)    # Move to center of semicircle
          .circle(cylinder_radius)        # Draw circle for cylinder
          .extrude(cylinder_height)      # Extrude cylinder upward
          .faces(">Z")      # Select top face of cylinder
          .workplane()
          .circle(phole_radius)        # Draw hole
          .cutThruAll())    # Cut hole through everything


height = 20  # Define height variable
holder_positioned = pencile_holder .rotate((0,0,0), (0,0,1), -90) .translate((
    (plate_x/2 )+cell +3 ,  # Front, outside by 10mm
    0,                     # Center
    0               # Sitting on base
))
show_object(holder_positioned)



all = result.union(holder_positioned)
show_object(all, name="all")
















