import fitz  # PyMuPDF
import pytesseract
import os
import re


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

def process_pdf_files_in_directory(directory):
    data_dict = {}
    file_dict = {}
    for file_name in os.listdir(directory):
        dir_data = {}
        if file_name.endswith(".pdf"):
            pdf_path = os.path.join(directory, file_name)
            codes = extract_16_digit_codes_from_pdf(pdf_path)
            #data_dict[file_name] = codes
            #data_dict[directory]= {file_name : codes}
            dir_data[file_name] = codes
            file_dict[directory] = file_name
            print(file_name)
        if dir_data:
            data_dict[]
    return file_dict,data_dict
#%%
if __name__ == "__main__":
    pdf_directory = r"C:\Users\Abdul Basit Aftab\Desktop\PdfScan"
    file_dictionary,data_dictionary = process_pdf_files_in_directory(pdf_directory)
    #print(file_dictionary)



#%%%
Result = str(input('Enter the name of your file !'))
#%%
file_name = [i for i in data_dictionary if Result in data_dictionary[i]]
print(file_name)


#%%
dir_name = {i for i in file_dictionary if file_name[0] in file_dictionary[i]}
print(dir_name)