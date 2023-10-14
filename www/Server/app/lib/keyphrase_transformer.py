from keyphrasetransformer import KeyPhraseTransformer
import re
import dateutil.parser
import spacy


def extract_info(doc):
    # Load spaCy's English language model
    nlp = spacy.load("en_core_web_sm")

    # Initialize KeyPhraseTransformer
    kp = KeyPhraseTransformer()

    # Initialize lists to store extracted dates and prices
    dates = []
    prices = []
    codes = []

    # Regular expressions for extracting date patterns (yyyy-mm-dd), codes, and prices
    date_pattern = r"\d{4}-\d{2}-\d{2}"
    price_pattern = r"\$\d+(?:,\d{3})*(?:\.\d{2})?"  # Matches currency values (e.g., $5,000.00 or $5000)
    code_pattern = (
        r"\d{8}(?:,\s*\d{8})*"  # Matches one or more 8-digit codes separated by commas
    )

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
            start_date = date1.strftime("%Y-%m-%d")
            end_date = date2.strftime("%Y-%m-%d")
        else:
            start_date = date2.strftime("%Y-%m-%d")
            end_date = date1.strftime("%Y-%m-%d")
    elif len(date_strings) == 1:
        # If only one date is given, assume it as the 'start_date'
        start_date = dateutil.parser.parse(date_strings[0]).strftime("%Y-%m-%d")

    # Extract UNSPSC codes using regular expressions
    code_strings = re.findall(code_pattern, doc)
    for code_str in code_strings:
        codes.extend([code.strip('"') for code in code_str.split(", ")])

    # Extract prices using regular expressions
    price_strings = re.findall(price_pattern, doc)
    # Checking which is the highest and lowest range
    if len(price_strings) >= 2:
        price1 = int(price_strings[0].replace("$", "").replace(",", ""))
        price2 = int(price_strings[1].replace("$", "").replace(",", ""))
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
        start_price = int(price_strings[0].replace("$", "").replace(",", ""))
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

    # Exclude patterns by replacing them with spaces
    doc = re.sub(date_pattern, " ", doc)
    doc = re.sub(price_pattern, " ", doc)
    doc = re.sub(code_pattern, " ", doc)

    # Extract keywords and returning only the first keyword
    keywords = kp.get_key_phrases(doc)
    first_keyword = keywords[0] if keywords else None

    # Create a dictionary to store the extracted information
    result_dict = {
        "query": first_keyword,
        "startDate": start_date,
        "endDate": end_date,
        "Range": prices,
        "typeOfWork": work_type,
        "UNSPSCcode": [int(code) for code in codes],
    }

    return result_dict
