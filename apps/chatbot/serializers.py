from rest_framework import serializers

from .models import ChatSession, ChatMessage


# ============================================================
# CHAT MESSAGE SERIALIZER
# ============================================================

class ChatMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatMessage

        fields = [
            "id",
            "role",
            "content",
            "created_at",
        ]


# ============================================================
# CHAT SESSION SERIALIZER  (list view - no messages)
# ============================================================

class ChatSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatSession

        fields = [
            "id",
            "title",
            "created_at",
            "updated_at",
        ]


# ============================================================
# CHAT SESSION DETAIL SERIALIZER  (includes messages)
# ============================================================

class ChatSessionDetailSerializer(serializers.ModelSerializer):

    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSession

        fields = [
            "id",
            "title",
            "messages",
            "created_at",
            "updated_at",
        ]