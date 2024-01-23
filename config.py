import json
from config import Config , load_config , conf

with open('plugins/chatgpt-on-wechat-weaviate-plugin/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
print(config)  # Add this line
weaviate_url = config['weaviate_url']
weaviate_key = config['weaviate_key']
