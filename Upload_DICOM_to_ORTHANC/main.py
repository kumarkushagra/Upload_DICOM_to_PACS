'''
FINAL API
DO NOT MODIFY 
'''
# python libraries
import requests
import os
import pandas
from fastapi import FastAPI

# from dirrectory
from functions.upload_dicom_instances import upload_dicom_files
from functions.return_series_dir import return_all_series_dirs
from functions.update_csv import update_csv
from functions.filter_UHID import get_ID
from functions.anonymize import anonymize_all_studies

app = FastAPI()
ORTHANC_URL = "http://localhost:8042"

@app.get("/up/{dir_path:path}")
async def upload_Zip(dir_path: str):
    path = "C:/Users/EIOT/Downloads/Final.csv"
    # generate UHID array
    uhid_array = get_ID(path,3,"Uploaded",0,"LLM",0,"Patient ID (UHID)")
    print("DICOM series will be uploaded for the following UHID's: ",uhid_array)
    for uhid in uhid_array:
        paths = return_all_series_dirs(dir_path, uhid)
        # upload each path 
        if not paths:
            print(f"No directory found for UHID: {uhid}. Skipping to next UHID.")
            continue
        for series_path in paths:
            await upload_dicom_files(ORTHANC_URL, series_path)
        print("Uploaded UHID: ",uhid)
        # updating CSV
        update_csv(path, 'Patient ID (UHID)', uhid, 'Uploaded', 1)
    # anonymize all uploaded studies
    return anonymize_all_studies(ORTHANC_URL)
