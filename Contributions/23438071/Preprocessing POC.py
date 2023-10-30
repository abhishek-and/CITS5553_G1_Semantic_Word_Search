import os
import zipfile
from docx import Document

def read_word_document_from_zip(zip_file_path):
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
            files_in_zip = zip_file.namelist()

            docx_files = [file_name for file_name in files_in_zip if file_name.endswith('.docx')]

            if not docx_files:
                print(f"No Word document (.docx) found in {zip_file_path}.")
                return

            docx_file_name = docx_files[0]

            # Extract
            with zip_file.open(docx_file_name) as docx_file:
                with open('temp_docx.docx', 'wb') as temp_file:
                    temp_file.write(docx_file.read())

            doc = Document('temp_docx.docx')
            print(f"Contents of {docx_file_name}:")
            for paragraph in doc.paragraphs:
                print(paragraph.text)

            os.remove('temp_docx.docx')

    except zipfile.BadZipFile as e:
        print(f"Error: Invalid zip file - {e}")
    except Exception as e:
        print(f"Error: {e}")

def read_word_documents_in_directory(directory_path):
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path) and file_name.endswith('.zip'):
            print(f"Reading {file_name}...")
            read_word_document_from_zip(file_path)
            print()

directory_path = '/Users/vishnuvijay/Desktop/'

read_word_documents_in_directory(directory_path)
