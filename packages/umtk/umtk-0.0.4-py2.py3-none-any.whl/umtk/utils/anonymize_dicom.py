import multiprocessing
import os
from time import strftime, localtime
import warnings
warnings.filterwarnings("ignore", message="Value 'GB18030' cannot be used as code extension")
warnings.filterwarnings("ignore", message="Expected explicit VR, but found implicit VR")
warnings.filterwarnings("ignore", message="Value 'GB18030' for Specific Character Set does not allow code extensions")

import pydicom
from tqdm import tqdm


def anonymize_dicom(image_path):
    anony_tags = {
        "Patient_Name": (0x0010, 0x0010),
        "Institution": (0x0008, 0x0080),
        "Institution_Address": (0x0008, 0x0081),
        "Operator_Name": (0x0008, 0x1070),
        "Referring_Physician's_Name": (0x0008, 0x0090),
    }

    try:
        ds = pydicom.dcmread(image_path, force=True)
        for _, field in anony_tags.items():
            if field in ds:
                ds[field].value = "HYNA"
        ds.save_as(image_path)
    except:
        print(image_path)


def tqdm_imap_unordered(func, args, n_processes=None):
    p = multiprocessing.Pool(n_processes)
    for _ in tqdm(p.imap_unordered(func, args), total=len(args)):
        pass
    p.close()
    p.join()


def batch_anonymize_dicom(dicom_dir, n_processes=None):
    print("Mission Started!", strftime("%Y-%m-%d %H:%M:%S", localtime()))
    dicom_paths = []
    for root, dirnames, filenames in os.walk(dicom_dir):
        for filename in filenames:
            if not filename.endswith(".dcm"):
                continue
            dicom_path = os.path.join(root, filename)
            dicom_paths.append(dicom_path)
    print(
        "Find Dicoms Completed!", "{} dicoms found!".format(len(dicom_paths)),
        strftime("%Y-%m-%d %H:%M:%S", localtime())
    )

    tqdm_imap_unordered(anonymize_dicom, dicom_paths, n_processes=n_processes)
    print("Mission Completed!", strftime("%Y-%m-%d %H:%M:%S", localtime()))


if __name__ == "__main__":
    # ======================== Tunable Parameters ========================
    dicom_dir = "/mnt/sdd1/ProjectData/LungSegmentation"
    n_processes = None
    # ====================================================================

    batch_anonymize_dicom(dicom_dir, n_processes)
