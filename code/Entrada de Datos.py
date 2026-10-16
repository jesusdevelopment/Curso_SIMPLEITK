# %% [markdown]
# ## Bibliotecas
import os
import dicom2nifti as d2n
import numpy as np
import SimpleITK as sitk

#%% [markdown]
# ## Conversión de imágenes DICOM a NIfTI
# 1. Definir la carpeta de salida (no un archivo .nii.gz directo)
output_dir = "/home/jesusr/imgs/nifti_salida"
os.makedirs(output_dir, exist_ok=True)

# 2. Convertir la serie DICOM completa a formato NIfTI
d2n.convert_directory(
    dicom_directory="/home/jesusr/imgs/CT_only",
    output_folder=output_dir,
    compression=True,
    reorient=True,
)
print(f"Conversión finalizada. Los archivos se guardaron en: {output_dir}")

# %% [markdown]
# ## Leyendo un archivo NIFTI
image_nifti = sitk.ReadImage("/home/jesusr/imgs/nifti_salida/201_abd-pel_radioter.nii.gz")
pixel_id = image_nifti.GetPixelID()
# 1. Consultar metadatos espaciales básicos
print(f"Espaciado: {image_nifti.GetSpacing()}")
print(f"Origen: {image_nifti.GetOrigin()}")
print(f"Tamaño: {image_nifti.GetSize()}")
print(f"Tipo de píxel: {image_nifti.GetPixelID()}")
print(f"Tipo de píxel: {sitk.GetPixelIDValueAsString(pixel_id)}")
print(f"Tipo de píxel: {image_nifti.GetPixelIDTypeAsString()}")
# 2. Consultar el diccionario de metadatos específicos del archivo (si existen)
# (Común en formatos como DICOM o NIfTI con campos extendidos)
keys = image_nifti.GetMetaDataKeys()
print(f"Claves de metadatos disponibles: {len(keys)}")
# 3. Listar y recorrer todas las claves de metadatos disponibles
print("\n--- Listado completo de metadatos ---")
for key in image_nifti.GetMetaDataKeys():
    value = image_nifti.GetMetaData(key)
    print(f"Tag: {key} = {value}")
# %% [markdown]
# ## Leyendo un archivo NIFTI con ImageFileReader   
reader = sitk.ImageFileReader()
reader.SetFileName("/home/jesusr/imgs/nifti_salida/201_abd-pel_radioter.nii.gz")

# 1. Leer únicamente la cabecera (metadatos espaciales y tamaño) sin cargar los píxeles
reader.ReadImageInformation()

print(f"Tamaño antes de cargar píxeles: {reader.GetSize()}")
print(f"Espaciado: {reader.GetSpacing()}")

# Forma correcta de obtener el tipo de píxel desde el lector:
pixel_id = reader.GetPixelID()
print(f"Tipo de píxel: {sitk.GetPixelIDValueAsString(pixel_id)}")

# 2. Cargar finalmente el volumen completo a memoria RAM
image_reader = reader.Execute()
# 3. Consultar los metadatos directamente sobre el objeto 'image' ya cargado
keys = image_reader.GetMetaDataKeys()
print(f"Claves de metadatos disponibles: {len(keys)}")
# %% [markdown]
# ## Leyendo un archivo de imagen DICOM
# Cargar la imagen completa
image_I100 = sitk.ReadImage("/home/jesusr/imgs/Dicom I/I100")
# 1. Verificar si existe una clave específica (ej. Nombre del Paciente - DICOM 0010|0010)
tag_paciente = "0010|0010"
if image_I100.HasMetaDataKey(tag_paciente):
    nombre = image_I100.GetMetaData(tag_paciente)
    print(f"Nombre del Paciente: {nombre}")
else:
    print("La clave de paciente no está presente en los metadatos.")
keys = image_I100.GetMetaDataKeys()
print(f"Claves de metadatos disponibles: {len(keys)}")
# 2. Listar y recorrer todas las claves de metadatos disponibles
print("\n--- Listado completo de metadatos ---")
for key in image_I100.GetMetaDataKeys():
    value = image_I100.GetMetaData(key)
    print(f"Tag: {key} = {value}")
# %% [markdown]
# ## Leyendo una carpeta de imágenes DICOM con ImageSeriesReader

# Ruta de la carpeta donde están tus archivos DICOM
ruta_carpeta = "/home/jesusr/imgs/Dicom I"

# 1. Obtener automáticamente la lista ordenada de archivos de la serie DICOM
reader = sitk.ImageSeriesReader()
dicom_names = reader.GetGDCMSeriesFileNames(ruta_carpeta)
reader.SetFileNames(dicom_names)

# 2. ¡CRUCIAL! Habilitar la actualización del array de metadatos por cada corte
reader.MetaDataDictionaryArrayUpdateOn()

# 3. Cargar el volumen completo con el lector configu rado
image = reader.Execute()

# 4. Comprobar si el primer archivo (índice 0) tiene claves de metadatos disponibles
print(f"Total de archivos en la serie: {len(dicom_names)}")
keys = reader.GetMetaDataKeys(0)  # Ahora sí consultará el índice 0 correctamente

if len(keys) > 0:
    print("\n--- ¡Sí hay metadatos! Listado de tags encontrados en el archivo 0: ---")
    for key in keys:
        valor = reader.GetMetaData(0, key)
        print(f"Tag {key} = {valor}")
else:
    print("\nEl archivo DICOM no contiene ningún metadato legible o la cabecera está vacía/anonimizada.")

# 5. Verificar el metadato del paciente directamente en el primer corte del lector
tag_paciente = "0010|0010" # Nombre del Paciente
if reader.HasMetaDataKey(0, tag_paciente):
    nombre = reader.GetMetaData(0, tag_paciente)
    print(f"\nNombre del Paciente: {nombre}")
else:
    print("\nLa clave de paciente no está presente o está vacía en los metadatos de este archivo.")

print(f"Dimensiones del volumen 3D cargado: {image.GetSize()}")
# %% [markdown]
# ## Conversión de imagen a punto flotante (float32)

# Cargar imagen raw (ej. desde archivo comprimido nifti)
image_raw = sitk.ReadImage("/home/jesusr/imgs/nifti_salida/201_abd-pel_radioter.nii.gz")
print(f"Tipo nativo original: {image_raw.GetPixelIDTypeAsString()}")

# Casting inmediato a punto flotante de 32 bits
image_float = sitk.Cast(image_raw, sitk.sitkFloat32)
print(f"Tipo optimizado: {image_float.GetPixelIDTypeAsString()}")
# %%
import SimpleITK as sitk

ruta_carpeta = "/home/jesusr/imgs/Dicom I"

# 1. Obtener la lista ordenada de ficheros DICOM de la carpeta
dicom_names = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(ruta_carpeta)

# 2. Pasar la lista de archivos directamente a sitk.ReadImage
image = sitk.ReadImage(dicom_names)

# 3. Comprobar los metadatos en la imagen resultante
tag_paciente = "0010|0010"
if image_I100.HasMetaDataKey(tag_paciente):
    nombre = image_I100.GetMetaData(tag_paciente)
    print(f"Nombre del Paciente: {nombre}")
else:
    print("La clave de paciente no está presente en los metadatos.")
keys = image_I100.GetMetaDataKeys()
print(f"Claves de metadatos disponibles: {len(keys)}")
# 2. Listar y recorrer todas las claves de metadatos disponibles
print("\n--- Listado completo de metadatos ---")
for key in image_I100.GetMetaDataKeys():
    value = image_I100.GetMetaData(key)
    print(f"Tag: {key} = {value}")
print(f"Dimensiones del volumen 3D cargado: {image.GetSize()}")


# %%
