bl_info = {
    "name": "Dissolve 2-Edge Vertices",
    "author": "woow3d",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "Edit Mode > Vertex",
    "description": "Dissolve vertices connected to exactly two edges",
    "category": "Mesh",
}

import bpy
import bmesh


class MESH_OT_dissolve_two_edge_verts(bpy.types.Operator):
    bl_idname = "mesh.dissolve_two_edge_verts"
    bl_label = "Dissolve 2-Edge Vertices"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.edit_object
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "يجب أن تكون في Edit Mode على Mesh")
            return {'CANCELLED'}

        mesh = obj.data
        bm = bmesh.from_edit_mesh(mesh)

        bm.verts.ensure_lookup_table()
        selected_verts = [v for v in bm.verts if v.select]

        if not selected_verts:
            self.report({'INFO'}, "لم يتم تحديد أي Vertex")
            return {'CANCELLED'}
        verts_to_dissolve = [
            v for v in selected_verts
            if len(v.link_edges) == 2
        ]

        if not verts_to_dissolve:
            self.report({'INFO'}, "لا يوجد Vertices تنطبق عليها الشروط")
            return {'CANCELLED'}

        bmesh.ops.dissolve_verts(
            bm,
            verts=verts_to_dissolve
        )

        bmesh.update_edit_mesh(mesh)
        return {'FINISHED'}


# إضافة الأمر إلى قائمة Vertex
def vertex_menu_func(self, context):
    self.layout.separator()
    self.layout.operator(
        MESH_OT_dissolve_two_edge_verts.bl_idname,
        icon='AUTOMERGE_OFF'
    )


def register():
    bpy.utils.register_class(MESH_OT_dissolve_two_edge_verts)
    bpy.types.VIEW3D_MT_edit_mesh_vertices.append(vertex_menu_func)


def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_vertices.remove(vertex_menu_func)
    bpy.utils.unregister_class(MESH_OT_dissolve_two_edge_verts)


if __name__ == "__main__":
    register()
