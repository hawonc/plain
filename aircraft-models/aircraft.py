import bpy
import math
import uuid
import sys

def store_original_transforms(obj):
    """
    If not already stored, save the object's original location, rotation, and scale.
    """
    if "orig_loc" not in obj.keys():
        obj["orig_loc"] = (obj.location.x, obj.location.y, obj.location.z)
        obj["orig_rot"] = (obj.rotation_euler.x, obj.rotation_euler.y, obj.rotation_euler.z)
        obj["orig_scl"] = (obj.scale.x, obj.scale.y, obj.scale.z)

def restore_original_transforms(obj):
    """
    Restores an object's transforms from stored custom properties.
    """
    if "orig_loc" in obj.keys():
        obj.location = tuple(obj["orig_loc"])
    if "orig_rot" in obj.keys():
        obj.rotation_euler = tuple(obj["orig_rot"])
    if "orig_scl" in obj.keys():
        obj.scale = tuple(obj["orig_scl"])

def scale_and_position_aircraft(
    body_length: float,
    body_diameter: float,
    wing_span_area: float,  # total wing area in m²
    chord_length: float,    # full horizontal span (tip-to-tip) in m
    engine_diameter: float  # desired engine diameter in m
):
    """
    Scales and repositions aircraft parts from the collection "aircraft".
    Expected parts (by name):
      - body
      - tail
      - left_wing, right_wing
      - left_engine_inner, left_engine_outer
      - right_engine_inner, right_engine_outer

    Inputs are assumed to be in real-world meters (and m² for wing area).
    The new parameter 'engine_diameter' is used to scale the engine parts.
    
    For this configuration, only two engines (the inner ones) will be used.
    The outer engines will be hidden.
    """
    # -------------------------------------------------------------------------
    # 1) Retrieve objects by name
    # -------------------------------------------------------------------------
    bpy.ops.wm.open_mainfile(filepath="aircraft.blend")
    col_name = "aircraft"
    col = bpy.data.collections.get(col_name)
    if not col:
        print(f"Collection '{col_name}' not found.")
        return

    part_names = [
        "body", "tail",
        "left_wing", "right_wing",
        "left_engine_inner",
        "right_engine_inner"
    ]
    parts = {}
    for name in part_names:
        obj = col.all_objects.get(name)
        if obj is None:
            print(f"Object '{name}' not found in collection '{col_name}'.")
            return
        parts[name] = obj

    body_obj   = parts["body"]
    tail_obj   = parts["tail"]
    lwing_obj  = parts["left_wing"]
    rwing_obj  = parts["right_wing"]
    lein_obj   = parts["left_engine_inner"]
    rein_obj   = parts["right_engine_inner"]

    # -------------------------------------------------------------------------
    # 2) Store and restore original transforms for consistency
    # -------------------------------------------------------------------------
    all_objs = [body_obj, tail_obj, lwing_obj, rwing_obj, lein_obj, rein_obj]
    for obj in all_objs:
        store_original_transforms(obj)
        restore_original_transforms(obj)

    # -------------------------------------------------------------------------
    # 3) Define reference dimensions (match these to your original model)
    # -------------------------------------------------------------------------
    ref_body_length    = 30.0   # m
    ref_body_diameter  = 3.0    # m
    ref_wing_half_span = 10.0   # m (half of the original wing span)
    ref_wing_chord     = 3.0    # m (original front-to-back dimension of the wing)
    ref_engine_diameter = 0.5   # m (assumed original engine diameter)

    # -------------------------------------------------------------------------
    # 4) Compute scale factors
    # -------------------------------------------------------------------------
    # Body scale factors:
    sf_body_length   = body_length / ref_body_length
    sf_body_diameter = body_diameter / ref_body_diameter

    # For wings:
    # chord_length is the full wing span (tip-to-tip) in m.
    # Therefore, new_wing_half_span = chord_length/2.
    # And the wing's front-to-back dimension (wing_chord) is:
    #     wing_chord = wing_span_area / chord_length
    new_wing_half_span = chord_length / 2.0
    new_wing_chord     = wing_span_area / chord_length

    sf_wing_span  = new_wing_half_span / ref_wing_half_span
    sf_wing_chord = new_wing_chord / ref_wing_chord

    # For engines:
    sf_engine = engine_diameter / ref_engine_diameter

    # -------------------------------------------------------------------------
    # 5) Apply scaling to each part
    # -------------------------------------------------------------------------
    # Body and tail (scale X for length, Y and Z for diameter):
    body_obj.scale = (sf_body_length, sf_body_diameter, sf_body_diameter)
    tail_obj.scale = (sf_body_length, sf_body_diameter, sf_body_diameter)

    # Wings (use X for chord, Y for half-span, Z for thickness)
    wing_thickness = 0.2 * sf_body_diameter  # adjust if needed
    lwing_obj.scale = (sf_wing_chord, sf_wing_span, wing_thickness)
    rwing_obj.scale = (sf_wing_chord, sf_wing_span, wing_thickness)

    # Engines: scale them according to engine_diameter input.
    for eng in [lein_obj, rein_obj]:
        eng.scale = (sf_engine, sf_engine, sf_engine)

    # -------------------------------------------------------------------------
    # 6) Position each part with simple offset logic
    # -------------------------------------------------------------------------
    # Place body at the origin.
    body_obj.location = (0.0, 0.0, 0.0)

    # Tail behind the body.
    tail_offset_x = -ref_body_length * 0.45 * sf_body_length
    tail_obj.location = (tail_offset_x, 0.0, 0.0)

    # Wings: positioned roughly 30% along the fuselage.
    wing_offset_x = body_length * 0.3
    lwing_obj.location = (wing_offset_x, -new_wing_half_span * 0.5, 0.0)
    rwing_obj.location = (wing_offset_x,  new_wing_half_span * 0.5, 0.0)

    # Engines: position them under the wings.
    # Use a fixed clearance to avoid intersection; adjust if needed.
    engine_clearance = 1.0  # m clearance below wing base
    engine_x_offset = wing_offset_x + 1.0
    engine_y_inner  = -new_wing_half_span * 0.3
    engine_y_outer  = -new_wing_half_span * 0.6
    engine_z_offset = -engine_clearance

    # Left engines:
    lein_obj.location  = (engine_x_offset, engine_y_inner, engine_z_offset)
    # Right engines (mirror Y):
    rein_obj.location  = (engine_x_offset, -engine_y_inner, engine_z_offset)

    if not bpy.context.preferences.addons.get("io_scene_gltf2"):
        bpy.ops.preferences.addon_enable(module="io_scene_gltf2")
    
    
    file_name = str(uuid.uuid4()) + ".glb"
    export_path = "models/" + file_name

    # Set your desired export path (update the path as needed)
    

    # Export the entire scene to GLB (binary glTF format).
    bpy.ops.export_scene.gltf(filepath=export_path, export_format='GLB')
    bpy.ops.wm.read_factory_settings(use_empty=True)
    return file_name


# -----------------------------------------------------------------------------
# Example usage:
# -----------------------------------------------------------------------------
# Uncomment and adjust the parameters as needed, then run the script.
# scale_and_position_aircraft(
#     body_length=32.268,       # m
#     body_diameter=4.033,      # m
#     wing_span_area=62.2867,   # m² (total for both wings)
#     chord_length=22.322,      # m (full wing span, tip-to-tip)
#     engine_diameter=0.75    # m (desired engine diameter)
# )

args = sys.argv
if "--" in args:
    idx = args.index("--")
    user_args = args[idx+1:]
else:
    user_args = []

if len(user_args) >= 5:
    try:
        body_length    = float(user_args[0])
        body_diameter  = float(user_args[1])
        wing_span_area = float(user_args[2])
        chord_length   = float(user_args[3])
        engine_diameter= float(user_args[4])
    except Exception as e:
        print("Error parsing arguments. Using default values.", e)
        body_length = 32.268
        body_diameter = 4.033
        wing_span_area = 62.2867
        chord_length = 22.322
        engine_diameter = 0.75
else:
    # Default values if not enough arguments are provided.
    body_length = 32.268       # m
    body_diameter = 4.033      # m
    wing_span_area = 62.2867   # m²
    chord_length = 22.322      # m
    engine_diameter = 0.75     # m

# Run the scaling and exporting function with parameters from command-line (or defaults)
scale_and_position_aircraft(body_length, body_diameter, wing_span_area, chord_length, engine_diameter)


# Example Usage:
# "C:\Program Files\Blender Foundation\Blender 4.4\blender.exe" -b "C:\path\to\your\aircraft.blend" --python "C:\path\to\your\aircraft.py" -- 1 1 1 1 1


