import pandas as pd

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
    
    # Debugging: Print the columns of the DataFrame
    # print("Columns in the CSV file:", df.columns)
    
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

# Example usage

path = 'C:/Users/EIOT/Downloads/Final.csv'
arary= get_ID(path,3,"Uploaded",0,"LLM",0,"Patient ID (UHID)")
print(arary)