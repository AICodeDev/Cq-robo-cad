import cadquery as cq

# ============================================
# PARAMETERS
# ============================================

adapter_dia = 12.0

motor_side_len = 9.0
wheel_side_len = 9.0
middle_plate_len = 2.0

# D-shaft sizes
motor_d_radius = 3+0.1     # FEMALE D (motor shaft Ø6 mm)
wheel_d_radius = 2.5+0.1     # MALE D (wheel Ø5 mm)

wheel_clearance_dia = 10.0-0.75

# ============================================
# MOTOR SIDE — FEMALE D (CUT)
# ============================================

motor_base = (
    cq.Workplane("XY")
    .circle(adapter_dia / 2)
    .extrude(motor_side_len)
)

motor_d_female = (
    cq.Workplane("XY")
    .moveTo(-motor_d_radius, 0)
    .radiusArc((0, motor_d_radius), motor_d_radius)
    .radiusArc((motor_d_radius, 0), motor_d_radius)
    .radiusArc((0, -motor_d_radius), motor_d_radius)
    .lineTo(-motor_d_radius, 0)
    .close()
    .extrude(motor_side_len)
)

motor_side = motor_base.cut(motor_d_female)

# ============================================
# MIDDLE PLATE
# ============================================

middle_plate = (
    cq.Workplane("XY")
    .workplane(offset=motor_side_len)
    .circle(adapter_dia / 2)
    .extrude(middle_plate_len)
)

# ============================================
# WHEEL SIDE — MALE D (UNION)
# ============================================

wheel_base = (
    cq.Workplane("XY")
    .workplane(offset=motor_side_len + middle_plate_len)
    .circle(adapter_dia / 2)
    .extrude(wheel_side_len)
)

# clearance hole (wheel already has hole)
wheel_clearance = (
    cq.Workplane("XY")
    .workplane(offset=motor_side_len + middle_plate_len)
    .circle(wheel_clearance_dia / 2)
    .extrude(wheel_side_len)
)

wheel_base = wheel_base.cut(wheel_clearance)

wheel_d_male = (
    cq.Workplane("XY")
    .workplane(offset=motor_side_len + middle_plate_len)
    .moveTo(-wheel_d_radius, 0)
    .radiusArc((0, wheel_d_radius), wheel_d_radius)
    .radiusArc((wheel_d_radius, 0), wheel_d_radius)
    .radiusArc((0, -wheel_d_radius), wheel_d_radius)
    .lineTo(-wheel_d_radius, 0)
    .close()
    .extrude(wheel_side_len)
)

wheel_side = wheel_base.union(wheel_d_male)

# ============================================
# FINAL ADAPTER
# ============================================

shaft_adapter = motor_side.union(middle_plate).union(wheel_side)

show_object(shaft_adapter, options={"color": "gray", "alpha": 0.95})

# ============================================
# SIDE SET-SCREW HOLES (M2)
# ============================================

m2_clearance_dia = 2.2      # M2 clearance
set_screw_depth = adapter_dia

# --- Motor side set screw (female D side) ---
motor_set_screw = (
    cq.Workplane("YZ")
    .workplane(offset=adapter_dia / 2)
    .center(0, motor_side_len / 2)
    .circle(m2_clearance_dia / 2)
    .extrude(-set_screw_depth)
)

# --- Wheel side set screw (male D side) ---
wheel_set_screw = (
    cq.Workplane("YZ")
    .workplane(offset=adapter_dia / 2)
    .center(0, motor_side_len + middle_plate_len + wheel_side_len / 2)
    .circle(m2_clearance_dia / 2)
    .extrude(-set_screw_depth)
)

# --- Cut both holes ---
shaft_adapterf = shaft_adapter.cut(motor_set_screw).cut(wheel_set_screw)

show_object(shaft_adapterf, options={"color": "gray", "alpha": 0.95})

