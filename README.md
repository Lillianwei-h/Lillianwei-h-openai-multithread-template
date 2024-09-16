# A template for multithread use of OpenAI's GPT api

This project is a template to enable multithread generation of OpenAI's gpt api.

## Preparation
### Python environment

I believe any python version >= 3.7 is supported. You can try it anyway.
### Download dependencies
```bash
pip install openai pyyaml argparse tqdm
```
### Prepare your dataset

The format should be:

```json
[
    {
        "id": id,
        "question": [
            {
                "text": "text",
                "image": "image"
            },
            ...
        ]
        "answer": [
            {
                "text": "text",
                "image": "image"
            },
            ...
        ]
    },
    ...
]
```

## Customization

### Set GPT config
Put your api key (and maybe base url) in [gpt_config.yaml](./gpt_config.yaml). You can also change 'model' and 'max_tokens'.

### Set SYSTEM_PROMPT
Write your own 'SYSTEM_PROMPT' in [data.py](./data.py).

### (Optional) Set answer decoding rule
Design your answer's decoding rule in [decode_answer(line 62)](./data.py). It is very useful for answer in specified format and need to work with SYSTEM_PROMPT. You also need to pass `--decode` when running `main.py`.

## Usage
- **-t --thread_num**: The max number of threads. You can set it according to your pricing tier to avoid exceeding limit. By default is 1.
- **-i --input_path** : Input data file path. By default is "./data.json".
- **-o --output_dir**: Output data dir. By default is './output'.
- **-m --mode**: Question mode. Currently only supports "ans" and "eval". By default is 'ans'.
- **--trucate_len**: Limit the length of your question set, 0 represents no truncating(designed for test). By default is 0.
- **--max_retries**: Limit the number of retrying when your request is denied. By default is 20.
- **--decode**: Decode response to abstruct answer.
- **--debug**: Print exceptions.

## Examples
### Ask mode
```bash
python main.py -t 10 -i 'YOUR_INPUT_PATH.json'
```

### Eval mode
 ```bash
python main.py -t 10 -i 'YOUR_INPUT_PATH.json' -m 'eval' --decode
```



