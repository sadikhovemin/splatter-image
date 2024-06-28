import bpy

# Clear existing objects in the scene
bpy.ops.object.select_all(action="DESELECT")
bpy.ops.object.select_by_type(type="MESH")
bpy.ops.object.delete()

imported_object = bpy.ops.import_scene.obj(
    filepath="/storage/group/dataset_mirrors/01_incoming/3DFront/3D-FUTURE-model/3062da49-9d90-3894-8c6a-207b131a7f1f/normalized_model.obj"
)
obj_object = bpy.context.selected_objects[0]

# Set camera and rendering settings
scene = bpy.context.scene
camera = bpy.data.cameras.new("Camera")
camera_object = bpy.data.objects.new("Camera", camera)
scene.camera = camera_object

camera_radius = 10  # Distance from object
camera_height = 0  # Height from the base of the object
camera_object.location = (camera_radius, 0, camera_height)
camera_object.rotation_euler = (0, 0, 0)

# Add camera to the scene
bpy.context.collection.objects.link(camera_object)

# Set render resolution
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080

# Set render engine to Cycles for better quality
scene.render.engine = "CYCLES"

# Define angles (degrees) for rotation around the object
angles = [0, 90, 180, 270]

# Render the scene at different angles
for angle in angles:
    camera_object.rotation_mode = "XYZ"
    z_angle = angle * (3.14159 / 180)  # Convert degrees to radians
    camera_object.rotation_euler[2] = z_angle
    camera_object.rotation_euler[0] = 0

    scene.render.filepath = (
        f"/usr/prakt/s0091/github/splatter-image/renders/rendered_image_{angle}.png"
    )

    bpy.ops.render.render(write_still=True)
