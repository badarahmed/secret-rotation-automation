import requests
import yaml
from datetime import datetime, timedelta

# Load secrets from YAML file
def load_secrets(file_path):
    with open(file_path, 'r') as file:
        secrets = yaml.safe_load(file)
    return secrets['secrets']

# Check if a secret is approaching its target date
def is_approaching_target_date(target_date, days_before=7):
    target_date = datetime.strptime(target_date, '%Y-%m-%d')
    return datetime.now() >= target_date - timedelta(days=days_before)

# Send Grafana Cloud alert
def send_grafana_alert(api_key, message):
    url = "https://api.grafana.com/api/alerts"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "message": message,
        "tags": {
            "severity": "critical"
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Main function to monitor secrets
def monitor_secrets(secrets_file, grafana_api_key, sla_days=7):
    secrets = load_secrets(secrets_file)
    for secret in secrets:
        if is_approaching_target_date(secret['target_date'], sla_days):
            send_grafana_alert(grafana_api_key, f"Secret {secret['name']} is approaching its target date.")

if __name__ == "__main__":
    SECRETS_FILE = 'secrets.yaml'
    GRAFANA_API_KEY = 'your_grafana_api_key'
    SLA_DAYS = 10

    monitor_secrets(SECRETS_FILE, GRAFANA_API_KEY, SLA_DAYS)
