import re
from collections import defaultdict
from constants import automaton_data_file
from dataFormatter import load_file
from alert import send_desktop_alert

def build_automaton(rules):
    automata = defaultdict(list)
    for rule in rules:
        for pattern in rule.patterns:
            try:
                words = re.findall(r'\b\w+\b', pattern)
                if not words:
                    first_char = next((c for c in pattern if c not in '^\\S+[]'), '')
                    automata[first_char].append((re.compile(pattern), rule))
                else:
                    for word in words:
                        automata[word].append((re.compile(pattern), rule))
            except re.error as e:
                print(f"Error in rule {rule.id}, pattern '{pattern}': {str(e)}")
                continue
    return automata

def search_logs(automaton, log):
    matched_rules = set()
    words = set(re.findall(r'\b\w+\b', log))
    
    for word in words:
        if word in automaton:
            for pattern,rule in automaton[word]:
                if pattern.search(log):
                    matched_rules.add(rule)
    return list(matched_rules)

def detect_attack(log,file):
    automaton = load_file(automaton_data_file)
    matched_rules = search_logs(automaton, log)
    if matched_rules:
        print(log)
        send_desktop_alert("Intrusion Alert", f"Potential intrusion detected in {file}! with log message: {log}",matched_rules)
    