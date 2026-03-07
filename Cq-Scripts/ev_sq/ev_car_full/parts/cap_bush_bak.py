import cadquery as cq
from params import CarParams as p

# --- Top Level Variables (Planar Plate) ---
PLATE_WIDTH = 100.0   # Dimension along X axis
PLATE_HEIGHT = 50.0    # Dimension along Y axis
PLATE_THICKNESS = 10.0
SCREW_HOLE_DIA = 3.0

def make_cap_bush():
    # Ring Parameters
    outer_dia = (p.CAP_PIPE_BASE_DIA) + 0.2
    inner_dia = (p.CAP_PIPE_TOP_DIA) + 1
    ring_height = 6
    
    # 1. Create the Rectangular Plate (Guarantees Planar Faces)
    result = cq.Workplane("XY").box(PLATE_WIDTH, PLATE_HEIGHT, PLATE_THICKNESS)
    
    # 2. Left Planar Wall: Two Holes (6mm deep)
    # Selecting the flat left face of the box
    result = (
        result.faces("<X")
        .workplane()
        .pushPoints([(8, 0), (-8, 0)]) # Coordinates relative to face center
        .hole(SCREW_HOLE_DIA, depth=6)
    )
    
    # 3. Right Planar Wall: Add the Ring
    # Selecting the flat right face of the box
    result = (
        result.faces(">X")
        .workplane()
        .circle(outer_dia / 2)
        .extrude(ring_height)
    )
    
    # 4. Common Hole: Pass through BOTH Ring and Plate
    # Selecting the new top-most planar face of the ring
    result = (
        result.faces(">X")
        .workplane()
        .circle(inner_dia / 2)
        .cutThruAll()
    )
    
    return result
