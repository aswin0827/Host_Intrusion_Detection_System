rules_directory = './HIDSRules'
test_directory = './tests'
data_directory = './data'
rules_data_file = './data/rulesData.pkl'
automaton_data_file = './data/automaton.pkl'
parsed_rules_json_file = './data/parsedRules.json'
alerts_data_file = './data/alertsData.pkl'
all_alert_notification_data_file = './data/alertNotification.pkl'
userManagementDataFile = './data/userManagementData.pkl'

monitoring_files = {
    'windows': [
        r"C:\Windows\System32\config\SAM",
        r"C:\Windows\System32\config\SYSTEM",
        # Hosts file for network configurations.
        r"C:\Windows\System32\drivers\etc\hosts",
        r"C:\Windows\System32\winevt\Logs\Security.evtx",
        r"C:\Windows\System32\winevt\Logs\Application.evtx",
        r"C:\Windows\System32\winevt\Logs\System.evtx",
        r"C:\Windows\explorer.exe",
        r"C:\Windows\System32\winlogon.exe",
        r"C:\Windows\System32\services.exe",
        r"C:\Windows\System32\svchost.exe",
        r"C:\Windows\System32\ntoskrnl.exe",
        r"C:\Windows\System32\kernel32.dll",
        r"C:\Windows\System32\user32.dll",
        r"C:\Windows\System32\firewall.cpl",
        r"C:\Program Files\Common Files\System\masadc"
    ],
    'linux': [
        # User account information and passwords.
        "/etc/passwd",
        "/etc/shadow",
        "/etc/group",
        "/etc/sudoers",
        # Local network configuration.
        "/etc/hosts",
        # Authentication logs, including SSH login attempts.
        "/var/log/auth.log",
        # General system logs for various activities.
        "/var/log/syslog",
        # Kernel logs, capturing low-level system operations.
        "/var/log/kern.log",
        "/etc/crontab",
        "/etc/ssh/sshd_config",
        # Common directories for system binaries.
        "/bin/bash",
        "/bin/sh",
        "/sbin/init",
        "/lib/systemd/systemd",
        "/etc/ld.so.conf",
        "/etc/resolv.conf",
        "/etc/hosts.allow",
        "/etc/hosts.deny"
    ]
}

alertsObject = {
    'count':0,
    'defaultMessage':"Looks like more attack are happening check attacks."
}

userManagementData = {
    'email':"",
    'sendEmailAlerts':False
}