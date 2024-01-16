# serializers.py
from rest_framework import serializers

class ConversationSerializer(serializers.Serializer):
    role = serializers.CharField()
    content = serializers.CharField()

class GPTRequestSerializer(serializers.Serializer):
    mode = serializers.CharField()
    messages = ConversationSerializer(many=True)
    stream = serializers.BooleanField()
