import bpy
import numpy as np
import os
import math
import mathutils

# Clear existing objects
bpy.ops.object.select_all(action="DESELECT")
bpy.ops.object.select_by_type(type="MESH")
bpy.ops.object.delete()

# Load the model
model_path = "/storage/group/dataset_mirrors/01_incoming/3DFront/3D-FUTURE-model/3062da49-9d90-3894-8c6a-207b131a7f1f/normalized_model.obj"
bpy.ops.import_scene.obj(filepath=model_path)

# Set up rendering
bpy.context.scene.render.engine = "CYCLES"
bpy.context.scene.render.resolution_x = 1024
bpy.context.scene.render.resolution_y = 1024

output_path = "/usr/prakt/s0091/github/splatter-image/renders_5/images/"
if not os.path.exists(output_path):
    os.makedirs(output_path)

# Add a light source
light_data = bpy.data.lights.new(name="light_2.80", type="POINT")
light_object = bpy.data.objects.new(name="light_2.80", object_data=light_data)
bpy.context.collection.objects.link(light_object)
light_object.location = (5, -5, 10)

# Get the object
obj = bpy.context.selected_objects[0]

# Calculate the bounding box dimensions
scale = obj.scale
dims = obj.dimensions
max_dim = max(dims.x * scale.x, dims.y * scale.y, dims.z * scale.z)

# Set camera distance based on the largest dimension
camera_distance = max_dim * 3

# Add a camera
camera_data = bpy.data.cameras.new(name="Camera")
camera_object = bpy.data.objects.new("Camera", camera_data)
bpy.context.collection.objects.link(camera_object)
bpy.context.scene.camera = camera_object

# Add a constraint to make the camera look at the object
constraint = camera_object.constraints.new(type="TRACK_TO")
constraint.target = obj
constraint.track_axis = "TRACK_NEGATIVE_Z"
constraint.up_axis = "UP_Y"


# Function to render and save images and parameters
def render_and_save(camera, obj, index):
    bpy.context.view_layer.update()  # Update the scene to register changes
    bpy.context.scene.render.filepath = os.path.join(output_path, f"{index:03d}.png")
    bpy.ops.render.render(write_still=True)

    # Save the camera's rotation matrix and translation
    cam_matrix = np.array(camera.matrix_world)
    np.save(os.path.join(output_path, f"{index:03d}.npy"), cam_matrix)


# Render 12 views by rotating the camera around the object
num_views = 12
angle_increment = 2 * math.pi / num_views

for i in range(num_views):
    angle = i * angle_increment
    camera_object.location.x = obj.location.x + camera_distance * math.cos(angle)
    camera_object.location.y = obj.location.y + camera_distance * math.sin(angle)
    camera_object.location.z = obj.location.z

    render_and_save(camera_object, obj, i)
