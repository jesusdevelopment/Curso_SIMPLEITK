# %% [markdown]
import SimpleITK as sitk
# Crear una imagen sintética en blanco de 512x512 píxeles y 100 cortes, de tipo entero de 16 bits
image = sitk.Image([512, 512, 100], sitk.sitkInt16)
# Consultar el tamaño
size = image.GetSize()
print(f"Tamaño de la matriz (X, Y, Z): {size}")
# %% [markdown]
# Definir un espaciado isotrópico de 1.0 mm en todas las direcciones
image.SetSpacing([1.0, 1.0, 1.0])
spacing = image.GetSpacing()
print(f"Espaciado de los vóxeles (mm): {spacing}")
# %% [markdown]
# Establecer el origen físico de la esquina superior izquierda / primer vóxel en el espacio real
image.SetOrigin([-125.5, -125.5, -50.0])
origin = image.GetOrigin()
print(f"Origen espacial en el mundo (mm): {origin}")
# %% [markdown]
# Obtener la matriz de dirección actual
direction = image.GetDirection()
print(f"Matriz de dirección (cosenos directores): {direction}")

# %% [markdown]
# Consultar el tipo de píxel actual
pixel_type_str = image.GetPixelIDTypeAsString()
print(f"Tipo de píxel de la imagen: {pixel_type_str}")
# Convertir (Castear) la imagen a números de punto flotante de 32 bits (común en redes neuronales y filtros)
image_float = sitk.Cast(image, sitk.sitkFloat32)
print(f"Nuevo tipo de píxel: {image_float.GetPixelIDTypeAsString()}")
# %%

