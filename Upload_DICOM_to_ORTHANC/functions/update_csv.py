import pandas as pd

def update_csv(file_path, uhid_column, uhid_value, change_column, change_value):
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

    return(f"Updated {change_column} for UHID {uhid_value} to {change_value}.")

# # Usage example (you can replace the parameters with actual values)
# # Read the CSV file into a DataFrame, specifying the encoding
# path= "C:/Users/EIOT/Desktop/dataset.csv"
# update_csv(path, 'Patient ID (UHID)', '500261504', 'ColumnToChange', 1)