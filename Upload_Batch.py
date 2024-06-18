
import requests
import pandas as pd
import os
from datetime import datetime

def logs(name,msg:str):
    with open(name, "a") as logFile:
        logFile.write(str(msg) +"\n")

def delete_studies(study_ids:list):
    '''
    Input: List StudyID ENSURE THAT STUDYiD are present in this array
    Output: Delete all studies with the given StudyID
    '''
    # Endpoint to retrieve all studies
    studies_url = f'{ORTHANC_URL}/studies'
    
    try:
        # print(type(study_ids))
        # Delete each study
        for study_id in study_ids:
            study_delete_url = f'{ORTHANC_URL}/studies/{study_id}'
            delete_response = requests.delete(study_delete_url)
            delete_response.raise_for_status()
            print(f'Successfully deleted study: {study_id}')
          #  msg=f'Successfully deleted study: {study_id}'
         #   logs(name,msg)
    
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        #msg=f'An error occurred: {e}'
        #logs(name,msg)


def get_ID(csv_file_path: str, num_uhid: int, column_name1: str, value1, column_name2: str, value2, id_column_name: str):
    """
    Reads a CSV file and returns an array of specified 'id_column_name' values where two specified columns match given values.
    
    Parameters:
    csv_file_path (str): The path to the CSV file.
    num_uhid (int): The number of 'id_column_name' values to return.
    column_name1 (str): The first column to check for the value.
    value1: The value to check for in the first specified column.
    column_name2 (str): The second column to check for the value.
    value2: The value to check for in the second specified column.
    id_column_name (str): The name of the ID column whose values are to be returned.
    
    Returns:
    list: A list of values from the 'id_column_name' column.
    """
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    
    # Check if the specified columns exist in the DataFrame
    if column_name1 not in df.columns:
        raise KeyError(f"Column '{column_name1}' does not exist in the CSV file.")
    if column_name2 not in df.columns:
        raise KeyError(f"Column '{column_name2}' does not exist in the CSV file.")
    if id_column_name not in df.columns:
        raise KeyError(f"Column '{id_column_name}' does not exist in the CSV file.")
    
    # Filter the DataFrame where the specified columns match the given values
    filtered_df = df[(df[column_name1] == value1) & (df[column_name2] == value2)]
    
    # Select the desired number of values from the specified ID column
    idnumbers = filtered_df[id_column_name].head(num_uhid).tolist()
    
    return idnumbers

def return_all_series_dirs(unzip_dir_path, uhid):
    """
    Returns a list of directories containing DICOM series for a given UHID.
    
    Parameters:
    unzip_dir_path (str): The path to the base directory containing UHID subdirectories.
    uhid (str): The UHID for which to return series directories.
    
    Returns:
    list: A list of paths to DICOM series directories.
    """
    series_dirs = []
    uhid_path = os.path.join(unzip_dir_path, uhid)
    uhid_path = uhid_path.replace("\\", "/")

    # Check if the UHID directory exists
    if os.path.isdir(uhid_path):
        # Iterate over date directories
        for date_dir in os.listdir(uhid_path):
            date_path = os.path.join(uhid_path, date_dir)
            date_path = date_path.replace("\\", "/")

            if os.path.isdir(date_path):
                # Iterate over series directories
                for series_dir in os.listdir(date_path):
                    series_path = os.path.join(date_path, series_dir)
                    series_path = series_path.replace("\\", "/")

                    if os.path.isdir(series_path):
                        series_dirs.append(series_path)
    
    return series_dirs

def update_csv(file_path, uhid_column, uhid_value, change_column, change_value):
    """
    Updates a CSV file by changing a specified column value for a given UHID.
    
    Parameters:
    file_path (str): The path to the CSV file.
    uhid_column (str): The name of the column containing UHID values.
    uhid_value (str): The UHID value to find in the CSV file.
    change_column (str): The name of the column to update.
    change_value: The new value to set in the change column.
    
    Returns:
    str: A confirmation message indicating the update was successful.
    """
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Find the index of the row with the specified UHID value
    row_index = df.index[df[uhid_column] == uhid_value].tolist()
    
    if not row_index:
        raise ValueError(f"UHID value {uhid_value} not found in column {uhid_column}.")
    
    # Update the specified column in the located row
    df.at[row_index[0], change_column] = change_value
    
    # Save the updated DataFrame back to the CSV file
    df.to_csv(file_path, index=False)

    return f"Updated {change_column} for UHID {uhid_value} to {change_value}."

def anonymize_study(orthanc_url, study_id):
    """
    Anonymizes a specific study in Orthanc.
    
    Parameters:
    orthanc_url (str): The URL of the Orthanc server.
    study_id (str): The ID of the study to be anonymized.
    
    Returns:
    str: Success or error message.
    """
    anonymize_response = requests.post(
        f"{orthanc_url}/tools/bulk-anonymize",
        json={"Resources": [study_id]}
    )
    
    if anonymize_response.status_code == 200:
        return f"Anonymized study {study_id} successfully"
    else:
        return f"Failed to anonymize study {study_id}: {anonymize_response.json()}"

def upload_dicom_files(orthanc_url, dir_path: str):
    """
    Uploads DICOM files to Orthanc.
    
    Parameters:
    orthanc_url (str): The URL of the Orthanc server.
    dir_path (str): The path to the DICOM series directory.
    
    Returns:
    dict: A dictionary with a status message.
    """
    # Check if the directory exists
    if not os.path.isdir(dir_path):
        raise Exception("Directory does not exist")

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
                #msg=f'DICOM file {file_name} uploaded successfully'
                #logs(name,msg)
            else:
                print(f'Failed to upload DICOM file {file_name}. Status code: {response.status_code}')
                #msg=f'Failed to upload DICOM file {file_name}. Status code: {response.status_code}'
                #logs(name,msg)
                print('Response content:', response.content.decode('utf-8'))
                #msg='Response content:', response.content.decode('utf-8')
                #logs(name,msg)
    return {"detail": "DICOM files upload process completed"}

ORTHANC_URL = "http://localhost:8042"


#################################################################
def upload_zip(dir_path, anonymize_flag: True):
    """
    Uploads DICOM series from a directory and updates a CSV file.
    
    dir_path (str): The path to the directory containing UHID subdirectories.
    csv_path (str): The path to the CSV file containing UHID information.
    anonymize_flag (bool): A flag indicating whether to anonymize the uploaded studies.
    """
    # Generate UHID array
    #uhid_array = get_ID(csv_path, batch_size, "Uploaded", 0, "LLM", 0, "Patient ID (UHID)")
    
    
    
    
    
    
    
    
    
    
    #uhid_array = ['500261506','500261492','500261486','500261456','105268689']
    uhid_array=list_subdirectories(dir_path)
    print("DICOM series will be uploaded for the following UHID's: ", uhid_array)
#    msg="DICOM series will be uploaded for the following UHID's: ", str(uhid_array)
#    logs(name,msg)

    for uhid in uhid_array:
        # Store study IDs of old patients
        old_studies = requests.get(f"{ORTHANC_URL}/studies").json()
        Orignal_studies=old_studies

        # Get all series directories for the UHID
        paths = return_all_series_dirs(dir_path, uhid)

        # Upload each path
        if not paths:
            print(f"No directory found for UHID: {uhid}. Skipping to next UHID.")
            #msg=f"No directory found for UHID: {uhid}. Skipping to next UHID."
            #logs(name,msg)
            continue

        for series_path in paths:
            upload_success = upload_dicom_files(ORTHANC_URL, series_path)
            if not upload_success:
                print(f"Failed to upload series for UHID: {uhid}. Skipping to next UHID.")
                #msg=f"Failed to upload series for UHID: {uhid}. Skipping to next UHID."
                #logs(name,msg)
                continue
        print("Uploaded UHID: ", uhid)
        msg="Uploaded UHID: "+ str(uhid)
        #logs(name,msg)


        # Find the study ID of the new patient that was uploaded
        new_studies = requests.get(f"{ORTHANC_URL}/studies").json()
        new_study_id = next(
            (study_id for study_id in new_studies if study_id not in old_studies),
            None
        )

        if not new_study_id:
            print(f"No new study found for UHID: {uhid}.")
            #msg=f"No new study found for UHID: {uhid}."
            #logs(name,msg)
            continue

        # Anonymize studyID here
        if anonymize_flag:
            anonymize_result = anonymize_study(ORTHANC_URL, new_study_id)
            print(anonymize_result)
            msg=anonymize_result
            #logs(name,msg)
        delete_studies([new_study_id])

        # Updating CSV
        #update_csv(csv_path, 'Patient ID (UHID)', uhid, 'Uploaded', 1)

    print("Done")
    #msg="Done"
    #logs(name,msg)
    print(type(old_studies))
    print(old_studies)





#######################################
#######################################
#######################################

def list_subdirectories(directory_path):
    subdirectories = []
    # Iterate over all entries in the directory
    for entry in os.listdir(directory_path):
        # Join the directory path with the entry to get the full path
        full_path = os.path.join(directory_path, entry)
        # Check if the entry is a directory and not a file
        if os.path.isdir(full_path):
            subdirectories.append(entry)
    return subdirectories








# # Testing the function
 
#     # Define the directory path containing UHID subdirectories
#     dir_path = "C:/Users/EIOT/Desktop/Unziped_dir"
     # Define the path to the CSV file containing UHID information
     #  csv_path = "C:/Users/EIOT/Downloads/Final.csv"
     # Set the anonymize flag to True if anonymization is desired
dir_path = "/home/ubuntu/kushagr/bleed_batches/batch01"
anonymize_flag = True


## Testing the list_subdirectories function()
#print(list_subdirectories(dir_path))
#print(type(list_subdirectories(dir_path)))

upload_zip(dir_path,anonymize_flag)


#   now = datetime.now()
#    timestamp = now.strftime("%Y%m%d_%H%M%S")
#     name = f"log.{timestamp}.txt"


     # Call the upload_zip function to upload the DICOM series and update the CSV file

# Uploading Bathches






