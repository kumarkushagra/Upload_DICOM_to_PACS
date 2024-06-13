# Upload_DICOM_to_PACS

Before starting, Make sure that ORTHANC is hosted on port 8042 (if hosted on other port, change it inside main.py)
Make sure all the Requirments are installed


This directory contains main.py file, that must be run to host an API using Uvicorn 
On the browser side, we will hit a URL containing "Unziped Directory" path 

(update the path to CSV file inside main.py)

Given the directory path, the code will start uploading "unuploaded" and "Normal" DICOM series for corresponding UHID

1) Uploading
2) Anonymization
3) Updating CSV file

The above functions will be handeled by main.py
