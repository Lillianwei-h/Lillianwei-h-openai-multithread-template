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
            if args.debug:
                print(e)
            if attempt == max_retries - 1:
                if args.debug:
                    print("Max retries reached. Exiting.")
            else:
                continue
    return response

def thread_worker(id, content):
    result = process(content['content'])
    content['gpt_answer'] = result
    content.pop('content', None)
    answer_dict[id] = content

    if args.decode:
        answer = decode_answer(result)
        answer_dict[id]['answer'] = answer
    with open(args.temp_output_path, 'w') as f:
        answer_list = [value for _,value in answer_dict.items()]
        json.dump(answer_list, f, indent = 4)

def process_with_limited_threads(content_dict, max_threads):
    with ThreadPoolExecutor(max_threads) as executor:
        futures = {executor.submit(thread_worker, key, value): key for key, value in content_dict.items()}
        for future in tqdm(futures, total=len(futures), desc="Processing"):
            future.result()

parser = argparse.ArgumentParser(description="An openai GPT multithread template")

# Important Args
parser.add_argument('-t', '--thread_num', type=int, default=1, help='The max number of threads')
parser.add_argument('-i', '--input_path', type=str, default='./data.json', help='Input data file path')
parser.add_argument('-o', '--output_dir', type=str, default='./output', help='Output data dir')
parser.add_argument('-m', '--mode', type=str, default='ans', choices=['ans','eval'], help='Different modes. Use ans to get answers from gpt. Use eval to get evaluations for answers from gpt')

# Using default settings is recommended
parser.add_argument('--trucate_len', type=int, default=0, help='Limit the length of your question set, 0 represents no truncating. Used for testing.')
parser.add_argument('--max_retries', type=int, default=20, help='Limit the number of retrying when your request is denied')
parser.add_argument('--debug', action='store_true', help="Enable debug")
parser.add_argument('--decode', action='store_true', help="Decode response to abstruct answer")


args = parser.parse_args()
print(args)
print(f"Input from: {args.input_path}")
print(f"Max thread: {args.thread_num}")

os.makedirs(args.output_dir, exist_ok=True)
os.makedirs(os.path.join(args.output_dir, "temp"), exist_ok=True)

args.input_dir = os.path.dirname(args.input_path)
args.input_file = os.path.basename(args.input_path)
args.output_path = os.path.join(args.output_dir, f"{args.mode}_{args.input_file}")
args.temp_output_path = os.path.join(args.output_dir, "temp", f"{args.mode}_{args.input_file}")

content_dict = get_data(args.input_path, trucate_len = args.trucate_len, mode = args.mode)
answer_dict = {}

process_with_limited_threads(content_dict, max_threads=args.thread_num)

with open(args.output_path, 'w') as f:
    answer_list = [value for _,value in answer_dict.items()]
    json.dump(answer_list, f, indent = 4)

print(f"Save output to: {args.output_path}")


