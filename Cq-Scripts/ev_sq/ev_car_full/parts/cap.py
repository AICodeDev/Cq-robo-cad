import cadquery as cq
from params import CarParams as CapParams

def make_cap():
    """
    Creates the cap part by accessing CapParams class attributes directly.
    """
    # 1. Base Cylinder
    
    # CAP_PIPE_HOLE_SIDE: float = 8.1    
    # CAP_PIPE_TOP_DIA: float = 11 + 2 -0.1 #small (12.9)
    # CAP_PIPE_BASE_DIA: float =  CAP_PIPE_TOP_DIA + 2 -0.1 #Big
    # CAP_PIPE_BASE_HEIGHT: float = 1.0
    # CAP_PIPE_TOP_HEIGHT: float = 12
    
    # Big circle
    
    result = (
        cq.Workplane("XY")
        .circle((CapParams.CAP_PIPE_BASE_DIA / 2) + 1)
        .extrude(CapParams.CAP_PIPE_BASE_HEIGHT+0.1)
    )
    
    # 2. Top Cylinder (Stacked)
    result = (
        result.faces(">Z")
        .workplane()
        .circle(CapParams.CAP_PIPE_TOP_DIA / 2 + 0.1)
        .extrude(CapParams.CAP_PIPE_TOP_HEIGHT+3)
    )
    
    # 3. Square Hole
    result = (
        result.faces(">Z")
        .workplane()
        .rect(CapParams.CAP_PIPE_HOLE_SIDE, CapParams.CAP_PIPE_HOLE_SIDE)
        .cutThruAll()
    )
    
    return result


def make_cap_old():
    """
    Creates the cap part by accessing CapParams class attributes directly.
    """
    # 1. Base Cylinder
    result = (
        cq.Workplane("XY")
        .circle(CapParams.CAP_PIPE_BASE_DIA / 2)
        .extrude(CapParams.CAP_PIPE_BASE_HEIGHT)
    )
    
    # 2. Top Cylinder (Stacked)
    result = (
        result.faces(">Z")
        .workplane()
        .circle(CapParams.CAP_PIPE_TOP_DIA / 2)
        .extrude(CapParams.CAP_PIPE_TOP_HEIGHT)
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
