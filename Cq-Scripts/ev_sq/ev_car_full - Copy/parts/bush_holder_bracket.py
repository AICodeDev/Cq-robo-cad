import cadquery as cq
from params import CarParams as p


def make_bush_holder_bracket():
    # --- 1. THE BASE (Flat part with 2 small holes) ---
    # We build it at the origin (0,0,0) first
    base = (
        cq.Workplane("XY")
        .rect(p.BUSH_HOLDER_BRACKET_BASE_W, p.BUSH_HOLDER_BRACKET_BASE_L)
        .extrude(p.BUSH_HOLDER_BRACKET_BASE_H)
    )
    # Add the two small holes on top
    base = (
        base.faces(">Z")
        .workplane()
        .pushPoints([(0, -4), (0, 4)]) 
        .hole(p.BUSH_HOLDER_BRACKET_BASE_HOLE_D)
    )
    # Move the base to the side (your original -5 offset)
    base = base.translate((-5, 0, 0))

    # --- 2. THE UPRIGHT (Vertical part with 1 BIG hole) ---
    upright = (
        cq.Workplane("XY")
        .rect(p.BUSH_HOLDER_BRACKET_UPRIGHT_W, p.BUSH_HOLDER_BRACKET_BASE_L)
        .extrude(p.BUSH_HOLDER_BRACKET_UPRIGHT_H)
    )
    # Add the big hole on the side (Face >X)
    upright = (
        upright.faces(">X")
        .workplane()
        .pushPoints([(0, 50)]) 
        .hole(p.BUSH_HOLDER_BRACKET_AXLE_HOLE_D)
    )

    # --- 3. COMBINE ---
    # Combine the upright and the translated base
    bracket = upright.union(base)
    
    return bracket
