from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, Text
import json
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.types import TypeDecorator, TEXT

from helpers.rule_model import BaseRule
import helpers.constants as constants

class ModelBase(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

Base = declarative_base(cls=ModelBase)

tag_association_table = Table(
    'tag_association',
    Base.metadata,
    Column('tag_id', Integer, ForeignKey('tag.id')),
    Column('rule_id', Integer, ForeignKey('rule.id'))
)

class Tag(Base):

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name = Column(
        String(constants.TAG_NAME_MAX_LENGTH),
        unique=True
    )

class JSONEncodedDict(TypeDecorator):
    impl = TEXT

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return value

class MessageHistory(Base):
    __tablename__ = 'message_history'

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    history = Column(JSONEncodedDict)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    last_updated = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now()
    )

    def to_dict(self):
        return {
            'id': self.id,
            'history': self.history
        }

class Rule(Base, BaseRule):
    confidence = 0

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    text = Column(
        String(constants.USER_TEXT_MAX_LENGTH)
    )

    search_text = Column(
        String(constants.USER_TEXT_MAX_LENGTH),
        nullable=False,
        server_default=''
    )

    conversation = Column(
        String(constants.CONVERSATION_LABEL_MAX_LENGTH),
        nullable=False,
        server_default=''
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    tags = relationship(
        'Tag',
        secondary=lambda: tag_association_table,
        backref='rules'
    )

    in_response_to = Column(
        String(constants.USER_TEXT_MAX_LENGTH),
        nullable=True
    )

    search_in_response_to = Column(
        String(constants.USER_TEXT_MAX_LENGTH),
        nullable=False,
        server_default=''
    )

    persona = Column(
        String(constants.PERSONA_MAX_LENGTH),
        nullable=False,
        server_default=''
    )

    def get_tags(self):
        return [tag.name for tag in self.tags]

    def extend_tags(self, *tags):
        self.tags.extend([
            Tag(name=tag) for tag in tags
        ])
