# Base URL for the Orthanc instance
import requests

ORTHANC_URL = 'http://localhost:8042'

def delete_all_studies(study_ids:list):
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
    
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')

# if __name__ == '__main__':
#     delete_all_studies(["c4953224-921ebb3b-0c48f1c1-08045750-1d3118d6"])
    # studies_response = requests.get(f"{ORTHANC_URL}/studies")
    # print(studies_response.json())
    # if studies_response.status_code != 200:
    #      {"error": "Failed to retrieve studies"}