from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import ChatSession, ChatMessage
from .serializers import (
    ChatSessionSerializer,
    ChatSessionDetailSerializer,
    ChatMessageSerializer,
)

from apps.rag.services.rag_pipeline import ask_college_assistant


# ============================================================
# CHAT VIEW  — send a message and get AI reply
# POST /api/chatbot/chat/
#
# Request body:
#   {
#     "message": "What are the fees for CSE in Kerala?",
#     "session_id": 3          ← optional; omit to start a new session
#   }
#
# Response:
#   {
#     "success": true,
#     "session_id": 3,
#     "question": "...",
#     "answer": "..."
#   }
# ============================================================

class ChatView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        message = request.data.get("message", "").strip()

        if not message:
            return Response(
                {
                    "success": False,
                    "message": "Message cannot be empty."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        session_id = request.data.get("session_id")

        # ── Get or create chat session ───────────────────────
        if session_id:
            try:
                session = ChatSession.objects.get(
                    id=session_id,
                    user=request.user
                )
            except ChatSession.DoesNotExist:
                return Response(
                    {
                        "success": False,
                        "message": "Chat session not found."
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # Auto-title the session using first 60 chars of the question
            session = ChatSession.objects.create(
                user=request.user,
                title=message[:60]
            )

        # ── Save user message ────────────────────────────────
        ChatMessage.objects.create(
            session=session,
            role="user",
            content=message
        )

        # ── Call RAG pipeline ────────────────────────────────
        answer = ask_college_assistant(message)

        # ── Save AI reply ────────────────────────────────────
        ChatMessage.objects.create(
            session=session,
            role="assistant",
            content=answer
        )

        # Touch the session's updated_at timestamp
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


# ============================================================
# SESSION LIST VIEW  — list all sessions for the logged-in user
# GET /api/chatbot/sessions/
# ============================================================

class ChatSessionListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        sessions = ChatSession.objects.filter(user=request.user)

        serializer = ChatSessionSerializer(sessions, many=True)

        return Response(
            {
                "success": True,
                "count": sessions.count(),
                "data": serializer.data,
            }
        )


# ============================================================
# SESSION DETAIL VIEW  — get full chat history of one session
# GET  /api/chatbot/sessions/<id>/
# DELETE /api/chatbot/sessions/<id>/
# ============================================================

class ChatSessionDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def _get_session(self, pk, user):
        try:
            return ChatSession.objects.get(pk=pk, user=user)
        except ChatSession.DoesNotExist:
            return None

    def get(self, request, pk):

        session = self._get_session(pk, request.user)

        if not session:
            return Response(
                {
                    "success": False,
                    "message": "Session not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ChatSessionDetailSerializer(session)

        return Response(
            {
                "success": True,
                "data": serializer.data,
            }
        )

    def delete(self, request, pk):

        session = self._get_session(pk, request.user)

        if not session:
            return Response(
                {
                    "success": False,
                    "message": "Session not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        session.delete()

        return Response(
            {
                "success": True,
                "message": "Chat session deleted successfully."
            },
            status=status.HTTP_200_OK
        )