from typing import Any, Dict, List
from rest_framework import serializers

from .models import Option, Poll, Vote
from .services import create_poll, get_poll_results


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["id", "text"]


class PollSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ["id", "question", "expires_at", "created_at", "updated_at", "options"]


class PollCreateSerializer(serializers.Serializer):
    question = serializers.CharField()
    expires_at = serializers.DateTimeField(required=False, allow_null=True)
    options = serializers.ListField(
        child=serializers.CharField(),
        min_length=2,
        allow_empty=False,
    )

    def create(self, validated_data: Dict[str, Any]) -> Poll:
        question: str = validated_data["question"]
        expires_at = validated_data.get("expires_at")
        options: List[str] = validated_data["options"]
        return create_poll(question=question, options=options, expires_at=expires_at)


class VoteSerializer(serializers.Serializer):
    option_id = serializers.UUIDField()
    voter_identifier = serializers.CharField(required=False, allow_blank=True)


class ResultOptionSerializer(serializers.Serializer):
    option = serializers.CharField()
    votes = serializers.IntegerField()


class PollResultSerializer(serializers.Serializer):
    poll = serializers.CharField()
    results = ResultOptionSerializer(many=True)

    @classmethod
    def from_poll(cls, poll: Poll) -> "PollResultSerializer":
        results = get_poll_results(poll)
        payload = {
            "poll": poll.question,
            "results": results,
        }
        return cls(payload)

