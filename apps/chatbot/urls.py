from django.urls import path

from .views import (
    ChatView,
    ChatSessionListView,
    ChatSessionDetailView,
)

urlpatterns = [

    # Send message → get AI reply
    # POST /api/chatbot/chat/
    path(
        "chat/",
        ChatView.as_view(),
        name="chatbot-chat"
    ),

    # List all sessions for logged-in user
    # GET /api/chatbot/sessions/
    path(
        "sessions/",
        ChatSessionListView.as_view(),
        name="chatbot-session-list"
    ),

    # Get history or delete one session
    # GET    /api/chatbot/sessions/1/
    # DELETE /api/chatbot/sessions/1/
    path(
        "sessions/<int:pk>/",
        ChatSessionDetailView.as_view(),
        name="chatbot-session-detail"
    ),
]