import cadquery as cq
from params import CarParams as p

def make_bush_holder_plate():
    """Generates the specific plate for the axle bush holders."""
    # We use .box() for a centered, clean primitive
    plate = (
        cq.Workplane("XY")
        .box(
            p.BUSH_HOLDER_PLATE_L, 
            p.BUSH_HOLDER_PLATE_W, 
            p.BUSH_HOLDER_PLATE_T
        )
    )
    return plate

def show_bush_holder_plate(obj=None, color="lightgray", alpha=1.0):
    """Utility to display the plate with custom visuals."""
    if obj is None:
        # If no object is passed, create and translate it using defaults
        obj = make_bush_holder_plate().translate(
            (p.BUSH_HOLDER_X_OFFSET, 0, p.BUSH_HOLDER_Z_HEIGHT)
        )
    
    if "show_object" in globals():
        show_object(obj, options={"color": color, "alpha": alpha})
