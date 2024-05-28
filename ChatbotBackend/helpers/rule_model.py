from datetime import datetime

class BaseRule:
    base_fields = [
        'id', 'text', 'search_text', 'conversation', 'persona',
        'tags', 'in_response_to', 'search_in_response_to', 'created_at'
    ]

    additional_fields = []

    def get_fields(self):
        return self.base_fields + self.additional_fields
        
    def get_tags(self):
        return self.tags

    def extend_tags(self, *tags):
        self.tags.extend(tags)

    def serialize(self):
        serialized_data = {}
        for field in self.get_fields():
            value_getter = getattr(self, f'get_{field}', None)
            serialized_data[field] = value_getter() if value_getter else getattr(self, field, None)
        return serialized_data

class Rule(BaseRule):
    __slots__ = (
        'id', 'text', 'search_text', 'conversation', 'persona', 'tags',
        'in_response_to', 'search_in_response_to', 'created_at',
        'confidence', 'storage'
    )

    def __init__(self, text, in_response_to=None, **kwargs):
        self.id = kwargs.get('id')
        self.text = text
        self.search_text = kwargs.get('search_text', '')
        self.conversation = kwargs.get('conversation', '')
        self.persona = kwargs.get('persona', '')
        self.tags = kwargs.get('tags', [])
        self.in_response_to = in_response_to
        self.search_in_response_to = kwargs.get('search_in_response_to', '')
        self.created_at = datetime.now()
        self.confidence = 0
        self.storage = None

    def __str__(self):
        return self.text

    def __repr__(self):
        return f'<rule text:{self.text}>'

    def save(self):
        if self.storage:
            self.storage.update_rule(self)
