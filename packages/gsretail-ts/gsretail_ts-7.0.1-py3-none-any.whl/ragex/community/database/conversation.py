import json
from typing import Dict, Any, Text

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from ragex.community.constants import DEFAULT_RASA_ENVIRONMENT
from ragex.community.database.base import Base
from ragex.community.database import utils


class Conversation(Base):
    """Stores the user's conversation and its metadata."""

    __tablename__ = "conversation"

    sender_id = sa.Column(sa.String, primary_key=True)
    number_user_messages = sa.Column(sa.Integer, default=0)
    latest_input_channel = sa.Column(sa.String)
    latest_event_time = sa.Column(sa.Float)  # latest event time as unix timestamp
    in_training_data = sa.Column(sa.Boolean, default=True)
    minimum_action_confidence = sa.Column(sa.Float, default=1.0)
    evaluation = sa.Column(sa.Text)
    interactive = sa.Column(sa.Boolean, default=False)

    events = relationship(
        "ConversationEvent",
        cascade="all, delete-orphan",
        back_populates="conversation",
        order_by=lambda: ConversationEvent.timestamp.asc(),
    )

    unique_policies = relationship(
        "ConversationPolicyMetadata",
        cascade="all, delete-orphan",
        back_populates="conversation",
    )
    unique_actions = relationship(
        "ConversationActionMetadata",
        cascade="all, delete-orphan",
        back_populates="conversation",
    )
    unique_intents = relationship(
        "ConversationIntentMetadata",
        cascade="all, delete-orphan",
        back_populates="conversation",
    )
    unique_entities = relationship(
        "ConversationEntityMetadata",
        cascade="all, delete-orphan",
        back_populates="conversation",
    )

    corrected_messages = relationship(
        "ConversationMessageCorrection",
        cascade="all, delete-orphan",
        back_populates="conversation",
    )

    def as_dict(self) -> Dict[Text, Any]:
        from ragex.community.services.event_service import EventService

        return {
            "sender_id": self.sender_id,
            "sender_name": EventService.get_sender_name(self),  # displayed in the UI
            "latest_event_time": self.latest_event_time,
            "latest_input_channel": self.latest_input_channel,
            "intents": [i.intent for i in self.unique_intents],
            "actions": [a.action for a in self.unique_actions],
            "minimum_action_confidence": self.minimum_action_confidence,
            "in_training_data": self.in_training_data,
            "policies": [p.policy for p in self.unique_policies],
            "n_user_messages": self.number_user_messages,
            "flagged_messages": [e.timestamp for e in self.events if e.is_flagged],
            "unflagged_messages": [e.timestamp for e in self.events if e.is_unflagged],
            "corrected_messages": [
                {"message_timestamp": c.message_timestamp, "intent": c.intent}
                for c in self.corrected_messages
            ],
            "interactive": self.interactive,
        }


class ConversationEvent(Base):
    """Stores a single event which happened during a conversation."""

    __tablename__ = "conversation_event"

    id = sa.Column(sa.Integer, utils.create_sequence(__tablename__), primary_key=True)
    conversation_id = sa.Column(
        sa.String, sa.ForeignKey("conversation.sender_id"), index=True, nullable=False
    )
    conversation = relationship("Conversation", back_populates="events")

    type_name = sa.Column(sa.String, nullable=False)
    timestamp = sa.Column(
        sa.Float, index=True, nullable=False
    )  # time of the event as unix timestamp
    intent_name = sa.Column(sa.String)
    action_name = sa.Column(sa.String)
    policy = sa.Column(sa.String)
    is_flagged = sa.Column(sa.Boolean, default=False, nullable=False)
    is_unflagged = sa.Column(sa.Boolean, default=False, nullable=False)
    data = sa.Column(sa.Text)
    message_log = relationship("MessageLog", back_populates="event", uselist=False)
    evaluation = sa.Column(sa.Text)
    rasa_environment = sa.Column(sa.String, default=DEFAULT_RASA_ENVIRONMENT)

    def as_rasa_dict(self) -> Dict[Text, Any]:
        """Return a JSON-like representation of the internal Rasa (framework)
        event referenced by this `ConversationEvent`. Attach some information
        specific to Rasa X as part of the Rasa event metadata.

        Returns:
            A JSON-like representation of the Rasa event referenced by this
                database entity.
        """

        d = json.loads(self.data)

        # Add some metadata specific to Rasa X (namespaced with "rasa_x_")
        d.setdefault("metadata", {}).update(
            {"rasa_x_flagged": self.is_flagged, "rasa_x_id": self.id}
        )

        return d


class MessageLog(Base):
    """Stores the intent classification results of the user messages."""

    __tablename__ = "message_log"

    id = sa.Column(sa.Integer, utils.create_sequence(__tablename__), primary_key=True)
    hash = sa.Column(sa.String)
    model_id = sa.Column(sa.Integer, sa.ForeignKey("model.id"))
    model = relationship("Model", back_populates="message_logs")
    archived = sa.Column(sa.Boolean, default=False)
    time = sa.Column(sa.Float)  # time of the log as unix timestamp
    text = sa.Column(sa.Text)
    intent = sa.Column(sa.String)
    confidence = sa.Column(sa.Float)
    intent_ranking = sa.Column(sa.Text)
    entities = sa.Column(sa.Text)

    event_id = sa.Column(sa.Integer, sa.ForeignKey("conversation_event.id"))
    event = relationship(
        "ConversationEvent", uselist=False, back_populates="message_log"
    )

    __table_args__ = (sa.Index("message_log_idx_archived_text", "archived", "text"),)

    def as_dict(self) -> Dict[Text, Any]:
        return {
            "id": self.id,
            "time": self.time,
            "model": self.model.name if self.model else None,
            "hash": self.hash,
            "project_id": self.model.project_id if self.model else None,
            "team": self.model.project.team if self.model else None,
            "user_input": {
                "text": self.text,
                "intent": {"name": self.intent, "confidence": self.confidence},
                "intent_ranking": json.loads(self.intent_ranking),
                "entities": json.loads(self.entities),
            },
        }


class ConversationPolicyMetadata(Base):
    """Stores the distinct set of used policies in a conversation."""

    __tablename__ = "conversation_policy_metadata"

    conversation_id = sa.Column(
        sa.String, sa.ForeignKey("conversation.sender_id"), primary_key=True
    )
    policy = sa.Column(sa.String, primary_key=True)
    conversation = relationship("Conversation", back_populates="unique_policies")


class ConversationActionMetadata(Base):
    """Stores the distinct set of used actions in a conversation."""

    __tablename__ = "conversation_action_metadata"

    conversation_id = sa.Column(
        sa.String, sa.ForeignKey("conversation.sender_id"), primary_key=True
    )
    action = sa.Column(sa.String, primary_key=True)
    conversation = relationship("Conversation", back_populates="unique_actions")


class ConversationIntentMetadata(Base):
    """Stores the distinct set of used intents in a conversation."""

    __tablename__ = "conversation_intent_metadata"

    conversation_id = sa.Column(
        sa.String, sa.ForeignKey("conversation.sender_id"), primary_key=True
    )

    intent = sa.Column(sa.String, primary_key=True)
    conversation = relationship("Conversation", back_populates="unique_intents")


class ConversationEntityMetadata(Base):
    """Stores the distinct set of used entities in a conversation."""

    __tablename__ = "conversation_entity_metadata"

    conversation_id = sa.Column(
        sa.String, sa.ForeignKey("conversation.sender_id"), primary_key=True
    )

    entity = sa.Column(sa.String, primary_key=True)
    conversation = relationship("Conversation", back_populates="unique_entities")


class ConversationMessageCorrection(Base):
    """Stores post hoc corrections of intents in a conversation."""

    __tablename__ = "message_correction"

    conversation_id = sa.Column(
        sa.String, sa.ForeignKey("conversation.sender_id"), primary_key=True
    )

    # time of the message correction as unix timestamp
    message_timestamp = sa.Column(sa.Float, primary_key=True)
    intent = sa.Column(sa.String)
    conversation = relationship("Conversation", back_populates="corrected_messages")
