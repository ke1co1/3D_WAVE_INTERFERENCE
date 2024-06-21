import bpy
import csv

# Path to your CSV file
csv_file_path = r""

# Create new material
material_name = "LightBlueMaterial"
if material_name not in bpy.data.materials:
    mat = bpy.data.materials.new(name=material_name)
else:
    mat = bpy.data.materials[material_name]

mat.use_nodes = True
nodes = mat.node_tree.nodes
bsdf = nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs["Base Color"].default_value = (0.678, 0.847, 1.0, 1)  # Light blue color

# Clear existing object with the same name
if "PointObject" in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects["PointObject"], do_unlink=True)

# Create new mesh and object
mesh = bpy.data.meshes.new(name="PointMesh")
obj = bpy.data.objects.new("PointObject", mesh)

# Link object to the scene
bpy.context.collection.objects.link(obj)

# Assign the material to the object
if obj.data.materials:
    obj.data.materials[0] = mat
else:
    obj.data.materials.append(mat)

# Create the mesh from the CSV data
verts = []
edges = []
try:
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                x = float(row["x"])
                y = float(row["y"])
                z = float(row["z"])
                verts.append((x, y, z))
            except ValueError as e:
                print(f"Skipping row with invalid data: {row} - {e}")
except FileNotFoundError:
    print(f"File not found: {csv_file_path}")
except KeyError as e:
    print(f"CSV file is missing expected column: {e}")

# Add the central point (0, 0, 0)
central_point_index = len(verts)
verts.append((0, 0, 0))

# Create edges connecting each point to the central point
edges = [(central_point_index, i) for i in range(central_point_index)]

# Update the mesh with the vertices and edges
mesh.from_pydata(verts, edges, [])
mesh.update()

# Ensure the material is visible
obj.show_instancer_for_viewport = True
obj.show_instancer_for_render = True

# Select the object
bpy.context.view_layer.objects.active = obj

# Add spinning animation
frame_start = 1
frame_end = 250
rotation_amount = 2 * 3.14159  # 360 degrees in radians

# Insert keyframe at the start
obj.rotation_euler = (0, 0, 0)
obj.keyframe_insert(data_path="rotation_euler", frame=frame_start)

# Insert keyframe at the end
obj.rotation_euler = (0, 0, rotation_amount)
obj.keyframe_insert(data_path="rotation_euler", frame=frame_end)

# Set the interpolation mode to linear
action = obj.animation_data.action
for fcurve in action.fcurves:
    for keyframe in fcurve.keyframe_points:
        keyframe.interpolation = 'LINEAR'
