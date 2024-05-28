from difflib import SequenceMatcher

'''
Source: https://www.baeldung.com/cs/levenshtein-distance-computation
'''

class Levenshtein:
    def __call__(self, text1, text2):
        if not text1 or not text2:
            return 0
        lower_text1, lower_text2 = str(text1).lower(), str(text2).lower()
        similarity = SequenceMatcher(None, lower_text1, lower_text2).ratio()
        return round(similarity, 2)

