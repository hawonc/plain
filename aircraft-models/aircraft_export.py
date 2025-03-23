import bpy

# Ensure the glTF addon is enabled
if not bpy.context.preferences.addons.get("io_scene_gltf2"):
    bpy.ops.preferences.addon_enable(module="io_scene_gltf2")

# Set your desired export path (update the path as needed)
export_path = r"C:\Users\ybrot\OneDrive\Desktop\Projects\plain\aircraft-models\exported_aircraft.gltf"

# Export the entire scene to glTF.
# Options: 'GLTF_EMBEDDED' (all data in one file),
#          'GLTF_SEPARATE' (separate files for textures, etc.),
#          'GLB' (binary).
bpy.ops.export_scene.gltf(filepath=export_path, export_format='GLTF_EMBEDDED')

print("Exported scaled aircraft model to", export_path)
