import cadquery as cq

thickness=4

# Step 1: Create base plate
plate = (
    cq.Workplane("XY")
    .rect(120, 88)
    .extrude(thickness)
)

# Step 2: Make rectangular cutout
cut_length = 86
cut_width = 54

plate_cut = (
    plate
    .faces(">Z")
    .workplane()
    .rect(cut_length, cut_width)
    .cutThruAll()
)

walls_inner = (
    plate_cut
    .faces("|X ")   # outer + inner vertical walls
    .filter(
        lambda f: (
            abs(f.Center().x) < cut_length / 2 +5 and
            abs(f.Center().y) < cut_width / 2 +5
        )
    )
)

show_object(walls_inner, name="walls_inner")


walls_inner_y = (
    plate_cut
    .faces("|Y ")   # outer + inner vertical walls
    .filter(
        lambda f: (
            abs(f.Center().x) < cut_length / 2 +5 and
            abs(f.Center().y) < cut_width / 2 +5
        )
    )
)

show_object(walls_inner_y, name="walls_inner_y")




result = plate_cut  # start with original solid

for f in walls_inner:
    # vector from face center to plate center (0,0)
    center = f.Center()
    direction = cq.Vector(0, 0, 0) - cq.Vector(center)
    
    # make sure the vector is in XY plane only
    direction = cq.Vector(direction.x, direction.y, 0).normalized()
    
    # extrude along this vector
    result = result.union(
        cq.Workplane(obj=f)
        #.faces("|X ")
        .workplane(centerOption="CenterOfMass")
        #.rect(f.BoundingBox().xlen, f.BoundingBox().ylen)   # or your desired rectangle for rib
        .rect(cut_width,thickness)        
        .extrude(thickness*2)
    )

show_object(result, name="inner_walls_extruded")



for f in walls_inner_y:   
    # extrude along this vector
    result = result.union(
        cq.Workplane(obj=f)        
        .workplane(centerOption="CenterOfMass")
        .rect(cut_length,thickness)        
        .extrude(thickness*2)
    )

show_object(result, name="inner_walls_extrudedyy")


