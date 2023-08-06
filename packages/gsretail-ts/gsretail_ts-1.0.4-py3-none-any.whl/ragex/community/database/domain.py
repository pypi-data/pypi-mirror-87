import json
from collections import defaultdict
from typing import Any, Text, Dict, Union

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from rasa.core.domain import (
    Domain as RasaDomain,
    SESSION_CONFIG_KEY,
    SESSION_EXPIRATION_TIME_KEY,
    CARRY_OVER_SLOTS_KEY,
)
from ragex.community.database.base import Base
from ragex.community.database.data import TEMPLATE_ANNOTATION_KEYS, Template
from ragex.community.database import utils


class Domain(Base):
    """Stores the domain of the currently deployed Core model."""

    __tablename__ = "domain"

    id = sa.Column(sa.Integer, utils.create_sequence(__tablename__), primary_key=True)
    project_id = sa.Column(sa.String, sa.ForeignKey("project.project_id"))
    store_entities_as_slots = sa.Column(sa.Boolean, default=True)
    path = sa.Column(sa.String, nullable=True)
    session_expiration_time = sa.Column(sa.Float)
    carry_over_slots = sa.Column(sa.Boolean)

    actions = relationship(
        "DomainAction",
        cascade="all, delete-orphan",
        back_populates="domain",
        order_by=lambda: DomainAction.action_id.asc(),
    )
    intents = relationship(
        "DomainIntent",
        cascade="all, delete-orphan",
        back_populates="domain",
        order_by=lambda: DomainIntent.domain_id.asc(),
    )
    entities = relationship(
        "DomainEntity",
        cascade="all, delete-orphan",
        back_populates="domain",
        order_by=lambda: DomainEntity.entity_id.asc(),
    )
    slots = relationship(
        "DomainSlot",
        cascade="all, delete-orphan",
        back_populates="domain",
        order_by=lambda: DomainSlot.slot_id.asc(),
    )
    templates = relationship(
        "Template",
        cascade="all, delete-orphan",
        back_populates="domain",
        order_by=lambda: Template.id.asc(),
    )

    def remove_annotations(self, template_dict):
        """Removes keys from templates that are irrelevant for the dumped
        domain."""

        for key in TEMPLATE_ANNOTATION_KEYS:
            if key in template_dict:
                del template_dict[key]

        return template_dict

    def dump_templates(self):
        template_list = [
            {t.template: self.remove_annotations(json.loads(t.content))}
            for t in self.templates
        ]

        template_dict = defaultdict(list)
        for template in template_list:
            for k, v in template.items():
                template_dict[k].append(v)

        return dict(template_dict)

    def _get_session_config(self) -> Dict[Text, Union[bool, float]]:
        session_config = {}

        if self.session_expiration_time is not None:
            session_config[SESSION_EXPIRATION_TIME_KEY] = self.session_expiration_time

        if self.carry_over_slots is not None:
            session_config[CARRY_OVER_SLOTS_KEY] = self.carry_over_slots

        return session_config

    def as_dict(self) -> Dict[Text, Any]:
        slots = {}
        for s in self.slots:
            name = s.slot
            slots[name] = {"auto_fill": s.auto_fill, "type": s.type}

            if s.initial_value:
                slots[name]["initial_value"] = json.loads(s.initial_value)

            if "categorical" in s.type.lower() and s.values:
                slots[name]["values"] = json.loads(s.values)

        domain_dict = {
            "config": {"store_entities_as_slots": self.store_entities_as_slots},
            "actions": [e.action for e in self.actions if not e.is_form],
            "forms": [e.action for e in self.actions if e.is_form],
            "entities": [e.entity for e in self.entities],
            "intents": [i.as_dict() for i in self.intents],
            "slots": slots,
            "templates": self.dump_templates(),
        }

        if self.path:
            domain_dict["path"] = self.path

        session_config = self._get_session_config()
        if session_config:
            domain_dict[SESSION_CONFIG_KEY] = session_config

        return domain_dict

    def as_rasa_domain(self) -> RasaDomain:
        return RasaDomain.from_dict(self.as_dict())

    def is_empty(self):
        return not any(
            [self.actions, self.templates, self.entities, self.intents, self.slots]
        )


class DomainAction(Base):
    """Stores the actions which are defined in the domain."""

    __tablename__ = "domain_action"

    action_id = sa.Column(
        sa.Integer, utils.create_sequence(__tablename__), primary_key=True
    )
    domain_id = sa.Column(sa.Integer, sa.ForeignKey("domain.id"))
    action = sa.Column(sa.String)
    is_form = sa.Column(sa.Boolean, default=False)

    domain = relationship("Domain", back_populates="actions")

    def as_dict(self) -> Dict[Text, Union[Text, bool]]:
        return {
            "id": self.action_id,
            "domain_id": self.domain_id,
            "name": self.action,
            "is_form": self.is_form,
        }


class DomainIntent(Base):
    """Stores the intents which are defined in the domain."""

    __tablename__ = "domain_intent"

    intent_id = sa.Column(
        sa.Integer, utils.create_sequence(__tablename__), primary_key=True
    )
    domain_id = sa.Column(sa.Integer, sa.ForeignKey("domain.id"))
    intent = sa.Column(sa.String)
    triggered_action = sa.Column(sa.String)
    use_entities = sa.Column(sa.Text)
    ignore_entities = sa.Column(sa.Text)

    domain = relationship("Domain", back_populates="intents")

    def as_dict(self) -> Dict[Text, Any]:
        config = {
            "use_entities": json.loads(self.use_entities or "true"),
            "ignore_entities": json.loads(self.ignore_entities or str([])),
        }

        if self.triggered_action:
            config["triggers"] = self.triggered_action

        return {self.intent: config}


class DomainEntity(Base):
    """Stores the entities which are defined in the domain."""

    __tablename__ = "domain_entity"

    entity_id = sa.Column(
        sa.Integer, utils.create_sequence(__tablename__), primary_key=True
    )
    domain_id = sa.Column(sa.Integer, sa.ForeignKey("domain.id"))
    entity = sa.Column(sa.String)

    domain = relationship("Domain", back_populates="entities")


class DomainSlot(Base):
    """Stores the slots which are defined in the domain."""

    __tablename__ = "domain_slot"

    slot_id = sa.Column(
        sa.Integer, utils.create_sequence(__tablename__), primary_key=True
    )
    domain_id = sa.Column(sa.Integer, sa.ForeignKey("domain.id"))
    slot = sa.Column(sa.String)
    auto_fill = sa.Column(sa.Boolean, default=True)
    initial_value = sa.Column(sa.String)
    type = sa.Column(sa.String, default="rasa.core.slots.UnfeaturizedSlot")
    values = sa.Column(sa.String)

    domain = relationship("Domain", back_populates="slots")
