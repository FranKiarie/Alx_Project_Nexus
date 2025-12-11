from typing import List, Optional
from django.db import IntegrityError, transaction
from django.db.models import Count
from django.utils import timezone
from rest_framework import exceptions

from .models import Option, Poll, Vote


@transaction.atomic
def create_poll(question: str, options: List[str], expires_at: Optional[str] = None) -> Poll:
    poll = Poll.objects.create(question=question, expires_at=expires_at)
    option_objects = [Option(poll=poll, text=option) for option in options]
    Option.objects.bulk_create(option_objects)
    return poll


def cast_vote(poll: Poll, option_id, voter_identifier: str) -> Vote:
    if poll.is_expired:
        raise exceptions.ValidationError("Poll is closed for voting.")

    try:
        option = poll.options.get(id=option_id)
    except Option.DoesNotExist as exc:
        raise exceptions.ValidationError("Option does not belong to this poll.") from exc

    if not voter_identifier:
        voter_identifier = "anonymous"

    try:
        with transaction.atomic():
            vote = Vote.objects.create(
                poll=poll,
                option=option,
                voter_identifier=voter_identifier,
            )
    except IntegrityError as exc:
        raise exceptions.ValidationError("You have already voted on this poll.") from exc

    return vote


def get_poll_results(poll: Poll) -> List[dict]:
    results = (
        poll.options.annotate(votes_count=Count("votes"))
        .order_by("created_at")
        .values("text", "votes_count")
    )
    return [{"option": row["text"], "votes": row["votes_count"]} for row in results]

