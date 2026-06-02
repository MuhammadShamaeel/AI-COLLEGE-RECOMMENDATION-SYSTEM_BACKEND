from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import ChatSession, ChatMessage
from .serializers import (
    ChatSessionSerializer,
    ChatSessionDetailSerializer
)

from apps.rag.services.rag_pipeline import ask_college_assistant


class ChatView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        message = request.data.get("message", "").strip()
        session_id = request.data.get("session_id")
        
        # Get context from request (passed from frontend)
        context_state = request.data.get("context_state", "")
        context_location = request.data.get("context_location", "")

        if not message:
            return Response(
                {
                    "success": False,
                    "message": "Message cannot be empty."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get or create chat session
        if session_id:
            try:
                session = ChatSession.objects.get(id=session_id)
            except ChatSession.DoesNotExist:
                session = ChatSession.objects.create(
                    user=None,
                    title=message[:60]
                )
        else:
            session = ChatSession.objects.create(
                user=None,
                title=message[:60]
            )

        # Save user message
        ChatMessage.objects.create(
            session=session,
            role="user",
            content=message
        )

        # Call RAG pipeline with context
        try:
            answer = ask_college_assistant(
                question=message,
                context_state=context_state,
                context_location=context_location
            )
        except Exception as e:
            print(f"RAG Pipeline Error: {e}")
            answer = "I'm having trouble accessing the college database right now. Please try again in a moment."

        # Save AI reply
        ChatMessage.objects.create(
            session=session,
            role="assistant",
            content=answer
        )

        session.save()

        return Response(
            {
                "success": True,
                "session_id": session.id,
                "question": message,
                "answer": answer,
            },
            status=status.HTTP_200_OK
        )


class ChatSessionListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        sessions = ChatSession.objects.all()[:50]
        serializer = ChatSessionSerializer(sessions, many=True)
        return Response({
            "success": True,
            "count": sessions.count(),
            "data": serializer.data,
        })


class ChatSessionDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            session = ChatSession.objects.get(pk=pk)
        except ChatSession.DoesNotExist:
            return Response(
                {"success": False, "message": "Session not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ChatSessionDetailSerializer(session)
        return Response({"success": True, "data": serializer.data})

    def delete(self, request, pk):
        try:
            session = ChatSession.objects.get(pk=pk)
            session.delete()
            return Response({"success": True, "message": "Chat session deleted."})
        except ChatSession.DoesNotExist:
            return Response(
                {"success": False, "message": "Session not found."},
                status=status.HTTP_404_NOT_FOUND
            )