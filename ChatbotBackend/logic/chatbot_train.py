import os
from helpers.rule_model import Rule
import json

class ConversationTrainer:
    def __init__(self, chatbot, **kwargs):
        self.chatbot = chatbot

    def train(self, conversation):
        previous_rule_text = None
        previous_rule_search_text= ''
        rules_to_create = []
        for text in conversation:
            rule_search_text = self.chatbot.storage.tagger.get_root_word_tags(text)
            rule = self.chatbot.preprocessor(
                Rule(
                    text=text,
                    search_text=rule_search_text,
                    in_response_to=previous_rule_text,
                    search_in_response_to=previous_rule_search_text,
                    conversation='training'
                )
            )
            is_duplicate = self.chatbot.storage.find_rule_by_text(rule.text)
            previous_rule_text = rule.text
            previous_rule_search_text = rule_search_text
            if not is_duplicate:
                rules_to_create.append(rule)
        self.chatbot.storage.create_many_rules(rules_to_create)

    def parse_data(self, file_path):
        if (file_path.endswith('.json')):
            with open(file_path, 'r') as file:
                json_data = json.load(file)
                ordered_results = []
                for item in json_data:
                    values = list(item.values())[:2]
                    for value in values:
                        if isinstance(value, str):
                            ordered_results.append(value)
                        else:
                            ordered_results.append(str(value))
                return ordered_results
        elif file_path.endswith('.txt'):
            with open(file_path, 'r') as file:
                messages = [line.strip() for line in file.readlines()]
                return messages
        else:
            raise ValueError("Unsupported file type.")
    
    def process_files_in_folder(self):
        folder_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'training-data')
        files = os.listdir(folder_path)
        results = []
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                result = self.parse_data(file_path)
                results.extend(result) 
        return results