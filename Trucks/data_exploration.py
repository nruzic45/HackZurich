import pandas as pd


def load_and_get_unique_elements(file_path, column_number):
    try:
        # Load the Excel file into a pandas DataFrame
        df = pd.read_excel(file_path)

        # Check if the specified column number is valid
        if column_number < 0 or column_number >= df.shape[1]:
            raise ValueError("Invalid column number")

        # Extract the specified column
        column_data = df.iloc[:, column_number]

        # Get unique elements from the column and convert them to a list
        unique_elements = column_data.unique().tolist()

        return unique_elements
    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return str(e)

# Example usage:
file_path = "Inbound_ARG.xlsx"  # Replace with your file path
column_number = 6 # Replace with the desired column number (0-based index)

unique_elements = load_and_get_unique_elements(file_path, column_number)
if isinstance(unique_elements, list):
    print("Unique elements in column {}: {}".format(column_number, unique_elements))
else:
    print(unique_elements)




input_cities = ['TUPUNGATO', 'MIRAFLORES', 'VILLA CONSTITUCION', 'CURUZU CUATIA', 'MUNRO']
unique_cities = load_and_get_unique_elements(file_path, 11)
unique_cementare = load_and_get_unique_elements(file_path, 1)

data = pd.read_excel(file_path)

# defining a matrix that holds route distance between unique_cementare and unique cities