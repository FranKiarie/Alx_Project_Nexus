from django.db import models
from django.utils import timezone
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

from .models import Poll
from .serializers import (
    PollCreateSerializer,
    PollResultSerializer,
    PollSerializer,
    VoteSerializer,
)
from .services import cast_vote


class PollViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = (
        Poll.objects.all()
        .prefetch_related("options")
        .order_by("-created_at")
    )
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_at", "expires_at", "question"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action == "create":
            return PollCreateSerializer
        if self.action == "results":
            return PollResultSerializer
        return PollSerializer

    def create(self, request, *args, **kwargs):
        input_serializer = PollCreateSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        poll = input_serializer.save()
        output_serializer = PollSerializer(poll, context=self.get_serializer_context())
        headers = self.get_success_headers(output_serializer.data)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        queryset = super().get_queryset()
        active_param = self.request.query_params.get("active")
        if active_param is not None:
            now = timezone.now()
            is_active = active_param.lower() == "true"
            if is_active:
                queryset = queryset.filter(
                    models.Q(expires_at__isnull=True) | models.Q(expires_at__gte=now)
                )
            else:
                queryset = queryset.filter(expires_at__lt=now)
        return queryset

    @extend_schema(
        responses={
            201: OpenApiResponse(description="Poll created"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            400: OpenApiResponse(
                response=None,
                description="Validation error",
                examples=[
                    OpenApiExample(
                        "Missing options",
                        value={"options": ["This field is required."]},
                    ),
                ],
            ),
        }
    )
    @action(detail=True, methods=["post"])
    def vote(self, request, pk=None):
        poll = self.get_object()
        serializer = VoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        voter_identifier = serializer.validated_data.get(
            "voter_identifier",
            request.META.get("REMOTE_ADDR", ""),
        )
        cast_vote(
            poll=poll,
            option_id=serializer.validated_data["option_id"],
            voter_identifier=voter_identifier,
        )
        return Response(
            {"message": "Vote recorded successfully."},
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        responses={
            200: PollResultSerializer,
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Poll not found"),
        },
        examples=[
            OpenApiExample(
                "Sample results",
                value={
                    "poll": "Favorite language?",
                    "results": [
                        {"option": "Python", "votes": 10},
                        {"option": "JavaScript", "votes": 5},
                    ],
                },
            )
        ],
    )
    @action(detail=True, methods=["get"])
    def results(self, request, pk=None):
        poll = self.get_object()
        serializer = PollResultSerializer.from_poll(poll)
        return Response(serializer.data)


class HealthAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)

