from django.core.management.base import BaseCommand

from apps.rag.services.retrieval_service import (
    retrieve_relevant_chunks
)


class Command(BaseCommand):

    help = "Test semantic retrieval"

    def handle(self, *args, **kwargs):

        query = input(
            "\nEnter Query: "
        )

        results = retrieve_relevant_chunks(
            query
        )

        print("\n\nRETRIEVED CHUNKS:\n")

        for result in results:

            print("=" * 50)

            print(
                f"College: {result['college']}"
            )

            print(
                f"Location: {result['location']}"
            )

            print("\nContent:\n")

            print(result['content'][:1000])

            print("\n")