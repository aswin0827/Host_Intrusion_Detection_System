import os
from dataFormatter import save_file,load_file,append_rules_to_json
from rules import parse_ossec_rules
from constants import rules_directory, rules_data_file,data_directory,alertsObject,all_alert_notification_data_file
from constants import parsed_rules_json_file,automaton_data_file,alerts_data_file,userManagementDataFile,userManagementData
from automaton import build_automaton
from fileMonitor import LogMonitor

if __name__ == '__main__':
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)
        
    if not os.path.exists(rules_data_file):
        parsed_all_rules = parse_ossec_rules(rules_directory)
        save_file(parsed_all_rules,rules_data_file)
    else:
        parsed_all_rules = load_file(rules_data_file)

    if not os.path.exists(parsed_rules_json_file):
        append_rules_to_json(parsed_rules_json_file,parsed_all_rules)

    if not os.path.exists(automaton_data_file):
        automaton = build_automaton(parsed_all_rules)
        save_file(automaton,automaton_data_file)
        
    if not os.path.exists(alerts_data_file):
        alerts_data = alertsObject
        save_file(alerts_data,alerts_data_file)
        
    if not os.path.exists(all_alert_notification_data_file):
        all_alert_notifications = []
        save_file(all_alert_notifications,all_alert_notification_data_file)
        
    if not os.path.exists(userManagementDataFile):
        save_file(userManagementData,userManagementDataFile)
        
    # create log monitor
    print("Monitoring logs for intrusion detection...")
    monitor = LogMonitor()    
    monitor.run()      
    