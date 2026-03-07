import cadquery as cq
from params import CarParams as p

def make_bush_holder_bracket():
    # --- 1. BUILD THE UPRIGHT (The vertical part with the BIG hole) ---
    upright = (
        cq.Workplane("XY")
        .box(p.BUSH_HOLDER_BRACKET_UPRIGHT_W, p.BUSH_HOLDER_BRACKET_BASE_L, p.BUSH_HOLDER_BRACKET_UPRIGHT_H)
        .faces(">X").workplane()
        # Move up to the axle height (relative to the center of the box)
        .pushPoints([(p.BUSH_HOLDER_BRACKET_AXLE_Z - (p.BUSH_HOLDER_BRACKET_UPRIGHT_H/2), 0)])
        .hole(p.BUSH_HOLDER_BRACKET_AXLE_HOLE_D)
    )

    # --- 2. BUILD THE BASE (The flat part with 2 SMALL holes) ---
    base = (
        cq.Workplane("XY")
        .box(p.BUSH_HOLDER_BRACKET_BASE_W, p.BUSH_HOLDER_BRACKET_BASE_L, p.BUSH_HOLDER_BRACKET_BASE_H)
        .faces(">Z").workplane()
        .pushPoints([(0, -p.BUSH_HOLDER_BRACKET_BASE_HOLE_OFFSET), 
                     (0, p.BUSH_HOLDER_BRACKET_BASE_HOLE_OFFSET)])
        .hole(p.BUSH_HOLDER_BRACKET_BASE_HOLE_D)
    )

    # --- 3. POSITION AND COMBINE ---
    # Shift the base so it sits 'outside' the upright
    # Since upright width is 3, we shift the base center by (Base_W/2 + Upright_W/2)
    shift_x = (p.BUSH_HOLDER_BRACKET_BASE_W / 2) + (p.BUSH_HOLDER_BRACKET_UPRIGHT_W / 2)
    base = base.translate((shift_x, 0, -(p.BUSH_HOLDER_BRACKET_UPRIGHT_H/2) + (p.BUSH_HOLDER_BRACKET_BASE_H/2)))

    # Union them and move the whole part so the bottom is at Z=0
    bracket = upright.union(base).translate((0, 0, p.BUSH_HOLDER_BRACKET_UPRIGHT_H / 2))
    
    return bracket
