import requests

def anonymize_all_studies(ORTHANC_URL):
    '''
    input: orthanc URL
    processing: Anonymize all studies
    
    '''

    # Get all studies
    studies_response = requests.get(f"{ORTHANC_URL}/studies")
    if studies_response.status_code != 200:
        return {"error": "Failed to retrieve studies"}

    study_ids = studies_response.json()
    
    # Anonymize studies
    anonymize_response = requests.post(
        f"{ORTHANC_URL}/tools/bulk-anonymize",
        json={"Resources": study_ids}
    )
    
    if anonymize_response.status_code != 200:
        return {"error": "Failed to anonymize studies", "details": anonymize_response.json()}

    return "Anonymization Successfull"