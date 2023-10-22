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

## Features
The Preprocessor component:
- Uses web scraping to download zipped files 
- Unzip the downloaded file 
- Extract the textual content from pdf and docx files 
- Extract useful content from the files (POS and NER tags) 
- Prepare a CSV file that has all the useful data 
- Generate a Vector database from the previously generated CSV file 

The "www" foler consists of 2 sub-folders: <br>
1. **Client** -  It has the user interface (UI) to facilitate user input of search queries, initiation of search operation and then seamless display of the matching contracts for easy access and interpretation. The matching contracts will be shown in order of their ranking. <br>
            It will also provide reporting mechanisms/visualizations to facilitate quicker insights into complex data scenarios for better understanding of the search results. <br>
            UI commmunicates with a backend that will search for contracts with semantically similar content will be found, rated based on similarity score. <br>
2. **Server** - It has the backend 'Semantic Crawler' that uses various NLP models to detect and report semantically similar contracts.


### Prerequisites
- Python 3.x or higher 
- Jupyter Notebook (optional)
- Next.js 
- FastAPI 
- Tailwind CSS 

### Installation
All the python libraries can be installed using "pip".
The UI dependencies can be installed using - `pnpm install` (or) `npm install` after cloning repository

### Starting Backend and Frontend: 

To start the backend server, use the following command <br>
  `uvicorn main:app --reload` 

To start the frontend, use the following command <br>
  `pnpm run dev` 
