from pathlib import Path
from pypdf import PdfReader
from apps.rag.services.text_cleaner import clean_text


MEDIA_ROOT = Path("media")


def extract_text_from_pdf(pdf_path):

    text = ""

    try:

        reader = PdfReader(pdf_path)

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    except Exception as e:

        print(f"Error reading {pdf_path}: {e}")

    return text


def load_all_pdfs():

    documents = []

    for location_folder in MEDIA_ROOT.iterdir():

        if location_folder.is_dir():

            location = location_folder.name

            for pdf_file in location_folder.glob("*.pdf"):

                print(f"Processing: {pdf_file.name}")

                raw_text = extract_text_from_pdf(pdf_file)

                text = clean_text(raw_text)

                documents.append(
                    {
                        "college": pdf_file.stem,
                        "location": location,
                        "text": text,
                    }
                )

    return documents