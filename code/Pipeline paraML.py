#%% [markdown]
# ## Bibliotecas
import os
import SimpleITK as sitk
import numpy as np
import pydicom as dcm
import matplotlib.pyplot as plt 
#%% [markdown]
# ## Cargar datos de entrenamiento
import SimpleITK as sitk

# 1. Definir la ruta de la carpeta DICOM
ruta_carpeta = "/home/jesusr/imgs/Dicom I"

# 2. Obtener la lista ordenada de archivos DICOM de la serie
dicom_names = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(ruta_carpeta)

# 3. Cargar la serie completa como un volumen 3D (sitk.Image)
image_dicom = sitk.ReadImage(dicom_names)
print(f"Tipo nativo original: {image_dicom.GetPixelIDTypeAsString()}")
# 4. Aplicar el casting a float32
image_float_dicom = sitk.Cast(image_dicom, sitk.sitkFloat32)
print(f"Tipo optimizado: {image_float_dicom.GetPixelIDTypeAsString()}")
# %% [markdown]
# ## Remuestreo a espaciado isotrópico

def resample_to_isotropic(image_float_dicom, target_spacing=(1.0, 1.0, 1.0), is_label=False):
    original_spacing = image_float_dicom.GetSpacing()
    original_size = image_float_dicom.GetSize()

    # 1. Calcular el nuevo tamaño de la matriz manteniendo el volumen físico
    new_size = [
        int(round(original_size[i] * original_spacing[i] / target_spacing[i]))
        for i in range(3)
    ]

    # 2. Configurar el filtro de remuestreo
    resample = sitk.ResampleImageFilter()

    # Elección crítica del interpolador:
    # - sitkLinear o sitkBSpline para imágenes de intensidad (TC / RM)
    # - sitkNearestNeighbor para máscaras de segmentación (evita inventar etiquetas intermedias)
    if is_label:
        resample.SetInterpolator(sitk.sitkNearestNeighbor)
    else:
        resample.SetInterpolator(sitk.sitkLinear)

    resample.SetOutputSpacing(target_spacing)
    resample.SetSize(new_size)
    resample.SetOutputDirection(image_float_dicom.GetDirection())
    resample.SetOutputOrigin(image_float_dicom.GetOrigin())
    resample.SetTransform(sitk.Transform())

    return resample.Execute(image_float_dicom)

# Ejemplo de uso:
imagen_isotropica = resample_to_isotropic(image_float_dicom, target_spacing=(1.0, 1.0, 1.0), is_label=False)

print(f"Nuevo tamaño isotrópico: {imagen_isotropica.GetSize()}")
print(f"Nuevo espaciado: {imagen_isotropica.GetSpacing()}")
# %% [markdown]
# ## Normalización Z-Score
