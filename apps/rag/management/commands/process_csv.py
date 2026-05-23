from django.core.management.base import BaseCommand

from apps.rag.services.csv_loader import load_csv_data
from apps.rag.services.text_splitter import split_documents
from apps.rag.services.embedding_service import create_embeddings
from apps.rag.services.vector_store import save_to_faiss


class Command(BaseCommand):

    help = "Process CSV and create FAISS vector DB"

    def handle(self, *args, **kwargs):

        documents = load_csv_data()

        print(f"\nDocuments Loaded: {len(documents)}")

        chunks = split_documents(documents)

        print(f"\nChunks Created: {len(chunks)}")

        embeddings = create_embeddings(chunks)

        print("\nEmbeddings Created")

        save_to_faiss(
            chunks,
            embeddings
        )

        print("\nFAISS DB Created Successfully")