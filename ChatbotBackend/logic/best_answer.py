from logic.search import TextSearch
from helpers.rule_model import Rule
from collections import Counter

class BestAnswer:
    def __init__(self, chatbot, **kwargs):
        self.chatbot = chatbot
        self.search_algorithm = TextSearch(self.chatbot)
        self.maximum_similarity_threshold = 0.95
        default_responses = kwargs.get('default_response', [])
        if isinstance(default_responses, str):
            default_responses = [default_responses]
        self.default_responses = [Rule(text=response) for response in default_responses]
        self.excluded_words = kwargs.get('excluded_words')

    def is_processable(self, rule):
        return True

    def choose_default_response(self, input_rule):
        from random import choice
        try:
            return choice(self.default_responses) if self.default_responses else self.chatbot.storage.get_random_rule()
        except Exception:
            chosen_response = input_rule
            chosen_response.confidence = 0
            return chosen_response

    def get_latest_common_responses(self, conversation, sample=10, threshold=3, quantity=3):
        recent_rules = list(self.chatbot.storage.filter_rules(conversation=conversation, order_by=['id']))[-sample:]
        recent_responses = [rule.text for rule in recent_rules]
        response_counts = Counter(recent_responses)
        common_responses = [response for response, count in response_counts.most_common(quantity) if count >= threshold]
        return common_responses

    def process(self, input_rule, additional_response_selection_parameters=None):
        search_results = self.search_algorithm.search(input_rule)
        closest_match = next(search_results, input_rule)
        for result in search_results:
            closest_match = result
            if result.confidence >= self.maximum_similarity_threshold:
                break
        recent_repeated_responses = self.get_latest_common_responses(input_rule.conversation)
        response_selection_parameters = { 'search_in_response_to': closest_match.search_text, 'exclude_text': recent_repeated_responses, 'exclude_text_words': self.excluded_words }
        alternate_response_selection_parameters = { 'search_in_response_to': self.chatbot.storage.tagger.get_root_word_tags(input_rule.text), 'exclude_text': recent_repeated_responses, 'exclude_text_words': self.excluded_words }
        if additional_response_selection_parameters:
            response_selection_parameters.update(additional_response_selection_parameters)
            alternate_response_selection_parameters.update(additional_response_selection_parameters)
        response_list = list(self.chatbot.storage.filter_rules(**response_selection_parameters))
        alternate_response_list = []
        if not response_list:
            alternate_response_list = list(self.chatbot.storage.filter_rules(**alternate_response_selection_parameters))
        if response_list:
            response = response_list[0]
            response.confidence = closest_match.confidence
        elif alternate_response_list:
            response = alternate_response_list[0]
            response.confidence = closest_match.confidence
        else:
            response = self.choose_default_response(input_rule)
        return response
