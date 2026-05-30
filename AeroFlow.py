bl_info = {
    "name": "AeroFlow",
    "blender": (3, 0, 0),
    "category": "Object",
}

import bpy
from mathutils import Vector

def airflow_vector(direction):
    if direction == "+X": return (1, 0, 0)
    if direction == "-X": return (-1, 0, 0)
    if direction == "+Y": return (0, 1, 0)
    if direction == "-Y": return (0, -1, 0)
    if direction == "+Z": return (0, 0, 1)
    if direction == "-Z": return (0, 0, -1)
    return (1, 0, 0)

def projected_area(obj, direction):
    matrix = obj.matrix_world
    world_corners = [matrix @ Vector(corner) for corner in obj.bound_box]
    
    xs = [c.x for c in world_corners]
    ys = [c.y for c in world_corners]
    zs = [c.z for c in world_corners]
    
    x = max(xs) - min(xs)
    y = max(ys) - min(ys)
    z = max(zs) - min(zs)

    dx, dy, dz = direction

    ax = y * z * abs(dx)
    ay = x * z * abs(dy)
    az = x * y * abs(dz)

    return ax + ay + az

def drag_force(obj, direction, v=10.0, Cd=1.0):
    A = projected_area(obj, direction)
    return 0.5 * Cd * A * v * v

@bpy.app.handlers.persistent
def auto_update_drag(scene, depsgraph):
    obj = bpy.context.active_object
    if obj and obj.type == 'MESH':
        try:
            direction = airflow_vector(scene.air_direction)
            v = scene.drag_velocity
            Cd = scene.drag_coefficient
            
            drag = drag_force(obj, direction, v, Cd)
            obj["drag_value"] = drag
        except:
            pass

class OBJECT_OT_calculate_drag(bpy.types.Operator):
    bl_idname = "object.calculate_drag"
    bl_label = "Calculate Drag"

    def execute(self, context):
        obj = context.active_object
        if not obj:
            self.report({'WARNING'}, "No active object selected")
            return {'CANCELLED'}

        scene = context.scene
        direction = airflow_vector(scene.air_direction)
        v = scene.drag_velocity
        Cd = scene.drag_coefficient

        drag = drag_force(obj, direction, v, Cd)
        obj["drag_value"] = drag

        self.report({'INFO'}, f"Drag: {drag:.4f}")
        return {'FINISHED'}

class VIEW3D_PT_drag_panel(bpy.types.Panel):
    bl_label = "Drag Estimator"
    bl_idname = "VIEW3D_PT_drag_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Drag'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "air_direction")
        layout.prop(scene, "drag_velocity")
        layout.prop(scene, "drag_coefficient")
        layout.operator("object.calculate_drag")

def register_props():
    bpy.types.Scene.air_direction = bpy.props.EnumProperty(
        name="Air Direction",
        items=[
            ("+X", "+X", ""), ("-X", "-X", ""),
            ("+Y", "+Y", ""), ("-Y", "-Y", ""),
            ("+Z", "+Z", ""), ("-Z", "-Z", ""),
        ],
        default="+X"
    )
    bpy.types.Scene.drag_velocity = bpy.props.FloatProperty(name="Velocity", default=10.0)
    bpy.types.Scene.drag_coefficient = bpy.props.FloatProperty(name="Cd", default=1.0)

classes = [OBJECT_OT_calculate_drag, VIEW3D_PT_drag_panel]

def register():
    for c in classes:
        bpy.utils.register_class(c)
    register_props()
    bpy.app.handlers.depsgraph_update_post.append(auto_update_drag)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    if auto_update_drag in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(auto_update_drag)

    del bpy.types.Scene.air_direction
    del bpy.types.Scene.drag_velocity
    del bpy.types.Scene.drag_coefficient

if __name__ == "__main__":
    register()
