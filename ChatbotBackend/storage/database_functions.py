from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from storage.tables import MessageHistory
from helpers.inputprocessing.tag_lem import TagLem
class DatabaseFunctions:
    def __init__(self, **kwargs):
        self.database_uri = 'sqlite:///mydatabase.db'
        self.engine = create_engine(self.database_uri)
        Tagger = kwargs.get('tagger', TagLem)
        self.tagger = Tagger()
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=True)

    def get_rule_model(self):
        from storage.tables import Rule
        return Rule
    
    def get_message_history_model(self):
        from storage.tables import MessageHistory
        return MessageHistory
    
    def get_model(self, model_name):
        get_model_method = getattr(self, 'get_%s_model' % (
            model_name.lower()
        ))
        return get_model_method()
    
    def get_object(self, object_name):
        get_model_method = getattr(self, 'get_%s_object' % (
            object_name.lower()
        ))
        return get_model_method()
    
    def get_rule_object(self):
        from helpers.rule_model import Rule
        return Rule

    def get_tag_model(self):
        from storage.tables import Tag
        return Tag

    def model_to_object(self, rule):
        from helpers.rule_model import Rule as ruleObject
        return ruleObject(**rule.serialize())

    def count_rules(self):
        Rule = self.get_model('rule')
        session = self.Session()
        rule_count = session.query(Rule).count()
        session.close()
        return rule_count

    def remove_rule(self, rule_text, id=0):
        Rule = self.get_model('rule')
        session = self.Session()
        if (id != 0):
            query = session.query(Rule).filter_by(id=id)
            record = query.first()
        else:
            query = session.query(Rule).filter_by(text=rule_text)
            record = query.first()
        session.delete(record)
        self._session_finish(session)

    def find_rule_by_text(self, rule_text):
        Rule = self.get_model('rule')
        session = self.Session()
        query = session.query(Rule).filter_by(text=rule_text)
        record = query.first()
        return record

    def filter_rules(self, **kwargs):
        from sqlalchemy import or_
        Rule = self.get_model('rule')
        Tag = self.get_model('tag')
        session = self.Session()
        page_size = kwargs.pop('page_size', 1000)
        order_by = kwargs.pop('order_by', None)
        tags = kwargs.pop('tags', [])
        exclude_text = kwargs.pop('exclude_text', None)
        exclude_text_words = kwargs.pop('exclude_text_words', [])
        persona_not_startswith = kwargs.pop('persona_not_startswith', None)
        search_text_contains = kwargs.pop('search_text_contains', None)
        if type(tags) == str:
            tags = [tags]
        if len(kwargs) == 0:
            rules = session.query(Rule).filter()
        else:
            rules = session.query(Rule).filter_by(**kwargs)
        if tags:
            rules = rules.join(Rule.tags).filter_rules(
                Tag.name.in_(tags)
            )
        if exclude_text:
            rules = rules.filter(
                ~Rule.text.in_(exclude_text)
            )
        if exclude_text_words:
            or_word_query = [
                Rule.text.ilike('%' + word + '%') for word in exclude_text_words
            ]
            rules = rules.filter(
                ~or_(*or_word_query)
            )
        if persona_not_startswith:
            rules = rules.filter(
                ~Rule.persona.startswith('bot:')
            )
        if search_text_contains:
            or_query = [
                Rule.search_text.contains(word) for word in search_text_contains.split(' ')
            ]
            rules = rules.filter(
                or_(*or_query)
            )
        if order_by:
            if 'created_at' in order_by:
                index = order_by.index('created_at')
                order_by[index] = Rule.created_at.asc()
            rules = rules.order_by(*order_by)
        total_rules = rules.count()
        for start_index in range(0, total_rules, page_size):
            for rule in rules.slice(start_index, start_index + page_size):
                yield self.model_to_object(rule)
        session.close()

    def create_rule(self, **kwargs):
        Rule = self.get_model('rule')
        session = self.Session()
        if 'search_text' not in kwargs:
            kwargs['search_text'] = self.tagger.get_root_word_tags(kwargs['text'])
        if 'search_in_response_to' not in kwargs:
            in_response_to = kwargs.get('in_response_to')
            if in_response_to:
                kwargs['search_in_response_to'] = self.tagger.get_root_word_tags(in_response_to)
        rule = Rule(**kwargs)
        session.add(rule)
        session.flush()
        session.refresh(rule)
        rule_object = self.model_to_object(rule)
        self._session_finish(session)
        return rule_object

    def create_many_rules(self, rules):
        Rule = self.get_rule_model()
        session = self.Session()
        create_rules = []
        for rule in rules:
            rule_data = rule.serialize()
            rule_model_object = Rule(**rule_data)
            if not rule.search_text:
                rule_model_object.search_text = self.tagger.get_root_word_tags(rule.text)
            if not rule.search_in_response_to and rule.in_response_to:
                rule_model_object.search_in_response_to = self.tagger.get_root_word_tags(rule.in_response_to)
            create_rules.append(rule_model_object)
        session.add_all(create_rules)
        session.commit()

    def update_rule(self, rule):
        Rule = self.get_model('rule')
        if rule is not None:
            session = self.Session()
            record = None
            if hasattr(rule, 'id') and rule.id is not None:
                record = session.query(Rule).get(rule.id)
            else:
                record = session.query(Rule).filter(
                    rule.text == rule.text,
                    rule.conversation == rule.conversation,
                ).first()
                if not record:
                    record = Rule(
                        text=rule.text,
                        conversation=rule.conversation,
                        persona=rule.persona
                    )
            record.in_response_to = rule.in_response_to
            record.created_at = rule.created_at
            record.search_text = self.tagger.get_root_word_tags(rule.text)
            if rule.in_response_to:
                record.search_in_response_to = self.tagger.get_root_word_tags(rule.in_response_to)
            session.add(record)
            self._session_finish(session)

    def get_random_rule(self):
        import random
        Rule = self.get_model('rule')
        session = self.Session()
        count = self.count_rules()
        if count < 1:
            raise self.EmptyDatabaseException()
        random_index = random.randrange(0, count)
        random_rule = session.query(Rule)[random_index]
        rule = self.model_to_object(random_rule)
        session.close()
        return rule

    def drop_tables(self):
        Rule = self.get_model('rule')
        Tag = self.get_model('tag')
        MessageHistory = self.get_model('message_history')
        session = self.Session()
        session.query(Rule).delete()
        session.query(Tag).delete()
        session.query(MessageHistory).delete()
        session.commit()
        session.close()

    def create_database(self):
        from storage.tables import Base
        Base.metadata.create_all(self.engine)

    def create_history(self, history_entries):
        session = self.Session()
        try:
            new_history_record = MessageHistory(history=history_entries)
            session.add(new_history_record)
            session.commit()
            return new_history_record.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update_history(self, record_id, new_history):
        session = self.Session()
        try:
            history_record = session.query(MessageHistory).filter_by(id=record_id).first()
            if history_record:
                history_record.history = new_history
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_history(self, record_id):
        session = self.Session()
        try:
            return session.query(MessageHistory).filter_by(id=record_id).first()
        finally:
            session.close()

    def get_all_histories(self):
        session = self.Session()
        try:
            return session.query(MessageHistory).all()
        finally:
            session.close()

    def delete_history(self, record_id):
        session = self.Session()
        try:
            history_record = session.query(MessageHistory).filter_by(id=record_id).first()
            if history_record:
                session.delete(history_record)
                session.commit()
                return True
            else:
                return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_last_messages(self, conversation):
        from helpers.rule_model import Rule as RuleObject
        conversation_rules = list(self.filter_rules(
            conversation=conversation,
            order_by=['id']
        ))
        latest_rule = conversation_rules[-1] if conversation_rules else None
        if conversation_rules:
            if latest_rule.text:
                response_rules = list(self.filter_rules(
                    conversation=conversation,
                    text=latest_rule.text,
                    order_by=['id']
                ))
                if response_rules:
                    return response_rules[-1]
                return RuleObject(
                    text=latest_rule.text,
                    conversation=conversation
                )
            return latest_rule
        return None
    
    def learn(self, rule, previous_rule=None):
        if not previous_rule:
            previous_rule = rule.in_response_to if rule.in_response_to else self.get_last_messages( rule.conversation)
        if isinstance(previous_rule, str):
            rule.in_response_to = previous_rule
        elif hasattr(previous_rule, 'in_response_to'):
            rule.in_response_to = previous_rule.text
        rule.search_in_response_to = self.tagger.get_root_word_tags(rule.in_response_to)
        return self.create_rule(**rule.serialize())

    def _session_finish(self, session, rule_text=None):
        try:
            session.commit()
        finally:
            session.close()