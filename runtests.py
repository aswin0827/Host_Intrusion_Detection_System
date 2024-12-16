import configparser
import os
import logging
from constants import test_directory,automaton_data_file,rules_data_file
from dataFormatter import load_file
from automaton import search_logs
import re
import re

def remove_date_time(log_line):
    patterns = [
        r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[\+\-]\d{2}:\d{2})?', 
        r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:,\d{3})?',  
        r'\d{2} [A-Za-z]{3} \d{4} \d{2}:\d{2}:\d{2}',        
        r'\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}',             
        r'\[.*?\]',                                          
        r'\w{3} \d{1,2} \d{2} \d{2}:\d{2}:\d{2}',            
        r'\d{2} \w{3} \d{2} \d{2}:\d{2}:\d{2}',              
        r'\w{3} \d{1,2} \d{2} \d{2}:\d{2}:\d{2}',            
        r'\d{2} \w{3} \d{2} \d{2}:\d{2}:\d{2}',              
        r'\w{3} \d{2} \d{2}:\d{2}:\d{2}',                    
    ]
    
    
    combined_pattern = '|'.join(patterns)
    
    
    cleaned_log = re.sub(combined_pattern, '', log_line)
    
    
    cleaned_log = re.sub(r'\s+', ' ', cleaned_log).strip() 
    
    return cleaned_log

def setup_logging(log_file='test_failures.log'):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def parse_test_file(file_path):
    config = configparser.ConfigParser(allow_no_value=True, interpolation=None)
    config.read(file_path)

    tests = []
    for section in config.sections():
        test = {
            'name': section,
            'logs': [],
            'rule': config.get(section, 'rule', fallback=None),
            'alert': config.get(section, 'alert', fallback=None),
            'decoder': config.get(section, 'decoder', fallback=None)
        }
        for key, value in config.items(section):
            if key.startswith('log ') and key.endswith(' pass'):
                test['logs'].append(value)
        tests.append(test)
    return tests

def is_attack_detected(log_message, rules):
    output = []
    for rule in rules:
        for pattern in rule.patterns:
            try:
                compiled_pattern = re.compile(pattern)
            except re.error as e:
                # print(f"Error compiling pattern {pattern}: {str(e)}")
                continue
            if compiled_pattern.search(log_message):
                output.append(rule)
                # return True, rule
    return output

def run_tests(rules, test_directory):
    setup_logging()
    total_tests = 0
    detected_tests = 0
    not_matched = 0
    detected_and_not_matched = 0
    automaton = load_file(automaton_data_file)
    parsed_all_rules = load_file(rules_data_file)
    for filename in os.listdir(test_directory):
        if filename.endswith('.ini'):
            file_path = os.path.join(test_directory, filename)
            try:
                tests = parse_test_file(file_path)
            except Exception as e:
                print(f"Error parsing test file {filename}: {str(e)}")
                continue
            
            for test in tests:
                expected_rule_id = test['rule']
                expected_alert = int(test['alert']) if test['alert'] is not None else None

                for log in test['logs']:
                    flag = False
                    total_tests += 1
                    matches = search_logs(automaton,log)
                    log_message = (
                        f"Test failed: {test['name']}, File: {filename}\n"
                        f"Expected rule: {expected_rule_id}, Expected alert: {expected_alert}\n"
                        f"Log: {log}\n"
                    )
                    if matches:
                        detected_tests+=1
                        for match in matches:
                            log_message += f"Match found: Rule ID {match.id}, Description: {match.description}\n"
                            if match.id==expected_rule_id:
                                flag = True
                                break
                        if not flag:
                            detected_and_not_matched+=1
                    else:
                        log_message += "No rule detected\n"
                    if not flag:
                        logging.info(log_message)
                        not_matched+=1

    print(f"Total tests: {total_tests}")
    print(f"Detected tests: {detected_tests}")
    print(f"Not matched tests: {not_matched}")
    print(f"Detected but not matched tests: {detected_and_not_matched}")
    print(f"Accuracy: {detected_tests / total_tests * 100:.2f}%")
    
if __name__ == "__main__":
    parsed_all_rules = load_file(rules_data_file)
    run_tests(parsed_all_rules, test_directory)