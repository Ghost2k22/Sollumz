import bpy
import traceback
from Sollumz.ydr.shader_materials import create_shader, shadermats
from Sollumz.resources.shader import ShaderManager
from Sollumz.sollumz_properties import ObjectType, is_sollum_type, SOLLUMZ_UI_NAMES

def create_empty(sollum_type):
    empty = bpy.data.objects.new(SOLLUMZ_UI_NAMES[sollum_type], None)
    empty.empty_display_size = 0
    empty.sollum_type = sollum_type
    bpy.context.collection.objects.link(empty)
    bpy.context.view_layer.objects.active = bpy.data.objects[empty.name]

    return empty

class SOLLUMZ_OT_create_drawable(bpy.types.Operator):
    """Create a sollumz drawable"""
    bl_idname = "sollumz.createdrawable"
    bl_label = f"Create {SOLLUMZ_UI_NAMES[ObjectType.DRAWABLE]}"

    def execute(self, context):
        
        create_empty(ObjectType.DRAWABLE)

        return {'FINISHED'}

class SOLLUMZ_OT_create_drawable_model(bpy.types.Operator):
    """Create a sollumz drawable model"""
    bl_idname = "sollumz.createdrawablemodel"
    bl_label = f"Create {SOLLUMZ_UI_NAMES[ObjectType.DRAWABLE_MODEL]}"

    def execute(self, context):
        
        create_empty(ObjectType.DRAWABLE_MODEL)

        return {'FINISHED'}

class SOLLUMZ_OT_create_geometry(bpy.types.Operator):
    """Create a sollumz geometry"""
    bl_idname = "sollumz.creategeometry"
    bl_label = f"Create {SOLLUMZ_UI_NAMES[ObjectType.GEOMETRY]}"

    def execute(self, context):
        
        create_empty(ObjectType.GEOMETRY)

        return {'FINISHED'}

class SOLLUMZ_OT_quick_convert_mesh_to_drawable(bpy.types.Operator):
    """Quickly setup a gta drawable via a mesh object"""
    bl_idname = "sollumz.quickconvertmeshtodrawable"
    bl_label = "Quick Convert Mesh To Drawable"

    def execute(self, context):
        
        aobj = bpy.context.active_object
        if(aobj == None):
            return {'CANCELLED'}
        
        #create material
        sm = ShaderManager()
        mat = create_shader("default", sm)
        aobj.data.materials.append(mat)
        
        #set parents
        bpy.ops.sollumz.createdrawable()
        dobj = bpy.context.active_object
        bpy.ops.sollumz.createdrawablemodel()
        dmobj = bpy.context.active_object
        dmobj.parent = dobj
        aobj.parent = dmobj

        #set properties
        aobj.sollum_type = ObjectType.GEOMETRY

        return {'FINISHED'}

class SOLLUMZ_OT_convert_to_shader_material(bpy.types.Operator):
    """Convert material to a sollumz shader material"""
    bl_idname = "sollumz.converttoshadermaterial"
    bl_label = "Convert Material To Shader Material"

    def fail(self, name, reason):
        self.report({"INFO"}, "Material " + name + " can not be converted due to: " + reason)
        return {'CANCELLED'}

    def execute(self, context):
        
        aobj = bpy.context.active_object
        if(aobj == None):
            self.fail("", "No active object selected.")
        
        if(len(aobj.data.materials) != 1):
            self.fail("", "Active object can only have one material.")

        mat = aobj.data.materials[0]

        try:
            bsdf = mat.node_tree.nodes["Principled BSDF"]

            if(bsdf == None):
                self.fail(mat.name, "Material must have a Principled BSDF node.")

            diffuse_node = None
            diffuse_input = bsdf.inputs["Base Color"]
            if diffuse_input.is_linked:
                diffuse_node = diffuse_input.links[0].from_node

            if not isinstance(diffuse_node, bpy.types.ShaderNodeTexImage):
                self.fail(mat.name, "Material has no diffuse image.")
                
            specular_node = None
            specular_input = bsdf.inputs["Specular"]
            if specular_input.is_linked:
                specular_node = specular_input.links[0].from_node

            if not isinstance(diffuse_node, bpy.types.ShaderNodeTexImage):
                specular_node = None
            
            normal_node = None
            normal_input = bsdf.inputs["Normal"]
            if len(normal_input.links) > 0:
                normal_map_node = normal_input.links[0].from_node
                normal_map_input = normal_map_node.inputs["Color"]
                if len(normal_map_input.links) > 0:
                    normal_node = normal_map_input.links[0].from_node

            if not isinstance(normal_node, bpy.types.ShaderNodeTexImage):
                normal_node = None

            shader_name = "default"

            if normal_node != None and specular_node != None:
                shader_name = "normal_spec"
            elif normal_node != None and specular_node == None:
                shader_name = "normal"
            elif normal_node == None and specular_node != None:
                shader_name = "spec"

            #remove old materials
            for i in range(len(aobj.material_slots)):
                bpy.ops.object.material_slot_remove({'object': aobj})

            sm = ShaderManager()
            new_mat = create_shader(shader_name, sm)
            #new_mat.name = mat.name
            aobj.data.materials.append(new_mat) 

            bsdf = new_mat.node_tree.nodes["Principled BSDF"]       

            new_diffuse_node = None
            diffuse_input = bsdf.inputs["Base Color"]
            if diffuse_input.is_linked:
                new_diffuse_node = diffuse_input.links[0].from_node

            if(diffuse_node != None):
                new_diffuse_node.image = diffuse_node.image

            new_specular_node = None
            specular_input = bsdf.inputs["Specular"]
            if specular_input.is_linked:
                new_specular_node = specular_input.links[0].from_node

            if(specular_node != None):
                new_specular_node.image = specular_node.image

            new_normal_node = None
            normal_input = bsdf.inputs["Normal"]
            if len(normal_input.links) > 0:
                normal_map_node = normal_input.links[0].from_node
                normal_map_input = normal_map_node.inputs["Color"]
                if len(normal_map_input.links) > 0:
                    new_normal_node = normal_map_input.links[0].from_node

            if(normal_node != None):
                new_normal_node.image = normal_node.image
        except:
            self.fail(mat.name, traceback.format_exc())

        return {'FINISHED'}

class SOLLUMZ_OT_create_shader_material(bpy.types.Operator):
    """Create a sollumz shader material"""
    bl_idname = "sollumz.createshadermaterial"
    bl_label = "Create Shader Material"

    def execute(self, context):
        
        aobj = bpy.context.active_object
        if(aobj == None):
            return {'CANCELLED'}
        
        if is_sollum_type(aobj, ObjectType.GEOMETRY):
            sm = ShaderManager()
            mat = create_shader(shadermats[context.scene.shader_material_index].value, sm)
            aobj.data.materials.append(mat)
        
        return {'FINISHED'}

class SOLLUMZ_OT_BONE_FLAGS_NewItem(bpy.types.Operator): 
    bl_idname = "sollumz.bone_flags_new_item" 
    bl_label = "Add a new item"
    def execute(self, context): 
        bone = context.active_pose_bone.bone
        bone.bone_properties.flags.add() 
        return {'FINISHED'}

class SOLLUMZ_OT_BONE_FLAGS_DeleteItem(bpy.types.Operator): 
    bl_idname = "sollumz.bone_flags_delete_item" 
    bl_label = "Deletes an item" 
    @classmethod 
    def poll(cls, context): 
        return context.active_pose_bone.bone.bone_properties.flags

    def execute(self, context): 
        bone = context.active_pose_bone.bone

        list = bone.bone_properties.flags
        index = bone.bone_properties.ul_index
        list.remove(index) 
        bone.bone_properties.ul_index = min(max(0, index - 1), len(list) - 1) 
        return {'FINISHED'}