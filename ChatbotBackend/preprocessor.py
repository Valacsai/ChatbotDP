import re

def remove_unnecessary_symbols(rule):
    rule.text = re.sub(r'[\n\r\t]+', ' ', rule.text).strip()
    rule.text = re.sub(' +', ' ', rule.text)
    return rule
