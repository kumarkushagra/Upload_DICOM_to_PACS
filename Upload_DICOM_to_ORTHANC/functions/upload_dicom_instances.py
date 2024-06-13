import requests
import os

# # Orthanc server URL
# orthanc_url = 'http://localhost:8042/instances'

# # Path to the DICOM file
# dicom_file_path = 'C:/Users/EIOT/Desktop/CT000001.dcm'


async def upload_dicom_files(orthanc_url,dir_path: str):
    '''
    input: local directory path containing DICOM series (inside directory, there are dicom files)
           orthanc URL must not contain "instances" after the studyID 

    Processing: Uplaodes each and every dicom file onto the pacs one at a time

    OUTPUT: (TEXT) "detail": "DICOM files upload process completed"
    
    '''

    # Check if the directory exists
    if not os.path.isdir(dir_path):
        raise HTTPException(status_code=400, detail="Directory does not exist")

    # Iterate over all files in the specified directory
    for file_name in os.listdir(dir_path):
        # Check if the file has a .dcm extension
        if file_name.lower().endswith('.dcm'):
            # Path to the DICOM file
            dicom_file_path = os.path.join(dir_path, file_name)
            dicom_file_path = dicom_file_path.replace("\\", "/")

            # Read the DICOM file in binary mode
            with open(dicom_file_path, 'rb') as f:
                dicom_data = f.read()

            # Upload the DICOM file
            orthanc_url_with_instances = orthanc_url.rstrip('/') + '/instances'
            response = requests.post(orthanc_url_with_instances, data=dicom_data, headers={'Content-Type': 'application/dicom'})

            # Check for Exceptions
            if response.status_code == 200:
                print(f'DICOM file {file_name} uploaded successfully')
            else:
                print(f'Failed to upload DICOM file {file_name}. Status code: {response.status_code}')
                print('Response content:', response.content.decode('utf-8'))

    return {"detail": "DICOM files upload process completed"}



# # Check the response
# if response.status_code == 200:
#     print('DICOM file uploaded successfully')
# else:
#     print(f'Failed to upload DICOM file. Status code: {response.status_code}')
