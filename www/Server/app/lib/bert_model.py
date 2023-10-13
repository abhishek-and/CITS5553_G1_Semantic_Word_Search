from transformers import AutoTokenizer, AutoModel
import torch
import pandas as pd
from nltk.tokenize import word_tokenize

# Load BERT model and tokenizer
model_name = "bert-large-uncased"  # You can use other BERT variants
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)


def semantic_word_search(query_word, word_list, threshold=0.80):
    # Encode the query word
    query_input = tokenizer(
        query_word, return_tensors="pt", padding=True, truncation=True
    )
    with torch.no_grad():
        query_output = model(**query_input)

    # Extract the embeddings for the query word
    query_embedding = query_output.last_hidden_state.mean(dim=1).squeeze()

    # Encode the list of words
    word_inputs = tokenizer(
        word_list, return_tensors="pt", padding=True, truncation=True
    )
    with torch.no_grad():
        word_outputs = model(**word_inputs)

    # Extract the embeddings for the list of words
    word_embeddings = word_outputs.last_hidden_state.mean(dim=1)

    # Calculate cosine similarity between query and list of words
    cosine_scores = torch.nn.functional.cosine_similarity(
        query_embedding, word_embeddings, dim=1
    )

    # Convert cosine similarity scores to semantic scores and to normal (Python float) values
    semantic_scores = [
        (score.item() + 1) / 2 for score in cosine_scores
    ]  # Normalize to [0, 1] range and convert to float

    # Create a list to store unique words and their corresponding semantic scores as pairs
    unique_words_and_scores = []

    # Iterate through the words and semantic scores
    for word, score in zip(word_list, semantic_scores):
        if word not in (pair[0] for pair in unique_words_and_scores):
            if score > threshold:
                unique_words_and_scores.append((word, score))

    # Separate the unique words and their scores into separate lists
    unique_words, unique_scores = zip(*unique_words_and_scores)

    return list(unique_words), list(unique_scores)


def process_csv_and_get_scores(reference_number, query_word):
    # Read the CSV file into a DataFrame
    file_path = "try.csv"
    df = pd.read_csv(file_path, encoding="utf-8")

    # Filter the DataFrame based on the reference_number
    filtered_data = df[df["Reference Number"] == reference_number]

    # Concatenate text data from multiple columns into a single string
    columns_to_concat = ["Contract Title", "Description", "Tenders Content"]
    text_data = " ".join(
        filtered_data[column].values[0] for column in columns_to_concat
    )
    text_data = text_data.lower()

    # Tokenize the concatenated text data
    tokenized_words = word_tokenize(text_data)

    # Get words list and semantic scores using the BERT model
    words_list, semantic_scores = semantic_word_search(query_word, tokenized_words)

    return words_list, semantic_scores
