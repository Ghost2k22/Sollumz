import bpy
from mathutils import Vector
from ..properties.extensions import ExtensionsContainer
from ..utils import get_selected_archetype, get_selected_entity, get_selected_ytyp, get_selected_extension


class SOLLUMZ_OT_add_archetype_extension(bpy.types.Operator):
    """Add an extension to the archetype"""
    bl_idname = "sollumz.addarchetypeextension"
    bl_options = {"UNDO"}
    bl_label = "Add Extension"

    @classmethod
    def poll(cls, context):
        return get_selected_archetype(context) is not None

    def execute(self, context):
        selected_archetype = get_selected_archetype(context)
        selected_archetype.new_extension()

        return {"FINISHED"}


class SOLLUMZ_OT_delete_archetype_extension(bpy.types.Operator):
    """Delete the selected extension from the archetype"""
    bl_idname = "sollumz.deletearchetypeextension"
    bl_options = {"UNDO"}
    bl_label = "Delete Extension"

    @classmethod
    def poll(cls, context):
        selected_archetype = get_selected_archetype(context)

        if not selected_archetype:
            return None

        return selected_archetype.selected_extension is not None

    def execute(self, context):
        selected_archetype = get_selected_archetype(context)
        selected_archetype.delete_selected_extension()

        return {"FINISHED"}


class SOLLUMZ_OT_add_entity_extension(bpy.types.Operator):
    """Add an extension to the entity"""
    bl_idname = "sollumz.addentityextension"
    bl_options = {"UNDO"}
    bl_label = "Add Extension"

    @classmethod
    def poll(cls, context):
        return get_selected_entity(context) is not None

    def execute(self, context):
        selected_entity = get_selected_entity(context)
        selected_entity.new_extension()

        return {"FINISHED"}


class SOLLUMZ_OT_delete_entity_extension(bpy.types.Operator):
    """Delete the selected extension from the entity"""
    bl_idname = "sollumz.deleteentityextension"
    bl_options = {"UNDO"}
    bl_label = "Delete Extension"

    @classmethod
    def poll(cls, context):
        selected_entity = get_selected_entity(context)

        if not selected_entity:
            return None

        return selected_entity.selected_extension is not None

    def execute(self, context):
        selected_entity = get_selected_entity(context)
        selected_entity.delete_selected_extension()

        return {"FINISHED"}

class ExtensionUpdateFromSelectionHelper:
    bl_options = {"UNDO"}

    @classmethod
    def poll(cls, context):
        return get_selected_extension(context) is not None
    
    @classmethod
    def set_extension_props(cls, context: bpy.types.Context, verts_location: Vector):
        raise NotImplementedError

    def execute(self, context):
        aobj = context.active_object
        aobj.update_from_editmode()

        me = aobj.data
        selected_vertices = [v.co for v in me.vertices if v.select]
        verts_location = sum(selected_vertices, Vector()) / len(selected_vertices)

        self.set_extension_props(context, verts_location)
        
        return {"FINISHED"}


class SOLLUMZ_OT_update_offset_and_top_from_selected(bpy.types.Operator, ExtensionUpdateFromSelectionHelper):
    """Update ladder offest and top from selection"""
    bl_idname = "sollumz.updateoffsetandtopfromselection"
    bl_options = {"UNDO"}
    bl_label = "Update Offset and Top"

    @classmethod
    def set_extension_props(cls, context: bpy.types.Context, verts_location: Vector):
        ladder_props = get_selected_extension(context).ladder_extension_properties
        ladder_props.offset_position = verts_location
        ladder_props.top = verts_location


class SOLLUMZ_OT_update_bottom_from_selected(bpy.types.Operator, ExtensionUpdateFromSelectionHelper):
    """Update ladder bottom from selection"""
    bl_idname = "sollumz.updatebottomfromselection"
    bl_options = {"UNDO"}
    bl_label = "Update Bottom"

    @classmethod
    def set_extension_props(cls, context: bpy.types.Context, verts_location: Vector):
        ladder_props = get_selected_extension(context).ladder_extension_properties
        ladder_props.bottom = verts_location


class SOLLUMZ_OT_update_particle_effect_location(bpy.types.Operator, ExtensionUpdateFromSelectionHelper):
    """Update particle effect offset from selection"""
    bl_idname = "sollumz.updateptfxoffsetfromselection"
    bl_options = {"UNDO"}
    bl_label = "Update Offset location"

    @classmethod
    def set_extension_props(cls, context: bpy.types.Context, verts_location: Vector):
        particle_props = get_selected_extension(context).particle_extension_properties
        particle_props.offset_position = verts_location


class SOLLUMZ_OT_update_light_shaft_offeset_location(bpy.types.Operator, ExtensionUpdateFromSelectionHelper):
    """Update light shaft offset from selection"""
    bl_idname = "sollumz.updatelightshaftoffsetfromselection"
    bl_options = {"UNDO"}
    bl_label = "Update Offset location"


    @classmethod
    def set_extension_props(cls, context: bpy.types.Context, verts_location: Vector):
        light_shaft_props = get_selected_extension(context).light_shaft_extension_properties
        light_shaft_props.offset_position = verts_location


class SOLLUMZ_OT_update_corner_a_location(bpy.types.Operator, ExtensionUpdateFromSelectionHelper):
    """Update light shaft corner A location from selection"""
    bl_idname = "sollumz.updatecornerafromselection"
    bl_options = {"UNDO"}
    bl_label = "Update Corner A"

    @classmethod
    def set_extension_props(cls, context: bpy.types.Context, verts_location: Vector):
        light_shaft_props = get_selected_extension(context).light_shaft_extension_properties
        light_shaft_props.cornerA = verts_location

class SOLLUMZ_OT_update_corner_b_location(bpy.types.Operator, ExtensionUpdateFromSelectionHelper):
    """Update light shaft corner B location from selection"""
    bl_idname = "sollumz.updatecornerbfromselection"
    bl_options = {"UNDO"}
    bl_label = "Update Corner B"

    @classmethod
    def set_extension_props(cls, context: bpy.types.Context, verts_location: Vector):
        light_shaft_props = get_selected_extension(context).light_shaft_extension_properties
        light_shaft_props.cornerB = verts_location

class SOLLUMZ_OT_update_corner_c_location(bpy.types.Operator, ExtensionUpdateFromSelectionHelper):
    """Update light shaft corner C location from selection"""
    bl_idname = "sollumz.updatecornercfromselection"
    bl_options = {"UNDO"}
    bl_label = "Update Corner C"

    @classmethod
    def set_extension_props(cls, context: bpy.types.Context, verts_location: Vector):
        light_shaft_props = get_selected_extension(context).light_shaft_extension_properties
        light_shaft_props.cornerC = verts_location

class SOLLUMZ_OT_update_corner_d_location(bpy.types.Operator, ExtensionUpdateFromSelectionHelper):
    """Update light shaft corner D location from selection"""
    bl_idname = "sollumz.updatecornerdfromselection"
    bl_options = {"UNDO"}
    bl_label = "Update Corner D"

    @classmethod
    def set_extension_props(cls, context: bpy.types.Context, verts_location: Vector):
        light_shaft_props = get_selected_extension(context).light_shaft_extension_properties
        light_shaft_props.cornerD = verts_location