import re


def clean_text(text):

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    # Remove multiple newlines
    text = re.sub(r'\n+', '\n', text)

    # Remove unwanted symbols
    text = re.sub(r'[•■▪►]', ' ', text)

    # Remove page numbers
    text = re.sub(r'Page \d+', '', text)

    # Remove repeated spaces again
    text = re.sub(r'\s+', ' ', text)

    return text.strip()