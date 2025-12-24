import json
import os

# Get the path to the config file (two levels up from backend/config)
config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'app_config.json')

# Load the configuration
with open(config_path, 'r', encoding='utf-8') as f:
    CONFIG = json.load(f)

# Common config
COMMON_CONFIG = CONFIG['common']

# Zhongkao specific config
ZHONGKAO_CONFIG = CONFIG['zhongkao']

def format_page_indicator(current, total):
    """Format the page indicator text"""
    return COMMON_CONFIG['navigation']['pageIndicator'].replace('{current}', str(current)).replace('{total}', str(total))