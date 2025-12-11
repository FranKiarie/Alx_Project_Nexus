import uuid
from django.db import models
from django.utils import timezone


class TimestampedModel(models.Model):
    """Abstract base providing created/updated timestamps."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Poll(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.TextField()
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.question[:50]

    @property
    def is_expired(self) -> bool:
        return bool(self.expires_at and timezone.now() >= self.expires_at)


class Option(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    poll = models.ForeignKey(
        Poll,
        related_name="options",
        on_delete=models.CASCADE,
        db_index=True,
    )
    text = models.CharField(max_length=255)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["poll", "text"]),
        ]

    def __str__(self) -> str:
        return f"{self.poll_id}: {self.text}"


class Vote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    poll = models.ForeignKey(
        Poll,
        related_name="votes",
        on_delete=models.CASCADE,
        db_index=True,
    )
    option = models.ForeignKey(
        Option,
        related_name="votes",
        on_delete=models.CASCADE,
    )
    voter_identifier = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["poll", "voter_identifier"],
                name="unique_vote_per_poll_per_voter",
            )
        ]
        indexes = [
            models.Index(fields=["poll", "option"]),
            models.Index(fields=["poll", "voter_identifier"]),
        ]

    def __str__(self) -> str:
        return f"{self.poll_id} -> {self.option_id} ({self.voter_identifier})"

