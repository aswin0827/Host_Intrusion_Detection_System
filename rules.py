import xml.etree.ElementTree as ET
import os

class Rule:
    def __init__(self, id, level, description, category, patterns=None):
        self.id = id
        self.level = int(level) if level else 0
        self.description = description
        self.category = category
        self.patterns = patterns or []
        
    def to_dict(self):
        return {
            'id': self.id,
            'level': self.level,
            'description': self.description,
            'category': self.category,
            'patterns': self.patterns
        }
        
    def __str__(self) -> str:
        return f"Rule ID: {self.id}, Description: {self.description}, Level: {self.level}, Category: {self.category}"

def parse_ossec_rules(directory):
    all_rules = []
    for filename in os.listdir(directory):
        if filename.endswith('.xml'):
            file_path = os.path.join(directory, filename)
            try:
                rules = parse_single_file(file_path)
                all_rules.extend(rules)
            except Exception as e:
                print(f"Error parsing file {filename}: {str(e)}")
    return all_rules

def parse_single_file(file_path):
    rules = []
    with open(file_path, 'r') as file:
        content = file.read()
        wrapped_xml_content = f"<root>{content}</root>"
        root = ET.fromstring(wrapped_xml_content)
        for group_elem in root.findall('.//group'):
            category = group_elem.get('name', '')
        
            for rule_elem in group_elem.findall('.//rule'):
                rule_id = rule_elem.get('id')
                level = rule_elem.get('level')
                description = rule_elem.find('description').text if rule_elem.find('description') is not None else ''
                
                patterns = []
                for pattern_elem in rule_elem.findall('.//pcre2'):
                    if pattern_elem.text:
                        # cleaned_pattern = pattern_elem.text.strip().replace('|', '').replace('^$', '')
                        # if cleaned_pattern:
                        cleaned_pattern = pattern_elem.text.strip().rstrip('|')
                        if cleaned_pattern:
                            patterns.append(cleaned_pattern)
                if patterns:
                    rules.append(Rule(rule_id, level, description, category, patterns))
    return rules