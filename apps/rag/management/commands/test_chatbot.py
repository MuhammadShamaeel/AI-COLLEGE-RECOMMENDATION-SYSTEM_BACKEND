from django.core.management.base import BaseCommand

from apps.rag.services.rag_pipeline import ask_college_assistant


class Command(BaseCommand):

    help = "Test AI College Chatbot"

    def handle(self, *args, **kwargs):

        question = input("\nAsk Question: ")

        response = ask_college_assistant(question)

        print("\n")
        print("=" * 60)
        print("\nAI RESPONSE:\n")
        print(response)