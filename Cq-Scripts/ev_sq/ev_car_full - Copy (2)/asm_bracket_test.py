from parts.bush_holder_bracket import make_bush_holder_bracket
import cadquery as cq


# Create the primary (left) bracket
bracket_L = make_bush_holder_bracket()

# Create the mirrored (right) bracket
bracket_R = bracket_L.mirror(mirrorPlane="YZ")

# Position them side-by-side (adjust Y based on your chassis width)
bracket_L = bracket_L.translate((-20, 0, 0))
bracket_R = bracket_R.translate((20, 0, 0))

show_object(bracket_L, name="Bush_Bracket_L", options={"color": "orange"})
show_object(bracket_R, name="Bush_Bracket_R", options={"color": "orange"})
