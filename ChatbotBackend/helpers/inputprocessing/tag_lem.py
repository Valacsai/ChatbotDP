import string
import spacy

class TagLem:
    def __init__(self):
        self.punctuation_table = str.maketrans('', '', string.punctuation)
        self.nlp = spacy.load("en_core_web_sm")

    def get_root_word_tags(self, text):
        if len(text) <= 2:
            text = text.translate(self.punctuation_table)
        
        doc = self.nlp(text)
        filtered_tokens = [token for token in doc if token.is_alpha and not (len(text) > 2 and token.is_stop)]
        
        if len(filtered_tokens) < 2:
            filtered_tokens = [token for token in doc if token.is_alpha]
        
        if len(filtered_tokens) >= 2:
            bigram_pairs = [f'{filtered_tokens[i-1].pos_}:{filtered_tokens[i].lemma_.lower()}' for i in range(1, len(filtered_tokens))]
        else:
            bigram_pairs = [token.lemma_.lower() for token in filtered_tokens]
        
        return ' '.join(bigram_pairs)
