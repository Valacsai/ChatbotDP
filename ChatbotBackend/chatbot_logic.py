from logic.search import TextSearch
from logic.best_answer import BestAnswer
import helpers.utils as utils

class ChatBot(object):
    def __init__(self, name, **kwargs):
        self.name = name
        self.storage = kwargs.get('storage')
        preprocessor = kwargs.get('preprocessor','preprocessor.remove_unnecessary_symbols')
        self.adapter = BestAnswer(self)
        self.preprocessor = utils.import_module(preprocessor)
        self.chatbot_learn = kwargs.get('chatbot_learn', False)

    def find_answer(self, rule=None, **kwargs):
        Rule = self.storage.get_object('rule')
        last_bot_message = ''
        if rule['lastBot'] != "Empty":
            last_bot_message = rule['lastBot']
        rule = rule['user']
        add_params = kwargs.pop('additional_response_selection_parameters', {})
        match rule:
            case str():
                kwargs['text'] = rule
            case dict():
                kwargs.update(rule)
            case _ if hasattr(rule, 'serialize'):
                kwargs.update(rule.serialize())
        text = kwargs.pop('text', None)
        if text is None:
            return "Error: Empty input string"
        input_text_rule = Rule(text=text, **kwargs)
        input_text_rule = self.preprocessor(input_text_rule)
        if not input_text_rule.search_text:
            input_text_rule.search_text = self.storage.tagger.get_root_word_tags(input_text_rule.text)
        if not input_text_rule.search_in_response_to and input_text_rule.in_response_to:
            input_text_rule.search_in_response_to = self.storage.tagger.get_root_word_tags(input_text_rule.in_response_to)
        response = TextSearch.find_answer_from_adapter(self, input_text_rule, add_params)
        if self.chatbot_learn:
            input_text_rule.in_response_to = last_bot_message
            self.storage.learn(input_text_rule)
        return response