class TextSearch:
    def __init__(self, chatbot, **kwargs):
        from helpers.levenshtein import Levenshtein
        self.chatbot = chatbot
        self.rule_comparison_function = Levenshtein()

    def search(self, input_rule, **add_filter_params):
        input_search_text = input_rule.search_text
        if not input_rule.search_text:
            input_search_text = self.chatbot.storage.tagger.get_root_word_tags(input_rule.text)
        filter_parameters = {'search_text_contains': input_search_text, 'persona_not_startswith': 'bot:'}
        if add_filter_params:
            filter_parameters.update(add_filter_params)
        filtered_rules = self.chatbot.storage.filter_rules(**filter_parameters)
        highest_confidence = 0
        for rule in filtered_rules:
            confidence = self.rule_comparison_function(input_rule, rule)
            if confidence > highest_confidence:
                highest_confidence = confidence
                rule.confidence = confidence
                yield rule

    def find_answer_from_adapter(self, input_rule, additional_params=None):
        Rule = self.storage.get_object('rule')
        output = self.adapter.process(input_rule, additional_params)
        response = Rule(
            text=output.text,
            in_response_to=input_rule.text,
            conversation=input_rule.conversation,
            persona=f'bot:{self.name}',
            confidence=output.confidence
        )
        return response