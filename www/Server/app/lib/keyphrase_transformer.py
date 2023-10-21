import re
import dateutil.parser
from datetime import datetime
import spacy
import json

def extract_info(doc):
    # Load spaCy's English language model
    nlp = spacy.load("en_core_web_sm")
    pos_tags_of_interest = ['PROPN', 'NOUN']
    words_to_be_ignored = ['contract', 'tender', 'record', 'cost', 'price', 
                           'date', 'unspsc', 'code', "good", "service", "work" ]


    # Initialize KeyPhraseTransformer
    #kp = KeyPhraseTransformer()

    # Initialize lists to store extracted dates and prices
    dates = []
    prices = []
    codes = []

    # Regular expressions for extracting date patterns (yyyy-mm-dd), codes, and prices
    date_pattern = r'\d{4}-\d{2}-\d{2}'
    price_pattern = r'\$\d+(?:,\d{3})*(?:\.\d{2})?'  # Matches currency values (e.g., $5,000.00 or $5000)
    code_pattern = r'\d{8}(?:,\s*\d{8})*'  # Matches one or more 8-digit codes separated by commas

    # Extract dates using dateutil
    date_strings = re.findall(date_pattern, doc)

    # Initialize start_date and end_date as None
    start_date = None
    end_date = None

    # Checking which should be start date and end date
    if len(date_strings) >= 2:
        date1 = dateutil.parser.parse(date_strings[0])
        date2 = dateutil.parser.parse(date_strings[1])

        if date1 < date2:
            start_date = date1.strftime('%Y-%m-%d')
            end_date = date2.strftime('%Y-%m-%d')
        else:
            start_date = date2.strftime('%Y-%m-%d')
            end_date = date1.strftime('%Y-%m-%d')
    elif len(date_strings) == 1:
        # If only one date is given, assume it as the 'start_date'
        start_date = dateutil.parser.parse(date_strings[0]).strftime('%Y-%m-%d')
    elif len(date_strings) == 0:
        # Check for years only
        years = re.findall(r'\b\d{4}\b', doc)
        if len(years) > 0:
            years = sorted(years)
            date_object = datetime(int(years[0]), 1, 1)
            start_date = date_object.strftime('%Y-%m-%d')
            if len(years) >= 2:
                date_object = datetime(int(years[1]), 1, 1)
                end_date = date_object.strftime('%Y-%m-%d')


    # Extract UNSPSC codes using regular expressions
    code_strings = re.findall(code_pattern, doc)
    for code_str in code_strings:
        codes.extend([code.strip('"') for code in code_str.split(', ')])

    # Extract prices using regular expressions
    price_strings = re.findall(price_pattern, doc)
    # Checking which is the highest and lowest range
    if len(price_strings) >= 2:
        price1 = int(price_strings[0].replace('$', '').replace(',', ''))
        price2 = int(price_strings[1].replace('$', '').replace(',', ''))
        # Determine the lowest and highest values
        if price1 < price2:
            start_price = price1
            end_price = price2
            prices = [start_price, end_price]
        else:
            start_price = price2
            end_price = price1
            prices = [start_price, end_price]
    elif len(price_strings) == 1:
        # If only one price is given, assume it as the 'start_price'
        start_price = int(price_strings[0].replace('$', '').replace(',', ''))
        prices = [start_price]

    # Convert the text to lowercase for case-insensitive matching
    doc_lower = doc.lower()

    # Initialize type of work as an empty string
    work_type = ""

    # Check if "Goods and Services" appears in the user input
    if "goods and services" in doc_lower:
        work_type = "Goods and Services"

    # Check if "Works" appears in the user input
    elif "works" in doc_lower:
        work_type = "Works"

    # Pick only pure words
    #Remove all ignore words
    words_to_be_ignored = words_to_be_ignored + [word + 's' for word in words_to_be_ignored]
    doc_lower_words = doc_lower.split()
    
    # Use list comprehension to keep only words not in the list of words to remove
    filtered_doc_lower_words = [word for word in doc_lower_words if word not in words_to_be_ignored]
    
    # Join the filtered words back into a string
    doc_lower = ' '.join(filtered_doc_lower_words)    
    words_with_only_alphabets = re.findall(r'\b[a-zA-Z]+\b', doc_lower)
    doc = " ".join(words_with_only_alphabets).title()
    nlp_doc = nlp(doc)
    keywords = " ".join([token.text for token in nlp_doc if token.pos_ in pos_tags_of_interest ])

    # Create a dictionary to store the extracted information
    result_dict = {
        "query": keywords,
        "startDate": start_date,
        "endDate": end_date,
        "Range": prices,
        "typeOfWork": work_type,
        "UNSPSCcode": [int(code) for code in codes]
    }

    # Convert the dictionary to a JSON string
    result_json = json.dumps(result_dict, indent=4)

    return result_json
