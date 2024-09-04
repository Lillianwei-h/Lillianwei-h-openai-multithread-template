# A template for multithread use of OpenAI's GPT api

This project is a template to enable multithread generation of OpenAI's gpt api.

## Preparation
1. Python environment
    I believe any python version >= 3.7 is supported. You can try it anyway.
2. Download dependencies
    ```bash
    pip install openai pyyaml argparse tqdm
    ```
3. Prepare your dataset
    The format should be:
    ```
    {
        "{id_1}": {
            "question": {question}, // question is a string
            "answer": {answer}, // (Optional) answer is a list of string, which can be both text and path of image, designed for eval mode
        },
        "{id_2}": {
            ...
        }
        ...
    }
    ```

## Customization
1. Put your api key (and maybe base url) in [gpt_config.yaml](./gpt_config.yaml). You can also change 'model' and 'max_tokens'.
2. (Optional)Set your own 'SYSTEM_PROMPT' in [data.py](./data.py).
3. (Optional)Set your answer's decoding rule in [decode_answer(line 62)](./data.py). You also need to pass `-d` or `--decode` to `main.py`.

## Usage
- **-t --thread_num**: The max number of threads. You can set it according to your pricing tier to avoid exceeding limit. By default is 1.
- **-i --input_path** : Input data file path. By default is "input.json".
- **-o --output_dir**: Output data dir. By default is './output'.
- **-m --mode**: Question mode. Currently only supports "ask" and "eval". By default is 'ask'.
- **-l --trucate_len**: Limit the length of your question set, 0 represents no truncating(designed for test). By default is 0.
- **-r --max_retries**: Limit the number of retrying when your request is denied. By default is 20.
- **-s --safemode**: (Recommended)Enable safemode, output to file each time an item is processed.
- **-d --decode**: (Very useful for answer in specified format)Decode response to abstruct answer(need to work with SYSTEM_PROMPT).
- **-v --verbose**: Print exceptions.

## Examples
### Ask mode
```bash
python main.py -t 10 -i 'YOUR_INPUT_PATH.json' -s
```

### Eval mode
 ```bash
python main.py -t 10 -i 'YOUR_INPUT_PATH.json' -m 'eval' -d -s
```



