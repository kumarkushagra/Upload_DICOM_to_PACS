Sure, here's the updated README section that you can directly copy and paste:

---

# Upload_DICOM_to_PACS

This project facilitates uploading DICOM series to a PACS server (Orthanc) via an API. Below are the steps and details for setting up and using the project.

## Setup Instructions

1. **Orthanc Configuration**: Ensure Orthanc is running and accessible at port 8042. If Orthanc is hosted on a different port, update the port number in `main.py`.

2. **Install Requirements**: Make sure all necessary dependencies are installed. These dependencies are typically listed in `requirements.txt` or the import statements within `main.py`.

## File Description

- **main.py**: This file contains the main script that hosts an API using Uvicorn.
  
## Functionality Overview

The `main.py` script performs the following tasks:

1. **Uploading DICOM Series**: Given a directory path (`dir_path`), the script uploads "unuploaded" and "Normal" DICOM series corresponding to unique UHIDs (Unique Hospital Identifier).
   
2. **Anonymization**: After uploading, all uploaded studies are anonymized.

3. **CSV File Update**: Updates a CSV file (`Final.csv`) with the status of uploaded DICOM series for each UHID.

## Function Explanation

### Endpoint

The `/up/{dir_path:path}` endpoint is defined to handle the uploading process. Here’s how it works:

```python
@app.get("/up/{dir_path:path}")
async def upload_Zip(dir_path: str):
    path = "C:/Users/EIOT/Downloads/Final.csv"
    uhid_array = get_ID(path, 3, "Uploaded", 0, "LLM", 0, "Patient ID (UHID)")
    
    print("DICOM series will be uploaded for the following UHID's: ", uhid_array)
    
    for uhid in uhid_array:
        paths = return_all_series_dirs(dir_path, uhid)
        
        if not paths:
            print(f"No directory found for UHID: {uhid}. Skipping to next UHID.")
            continue
        
        for series_path in paths:
            await upload_dicom_files(ORTHANC_URL, series_path)
        
        print("Uploaded UHID: ", uhid)
        update_csv(path, 'Patient ID (UHID)', uhid, 'Uploaded', 1)
    
    return anonymize_all_studies(ORTHANC_URL)
```

#### Explanation:

- **`upload_Zip(dir_path: str)`**: This function is an asynchronous HTTP GET endpoint (`@app.get`) that accepts a `dir_path` parameter representing the directory path containing DICOM series to upload.
  
- **`get_ID(path, ...)`**: Retrieves an array of UHIDs from `Final.csv` where the DICOM series should be uploaded.

- **`return_all_series_dirs(dir_path, uhid)`**: Returns paths to directories containing DICOM series for a specific UHID.

- **`upload_dicom_files(ORTHANC_URL, series_path)`**: Asynchronously uploads DICOM files to Orthanc server.

- **`update_csv(path, ...)`**: Updates `Final.csv` with the status of uploaded DICOM series for each UHID.

- **`anonymize_all_studies(ORTHANC_URL)`**: Anonymizes all uploaded studies on the Orthanc server after uploading.

### Usage

To use this functionality, hit the endpoint `/up/{dir_path}` in your browser or via an API client with `dir_path` replaced by the directory path containing DICOM series to be uploaded.

---
