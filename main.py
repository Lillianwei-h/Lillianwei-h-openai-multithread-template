import json
from concurrent.futures import ThreadPoolExecutor
import argparse
from tqdm import tqdm
from data import get_data, decode_answer
from gpt import ask_gpt
import os

def process(content):
    response = ""
    max_retries = args.max_retries
    for attempt in range(max_retries):
        try:
            response = ask_gpt(content)
            break
        except Exception as e:
            if args.verbose:
                print(e)
            if attempt == max_retries - 1:
                if args.verbose:
                    print("Max retries reached. Exiting.")
            else:
                continue
    return response

def thread_worker(id, content):
    result = process(content['content'])
    answer_dict[id]['response'] = result
    if args.decode:
        answer = decode_answer(result)
        answer_dict[id]['answer'] = answer
    if args.safemode:
        with open(args.output_file, 'w') as f:
            json.dump(answer_dict, f, indent = 4)

def process_with_limited_threads(content_dict, max_threads):
    with ThreadPoolExecutor(max_threads) as executor:
        futures = {executor.submit(thread_worker, key, value): key for key, value in content_dict.items()}
        for future in tqdm(futures, total=len(futures), desc="Processing"):
            future.result()

parser = argparse.ArgumentParser(description="An openai GPT multithread template")
parser.add_argument('-t', '--thread_num', type=int, default=1, help='The max number of threads')
parser.add_argument('-i', '--input_path', type=str, default='input.json', help='Input data file path')
parser.add_argument('-o', '--output_dir', type=str, default='./output', help='Output data dir')
parser.add_argument('-m', '--mode', type=str, default='ask', help='Asking mode of GPT. Currently only supports <ask> and <eval>')
parser.add_argument('-l', '--trucate_len', type=int, default=0, help='Limit the length of your question set, 0 represents no truncating')
parser.add_argument('-r', '--max_retries', type=int, default=20, help='Limit the number of retrying when your request is denied')
parser.add_argument('-d', '--decode', action='store_true', help="Decode response to abstruct answer")
parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose")
parser.add_argument('-s', '--safemode', action='store_true', help="Enable safemode, output each time when an item is processed")

args = parser.parse_args()

print(f"Input from: {args.input_path}")
print(f"Max thread: {args.thread_num}")
os.makedirs(args.output_dir, exist_ok=True)
args.output_path = os.path.join(args.output_dir, ("answer_" + args.input_path))

content_dict = get_data(args.input_path, trucate_len = args.trucate_len, mode = args.mode)
answer_dict = {}

process_with_limited_threads(content_dict, max_threads=args.thread_num)

with open(args.output_file, 'w') as f:
    json.dump(answer_dict, f, indent = 4)

print(f"Output to: {args.output_file}")


