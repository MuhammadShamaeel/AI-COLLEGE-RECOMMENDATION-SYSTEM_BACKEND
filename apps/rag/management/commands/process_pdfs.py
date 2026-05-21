from django.core.management.base import BaseCommand

from apps.rag.services.pdf_loader import load_all_pdfs

from apps.rag.services.text_splitter import split_documents

from apps.rag.services.embedding_service import create_embeddings

from apps.rag.services.vector_store import save_to_faiss


class Command(BaseCommand):

    help = "Process PDFs and create FAISS vector DB"

    def handle(self, *args, **kwargs):

        # STEP 1 — Load PDFs
        documents = load_all_pdfs()

        print(f"\nPDFs Loaded: {len(documents)}")

        # STEP 2 — Split into chunks
        chunks = split_documents(documents)

        print(f"\nTotal Chunks Created: {len(chunks)}")

        # STEP 3 — Create embeddings
        embeddings = create_embeddings(chunks)

        print("\nEmbeddings Created Successfully")

        # STEP 4 — Save into FAISS
        save_to_faiss(
            chunks,
            embeddings
        )

        print("\nFAISS Vector Database Created Successfully")