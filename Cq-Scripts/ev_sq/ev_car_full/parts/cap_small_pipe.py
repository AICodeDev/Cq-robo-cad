import cadquery as cq
from params import CarParams as CapParams


def make_cap_small_pipe():
    # 1. Base Cylinder
    result = (
        cq.Workplane("XY")
        .circle(CapParams.CAP_PIPE_TOP_DIA / 2)
        .extrude(32)
    )
    
    # 2. Four Horizontal Holes
    # Use the XZ plane to drill "sideways" through the cylinder
    # result = (
        # result.copyWorkplane(cq.Workplane("XZ"))
        # .center(0, 8)  # Start 4mm from the bottom (Z=4 in global, Y in local XZ)
        # .pushPoints([(0, i * 16) for i in range(4)]) # Space 4 holes 16mm apart
        # .hole(4.15)
    # )
    
    
    result = (
        result.copyWorkplane(cq.Workplane("XZ"))
        .center(0, 8)  # First hole at 8mm height
        .pushPoints([(0, i * 16) for i in range(4)])
        .circle(4.15 / 2) # Create circle (diameter / 2 for radius)
        .cutThruAll() # "both=True" ensures it cuts in both directions from center
    )
    # 3. Square Hole
    result = (
        result.faces(">Z")
        .workplane()
        .rect(CapParams.CAP_PIPE_HOLE_SIDE+0.1, CapParams.CAP_PIPE_HOLE_SIDE+0.1)
        .cutThruAll()
    )
    
    return result


def make_cap_small_pipe2():
    """
    Creates the cap part by accessing CapParams class attributes directly.
    """
    # 1. Base Cylinder
    result = (
        cq.Workplane("XY")
        .circle(CapParams.CAP_PIPE_TOP_DIA / 2)
        .extrude(60)
    )
    
    result = (
        result.faces(">X") # Select the side face
        .workplane(offset=0) 
        .center(0, 4) # Start at 4mm from the base (Y is vertical in this plane)
        .pushPoints([(0, i * 16) for i in range(4)]) # Space 4 holes 16mm apart
        .hole(4.2)
    )
    
   
    
    # 3. Square Hole
    result = (
        result.faces(">Z")
        .workplane()
        .rect(CapParams.CAP_PIPE_HOLE_SIDE, CapParams.CAP_PIPE_HOLE_SIDE)
        .cutThruAll()
    )
    
    return result

if __name__ == "__main__":
    shape = make_cap()
    if "show_object" in globals():
        show_object(shape)
