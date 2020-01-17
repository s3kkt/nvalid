import os
import configparser


def read_config(config_path):
    if not os.path.isfile(config_path):
        return None

    config = configparser.ConfigParser()
    config.read(config_path)
    try:
        local_config = {
            'metric_path': config.get('Monitoring', 'metrics_path'),
            'metric_name': config.get('Monitoring', 'metric_name'),
            'check_timeout': int(config.get('Monitoring', 'check_timeout')),
            'fail_timeout': int(config.get('Monitoring', 'fail_send_timeout')),
            'slack_chan': config.get('Slack', 'slack_channel'),
            'slack_url': config.get('Slack', 'slack_webhook_url')
        }
        return local_config
    except Exception as ex:
        print(f"execution failure: {str(ex)}")
        raise


MPATH = os.getenv('METRICS_PATH', '/var/lib/prometheus/')
MNAME = os.getenv('METRICS_NAME', 'nginx_config_status.prom')
TIMEOUT = int(os.getenv('CHECK_TIMEOUT', 5))
FTIMEOUT = int(os.getenv('FAIL_TIMEOUT', 300))
SLACK_CHAN = os.getenv("SLACK_CHANNEL")
SLACK_URL = os.getenv("SLACK_URL")

env_vars = {
    'metric_path': MPATH,
    'metric_name': MNAME,
    'check_timeout': TIMEOUT,
    'fail_timeout': FTIMEOUT,
    'slack_url': SLACK_URL,
    'slack_chan': SLACK_CHAN,
}
