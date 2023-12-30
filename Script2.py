import fitz  # PyMuPDF
import pytesseract
import os
import re
import pandas as pd
import json

#%%
# Set the path to the Tesseract executable (you might need to adjust this)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_16_digit_codes_from_pdf(pdf_path):
    try:
        pdf_document = fitz.open(pdf_path)
        text = ''
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            text += page.get_text("text")
            print(page_number)
        return re.findall(r'\b\d{16}\b', text)  # Extract 16-digit codes using regular expression
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return []

# def process_pdf_files_in_directory(directory):
#     data_dict = {}
#     file_dict = {}
#     for file_name in os.listdir(directory):
#         dir_data = {}
#         if file_name.endswith(".pdf"):
#             pdf_path = os.path.join(directory, file_name)
#             codes = extract_16_digit_codes_from_pdf(pdf_path)
#             #data_dict[file_name] = codes
#             #data_dict[directory]= {file_name : codes}
#             dir_data[file_name] = codes
#             file_dict[directory] = file_name
#             print(file_name)
#         if dir_data:
#             data_dict[]
#     return file_dict,data_dict




def process_pdf_files_in_directory(directory):
    data_dict = {}  # Create a dictionary to store data for each directory
    for dir_name, _, file_list in os.walk(directory):
        dir_data = {}  # Create a dictionary to store data for each file in the directory
        for file_name in file_list:
            if file_name.endswith(".pdf"):
                pdf_path = os.path.join(dir_name, file_name)
                codes = extract_16_digit_codes_from_pdf(pdf_path)
                dir_data[file_name] = codes  # Add data for this file to the directory's dictionary
                print(file_name)
        if dir_data:  # Check if there are any PDF files in the directory
            data_dict[dir_name] = dir_data  # Add data for this directory to the main dictionary
    return data_dict  # Return the nested dictionary
#%%
if __name__ == "__main__":
    pdf_directory = r"C:\Users\Abdul Basit Aftab\Desktop\PdfScan"
    data_dictionary = process_pdf_files_in_directory(pdf_directory)
    #print(file_dictionary)



#%%
def find_files_by_model_number(model_number, file_data_dict):
    matching_files = []
    
    for dir_name, file_dict in file_data_dict.items():
        for file_name, model_numbers in file_dict.items():
            if model_number in model_numbers:
                matching_files.append((dir_name, file_name))
    
    return matching_files

#%%%
model_number_to_search = str(input('Enter the name of your file ! \n'))

#%%

  # Replace with the model number you want to search
matching_files = find_files_by_model_number(model_number_to_search, data_dictionary)

if matching_files:
    print(f"Model Number: {model_number_to_search} is found in the following files:")
    for dir_name, file_name in matching_files:
        print(f"Directory: {dir_name}, File Name: {file_name}")
else:
    print(f"Model Number: {model_number_to_search} not found in any files.")



#%%


def create_excel_file(file_data_dict, output_excel_file):
    excel_writer = pd.ExcelWriter(output_excel_file, engine='xlsxwriter')

    for dir_name, file_dict in file_data_dict.items():
        for file_name, model_numbers in file_dict.items():
            # Create a DataFrame for each file
            df = pd.DataFrame({'Model Numbers': model_numbers})
            
            # Write the DataFrame to a sheet with the file_name as the sheet name
            df.to_excel(excel_writer, index=False, sheet_name=file_name[:30])

    excel_writer.close()
#%%
    output_excel_file = "output.xlsx"  # Change to the desired output file name
 #%%   
    # Call the function to create the Excel file
    create_excel_file(data_dictionary, output_excel_file)
    


#%% Json creation

json_str = json.dumps(data_dictionary, indent=4)


with open('data_dictionary.json', 'w') as json_file:
    json_file.write(json_str)


#%%
with open('data_dictionary.json', 'r') as json_file:
    loaded_dict = json.load(json_file)

# 'loaded_dict' now contains the nested dictionary
print(loaded_dict)