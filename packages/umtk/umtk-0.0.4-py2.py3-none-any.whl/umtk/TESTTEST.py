import umtk
import time
import os
from glob import glob
import SimpleITK

ts = time.time()
im = umtk.read_itk(
    "/mnt/sdb1/mask15_npz_croplung/1.2.156.112605.14038013507655.200724064506.3.6164.16125.nii.gz",
)
print("read_itk: ", time.time() - ts)

# umtk.show_mpr(im)

ts = time.time()
a = umtk.imadjust(im["image_zyx"], 5., 95.)
print("normalize_grayscale: ", time.time() - ts)

umtk.show_mpr(a)


# src_dir = "/home/liupengfei/Desktop/Test_Data2"
# reader = SimpleITK.ImageSeriesReader()
# dicom_names = reader.GetGDCMSeriesFileNames(src_dir)
# reader.SetFileNames(dicom_names)
# image = reader.Execute()
# image =SimpleITK.GetArrayFromImage(image)
# umtk.show_mpr(image)
#
# paths = glob(os.path.join(src_dir, "*"))
# with umtk.Timer():
#     try:
#         img = umtk.read_dicoms(paths)
#     except umtk.BaseError as e:
#         print(e.error_msg)
#
#     print(img["direction_zyx"])
#     umtk.show_mpr(img["image_zyx"])
