import cadquery as cq
from params import CarParams as p
import cadquery as cq
def make_axle():
    """Generates the axle geometry at the origin."""
    return cq.Workplane("XY").box(
        p.AXLE_LENGTH, 
        p.AXLE_THICKNESS, 
        p.AXLE_THICKNESS
    )

def show_axle(obj, color="blue", alpha=0.5):
    """
    Displays any passed CadQuery object with custom styling.
    obj: The CadQuery object to show
    color: Name (string) or RGB tuple (0-255)
    alpha: 0.0 (transparent) to 1.0 (opaque)
    """
    # Check if show_object exists (standard in CQ-editor)
    
    show_object(
        obj, 
        options={"color": color, "alpha": alpha}
    )
