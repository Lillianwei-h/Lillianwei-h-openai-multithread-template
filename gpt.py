from openai import OpenAI
import yaml

with open('gpt_config.yaml', 'r') as file:
    config = yaml.safe_load(file)

if config['base_url'] is not None:
    client = OpenAI(api_key = config['api_key'], base_url = config['base_url'])
else:
    client = OpenAI(api_key = config['api_key'])

def ask_gpt(content):
    response = client.chat.completions.create(
        model = config['model'],
        messages=[
            {
                "role": "user",
                "content": content
            }
        ],
        max_tokens=config['max_tokens'],
    )
    return response.choices[0].message.content

