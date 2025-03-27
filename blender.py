import bpy


# Eliminar todos los objetos de la escena
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Limpiar cualquier material, luz o cámara
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# Eliminar todos los materiales (opcional, si deseas eliminar materiales también)
for material in bpy.data.materials:
    material.user_clear()
    bpy.data.materials.remove(material)

# Resetear el mundo (background) y la luz
bpy.context.scene.world = None
bpy.context.scene.world = bpy.data.worlds.new("World")

# Restablecer el motor de renderizado a 'CYCLES' (o el que desees)
bpy.context.scene.render.engine = 'CYCLES'

print("Escena reiniciada correctamente.")

# Ruta al modelo YCB (ajusta según el archivo descargado)
obj_path = "C:/Users/user/Escritorio/Repositories/TFG/YCB_Objetos/frutas/012_strawberry/tsdf/textured.obj"

# Importar el modelo
bpy.ops.wm.obj_import(filepath=obj_path)

# Seleccionar el objeto recién importado
obj = bpy.context.selected_objects[0]
obj.rotation_euler = (0, 0, 0)
obj.location = (2, 1, -0.4)

# if object strawberry
obj.scale = (2, 2, 2)
obj.name = "YCB_Object"

# Verificar si el objeto tiene un material, si no, crear uno
if not obj.data.materials:
    material = bpy.data.materials.new(name="NewMaterial")
    obj.data.materials.append(material)
else:
    material = obj.data.materials[0]

material.use_nodes = True

# Obtener el nodo Principled BSDF
bsdf = material.node_tree.nodes["Principled BSDF"]

# Crear un nodo de textura para el objeto YCB
texture_image = bpy.data.images.load("C:/Users/user/Escritorio/Repositories/TFG/YCB_Objetos/frutas/012_strawberry/tsdf/textured.png")  # Especifica la ruta a tu archivo de textura

bpy.context.scene.render.engine = 'CYCLES'

# Crear el nodo de imagen
texture_node = material.node_tree.nodes.new(type="ShaderNodeTexImage")
texture_node.image = texture_image

# Crear el nodo de coordenadas UV
uv_node = material.node_tree.nodes.new(type="ShaderNodeTexCoord")

# Conectar el nodo UV al nodo de imagen
material.node_tree.links.new(uv_node.outputs["UV"], texture_node.inputs["Vector"])

# Conectar el nodo de textura al Principled BSDF
material.node_tree.links.new(texture_node.outputs["Color"], bsdf.inputs["Base Color"])

# Asegurarse de que el objeto tiene un UV map
if not obj.data.uv_layers:
    # Si no tiene UV map, crearlo
    obj.data.uv_layers.new()

# El UV map por defecto es el primero en la lista
uv_map = obj.data.uv_layers[0]

# Asegurarte de que el objeto está en modo objeto para aplicar los cambios
bpy.ops.object.mode_set(mode="OBJECT")

print("Textura aplicada correctamente al objeto YCB.")


# Crear una mesa con un cubo escalado
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, -0.5))
mesa_shadow = bpy.context.object
mesa_shadow.name = "Mesa"
mesa_shadow.scale[0] = 2  # Ancho
mesa_shadow.scale[1] = 2.5  # Largo
mesa_shadow.scale[2] = 0.1  # Grosor

# Asegurar que la mesa reciba sombras
mesa_shadow.cycles.is_shadow_catcher = True


bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, -0.5))
mesa = bpy.context.object
mesa.name = "Mesa"
mesa.scale[0] = 2  # Ancho
mesa.scale[1] = 2.5  # Largo
mesa.scale[2] = 0.1  # Grosor
# Crear un material para la mesa
material_mesa = bpy.data.materials.new(name="MaterialMesa")

material_mesa.use_nodes = True

# Ruta a la textura para la mesa (ajusta según tu archivo de textura)
texture_mesa_image_path = "C:/Users/user/Escritorio/Repositories/TFG/YCB_Objetos/beige-wooden-textured-flooring-background.jpg"  # Especifica la ruta a tu archivo de textura

# Cargar la imagen de la textura
texture_mesa_image = bpy.data.images.load(texture_mesa_image_path)

# Crear el nodo de textura para la mesa
texture_mesa_node = material_mesa.node_tree.nodes.new(type="ShaderNodeTexImage")
texture_mesa_node.image = texture_mesa_image

# Crear el nodo de coordenadas UV para la mesa
uv_mesa_node = material_mesa.node_tree.nodes.new(type="ShaderNodeTexCoord")

# Conectar el nodo UV al nodo de imagen
material_mesa.node_tree.links.new(uv_mesa_node.outputs["UV"], texture_mesa_node.inputs["Vector"])

# Obtener el nodo Principled BSDF para la mesa
bsdf_mesa = material_mesa.node_tree.nodes["Principled BSDF"]

# Conectar la textura al Principled BSDF de la mesa
material_mesa.node_tree.links.new(texture_mesa_node.outputs["Color"], bsdf_mesa.inputs["Base Color"])

# Asegurarse de que la mesa tenga un UV map
if not mesa.data.uv_layers:
    # Si no tiene UV map, crearlo
    mesa.data.uv_layers.new()

# El UV map por defecto es el primero en la lista
uv_mesa_map = mesa.data.uv_layers[0]

# Asignar el material de la mesa
mesa.data.materials.append(material_mesa)

# Cambiar al modo objeto para aplicar los cambios
bpy.ops.object.mode_set(mode="OBJECT")

print("Textura aplicada correctamente a la mesa.")




import random

def colocar_objetos(objetos, min_x=-1, max_x=0, min_y=-0.4, max_y=1):
    for obj in objetos:
        obj.location.x = random.uniform(min_x, max_x)
        obj.location.y = random.uniform(min_y, max_y)
        obj.location.z = 0.0  # Altura sobre la mesa (banana = 0.05, strawberry = 0)
        obj.rotation_euler.z = random.uniform(0, 3.14)

# Obtener todos los objetos importados
objetos_ycb = [obj for obj in bpy.data.objects if "YCB_Object" in obj.name]

# Colocarlos aleatoriamente sobre la mesa
colocar_objetos(objetos_ycb)





# Activar la luz de entorno HDRI
# Asegurarse de que el mundo (background) de la escena usa nodos
bpy.context.scene.world.use_nodes = True

# Obtener los nodos del mundo (background)
nodes = bpy.context.scene.world.node_tree.nodes

# Crear un nodo de textura de entorno (HDRI)
node_env = nodes.new(type='ShaderNodeTexEnvironment')

# Cargar la imagen HDRI (ajusta la ruta según tu archivo)
node_env.image = bpy.data.images.load("C:/Users/user/Escritorio/Repositories/TFG/YCB_Objetos/poly_haven_studio_4k.hdr")  # Asegúrate de que la ruta sea correcta

# Obtener el nodo de "Background" (fondo) y conectarlo al HDRI
node_background = nodes["Background"]
bpy.context.scene.world.node_tree.links.new(node_env.outputs["Color"], node_background.inputs["Color"])

# Ajustar la intensidad del HDRI, si es necesario
node_background.inputs["Strength"].default_value = 1.0  # Ajusta la intensidad de la iluminación del HDRI


# Crear una cámara
bpy.ops.object.camera_add(location=(1, -1, 1))
cam = bpy.context.object
cam.rotation_euler = (1.2, 0, 0.8)  # Ajustar el ángulo

# Establecerla como cámara activa
bpy.context.scene.camera = cam


bpy.context.scene.render.resolution_x = 512
bpy.context.scene.render.resolution_y = 512
bpy.context.scene.render.resolution_percentage = 100

bpy.context.scene.cycles.shadow_threshold = 0.01
bpy.context.scene.cycles.use_fast_gi = True

bpy.context.scene.render.engine = 'CYCLES'  # Usar Cycles
bpy.context.scene.render.image_settings.file_format = 'PNG'  # Formato PNG
bpy.context.scene.render.filepath = "C:/Users/user/Escritorio/img1.png"  # Guardar imagen

# Ejecutar render
bpy.ops.render.render(write_still=True)
