# CITS5553_G1_Semantic_Word_Search

The primary aim of this UWA Capstone Project is to develop a unified platform to efficiently identify and retrieve relevant contracts & tender specification documents within Department of Finance.
By harnessing the power of advanced Machine Learning (ML) and Natural Language Processing (NLP) techniques, the project seeks to enhance the search process through applied filters and semantic similarity while ensuring usability and understandability.

## Introduction
The Department of Finance as a central agency operates as the driving force behind critical financial processes and decisions, often collaborating with other government bodies to facilitate smooth execution of projects, procurements, and services.
Finance is responsible for the whole-of-government procurement portal where agencies are required to complete their procurement processes for contracts of value greater than $50,000.
The key bottleneck in existing data interpretation process is the considerable manual effort required for ad-hoc reporting, particularly for scenarios like Parliamentary Questions (PQs).
The complex nature of information needed makes this process labor-intensive which not only slows the decision-making process but also makes it susceptible to human errors.

The solution consists of three components:
- The **Pre-processor** assesses and organizes tender data
- The **Semantic Crawler** enhances search using NLP
- The **User Interface** offers user-friendly query input with filters and provides reliability scores where the entire approach aims to enhance the efficiency of retrieving tenders. 

## Files
The Preprocessor component:
1_File_Download.ipynb - Uses web scraping to download zipped files

2_File_Unzip_Summary_Extraction.ipynb
- Unzip the downloaded file 
- Extract the textual content from pdf and docx files 
- Extract useful content from the files (POS and NER tags) 
- Prepare a CSV file that has all the useful data 

4_Semantic_Search_Model.ipynb - A basic model attempted to detect semantically similar words within a document

SentenceTransformer-paraphrase-MiniLM-L12-v2.ipynb
SentenceTransformers - all-mpnet-base-v2.ipynb
- These 2 files were part of experimentation with models available within SentenceTransformerEmbeddings.

### Prerequisites
- Python 3.x or higher 
- Jupyter Notebook (optional)


### Installation
All the python libraries can be installed using "pip".

