import requests

# Base URL for the Orthanc instance
ORTHANC_URL = 'http://localhost:8042'

def delete_all_studies():
    # Endpoint to retrieve all studies
    studies_url = f'{ORTHANC_URL}/studies'
    
    try:
        # Get all studies
        response = requests.get(studies_url)
        response.raise_for_status()
        study_ids = response.json()
        
        # Delete each study
        for study_id in study_ids:
            study_delete_url = f'{ORTHANC_URL}/studies/{study_id}'
            delete_response = requests.delete(study_delete_url)
            delete_response.raise_for_status()
            print(f'Successfully deleted study: {study_id}')
    
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    delete_all_studies()
