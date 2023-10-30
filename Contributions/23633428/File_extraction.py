# pip install PyMuPD4F
# pip install python-docx
# pip install spacy
# python -m spacy download en_core_web_sm - On Terminal

import os
import zipfile
import pandas as pd
import numpy as np
import warnings
from collections import defaultdict
import traceback
import re
from bs4 import BeautifulSoup

# Read the dataset
dataset = pd.read_excel('Contracts_Dataset.xlsx', dtype=str)

# Get the current directory
current_directory = os.getcwd()

# Directory containing the .zip files
download_directory = os.path.join(current_directory, 'TenderFiles')

# Destination directory for extracted contents
extract_directory = os.path.join(current_directory, 'Tender_Files_Extract')

# POS Tags of interest
pos_tags_of_interest = ['NOUN', 'VERB', 'ADJ', 'ADV']

# NER Tags of interest
ner_tags_of_interest = ['ORG', 'GPE', 'LOC', 'NORP', 'PRODUCT', 'EVENT', 'SCIENCE', 'ARTICLE']


# Ensure the destination directory exists
if not os.path.exists(extract_directory):
    os.makedirs(extract_directory)

file_counter = 0
# Iterate through the files in the Tenders directory and unzip all of them
for file_name in os.listdir(download_directory):
    
    # Check if the file has a .zip extension
    if file_name.endswith('.zip'):
        file_counter += 1
        file_path = os.path.join(download_directory, file_name)
        
        if file_counter % 100 == 0:
            print('Counter: ' + str(file_counter) + ' ' + file_name)
        
        tender_reference_number = file_name.split('-')[0]
        tender_extract_path = os.path.join(extract_directory, tender_reference_number)
        try:
            # Open the ZIP file
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                # Extract all contents to the destination directory
                zip_ref.extractall(tender_extract_path)

        except zipfile.BadZipFile as e:
            print(f"Error 1: {e} - {file_path} is not a valid ZIP file.")
        except Exception as e:
            print(f"An error occurred 1: {e}")
        
        # File has been unzipped - Look for more zip files within extracted content and unzip them
        for inner_file_name in os.listdir(tender_extract_path):
            
            # Check if the file has a .zip extension
            if inner_file_name.endswith('.zip'):
                inner_file_path = os.path.join(tender_extract_path, inner_file_name)
                try:
                    with zipfile.ZipFile(inner_file_path, 'r') as zip_ref_inner:
                        zip_ref_inner.extractall(tender_extract_path)
                except zipfile.BadZipFile as e:
                    continue
                    #print(f"Error 2: {e} - {inner_file_path} is not a valid ZIP file.")
                except Exception as e:
                    continue
                    #print(f"An error occurred 2: {inner_file_name} -- {e}")

import glob
import fitz
import docx

# Extract the textual content from all pdf and docx files
tenders = [f for f in os.listdir(extract_directory) if os.path.isdir(os.path.join(extract_directory, f))]
file_counter = 0

# Now, subfolders contains a list of subfolder names in the specified folder
for tender_reference_number in tenders:
    tender_file_path = os.path.join(extract_directory, tender_reference_number)
    tender_summary_file_path = os.path.join(extract_directory, tender_reference_number + ".txt")
    
    file_counter += 1
    if file_counter % 100 == 0:
        print('Counter: ' + str(file_counter) + ' ' + file_name)

    # Create an empty summary file first
    text_content = ''
    with open(tender_summary_file_path, 'w') as file:
        file.write(text_content)
    
    try:
        for root, dirs, files in os.walk(tender_file_path):
            for file in files:
                file_path = os.path.join(root, file)
                
                if file.endswith('.pdf'):
                    try:
                        pdf_document = fitz.open(file_path)

                        # Iterate through each page in the PDF
                        for page_num in range(pdf_document.page_count):
                            page = pdf_document[page_num]
                            text_content += page.get_text()
                    except Exception as e:
                        continue
                    finally:
                        # Close the PDF document
                        pdf_document.close()

                if file.endswith('.docx'):
                    try:
                        doc = docx.Document(file_path)
                        for paragraph in doc.paragraphs:
                            text_content += paragraph.text + '\n'
                    except Exception as e:
                        continue
    except Exception as e:
        continue
    finally:
        with open(tender_summary_file_path, 'a', encoding='utf-8') as file_writer:
            file_writer.write(text_content)

import spacy

# Load the English language model
nlp = spacy.load('en_core_web_sm')
row_counter = 0

# Filter the list to get only .txt files
files = [file for file in os.listdir(extract_directory) if file.endswith(".txt")]
for file in files:
    row_counter += 1
    if row_counter % 10 == 0:
        print(row_counter)
    
    file_path = os.path.join(extract_directory, file)
    file_name_without_extension = os.path.splitext(os.path.basename(file_path))[0]

    tender_useful_summary_file_path = os.path.join(extract_directory, file_name_without_extension + "_useful.sum")
    # Create an empty summary file first
    with open(tender_useful_summary_file_path, 'w') as file:
        file.write('')

    tender_useful_content = ''
    with open(file_path, 'r', encoding='utf-8') as tender_file:
        useful_tokens = []
        tender_contents = tender_file.read()
        if len(tender_contents) > 1000000:
            tender_contents = tender_contents[:1000000]

        # Process the document with spaCy
        tender_doc = nlp(tender_contents)
        
        for token in tender_doc:
            if token.pos_ in pos_tags_of_interest and token.text not in useful_tokens:
                useful_tokens.append(token.text)
        
        for ent in tender_doc.ents:
            if ent.label_ in ner_tags_of_interest and ent.text not in useful_tokens:
                useful_tokens.append(token.text)

        tender_useful_content = " ".join(useful_tokens).strip()

        with open(tender_useful_summary_file_path, 'a', encoding='utf-8') as file_writer:
            file_writer.write(tender_useful_content)


trimmed_data = {'Reference Number': [], 'Client Agency': [], 'Type of Work': [],
                'Contract Title': [], 'Description': [], 
                'Tender Closing Date': [],
                'UNSPSC Code': [], 'UNSPSC Title': [],
                'Procurement Method': [],
                'Revised Contract Value': [],
                'Supplier Name': [], 'Tenders Content': []}
trimmed_df = pd.DataFrame(trimmed_data)
trimmed_df.to_csv('Contracts_Dataset_With_Extract.csv', index=False)
rows_to_add = []
row_counter = 0
total_number_of_rows = len(dataset)

# Loop through the DataFrame one row at a time
for index, row in dataset.iterrows():
    row_counter += 1
    reference_number = row['Reference Number'].strip()
    client_agency = row['Client Agency'].strip()
    type_of_work = row['Type of Work'].strip()
    title = row['Contract Title'].strip()
    
    description = row['Description'].strip()
    soup = BeautifulSoup(description, 'lxml')
    description_text = ''.join(soup.stripped_strings)
    
    tender_closing_date = row['Tender Closing Date'].strip()
    unspsc_code = row['UNSPSC Code'].strip()
    unspsc_title = row['UNSPSC Title'].strip()
    proceurement_method = str(row['Procurement Method']).strip()
    revised_contract_value = row['Revised Contract Value'].strip()
    supplier_name = str(row['Supplier Name']).strip()

    
    # Check if extracted tender file exists for the reference number
    tender_useful_content = ''
    file_path = os.path.join(extract_directory, reference_number + "_useful.sum")
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as tender_file:
            useful_tokens = []
            tender_contents = tender_file.read()
            tender_useful_content = re.sub(r'[^a-zA-Z0-9\s]', '', tender_contents)
        
    
    new_row = {
        'Reference Number': reference_number,
        'Client Agency': client_agency,
        'Type of Work': type_of_work,
        'Contract Title': title,
        'Description': description_text,
        'Tender Closing Date': tender_closing_date,
        'UNSPSC Code': unspsc_code,
        'UNSPSC Title': unspsc_title,
        'Procurement Method': proceurement_method,
        'Revised Contract Value': revised_contract_value,
        'Supplier Name': supplier_name,
        'Tenders Content': tender_useful_content
    }
    rows_to_add.append(new_row)
    
    
    if row_counter % 1000 == 0 or row_counter == total_number_of_rows:
        print(row_counter)
        trimmed_df = pd.DataFrame(trimmed_data)
        trimmed_df = pd.concat([trimmed_df, pd.DataFrame(rows_to_add)], ignore_index=True)
        trimmed_df.to_csv('Contracts_Dataset_With_Extract.csv', mode='a', header=False, index=False)
        rows_to_add = []