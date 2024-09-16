import json
import base64
import os
import re

# write your system prompt below
SYSTEM_PROMPT = '''You are a helpful assistant.'''

# An example of evaluating prompt
# SYSTEM_PROMPT = '''### Instruction
# You are an assistant who can evaluate the quality of an answer to a given question. As the answer may contain both text and images, you will need to evaluate the following five aspects.
# - Text Quality
#     Text quality measures how clear, coherent, and error-free the output text is. It considers grammar, spelling, readability, coherence with the instruction and context, and whether it contains duplicate content.
# - Perceptual Quality
#     Perceptual quality measures how visually convincing, natural, and free from distortions or artifacts a generated image appears. It considers how accurately the image mimics reality without unnatural disruptions in structure, colors, or composition.
# - Image Coherence
#     Image coherence measures the consistency in style and subject representation across images. This includes textures, color palette, lighting, rendering styles, and maintaining consistent physical attributes, clothing, and behavioral traits. Image coherence also penalizes image duplication, where the output images are too similar, or within the output images themselves.
# - Text-Image Coherence
#     Text-to-image coherence measure the alignment and integration between textual and visual elements in a pairwise manner, ensuring they work together to convey a unified and cohesive narrative.
# - Helpfulness
#     Helpfulness measures how well the output text and images follow the task instructions and provide complete information to achieve the task. It also considers whether the outputs follow a reasonable logic flow.
# Then I will give you the question and the answer. Each aspect is worth 1 point. Adding them up will give you the final score. You must briefly explain your scoring procedure for each aspect. You should give your final answer in this format: <SCORE: {score}>. Where '{score}' is the final score of the answer, ranging from 0 to 5.
# '''

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def process_asking_content(d, all_dict, mode):
    question = d['question']
    content = []
    content.append({"type": "text", "text": f"### Question:\n"})
    for q in question:
        if q['text'] is not None:
            content.append({"type": "text", "text": q['text']})
        if q['image'] is not None:
            if os.path.exists(q['image']):
                base64_image = encode_image(q['image'])
                content.append({"type": "image_url","image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}})
            else:
                print(f"File {q['image']} doesn't exist.")

    if mode == "eval":
        answer = d['answer']
        content.append({"type": "text", "text": f"### Answer:\n"})
        for a in answer:
            if a['text'] is not None:
                content.append({"type": "text", "text": a['text']})
            if a['image'] is not None:
                if os.path.exists(a['image']):
                    base64_image = encode_image(a['image'])
                    content.append({"type": "image_url","image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}})
                else:
                    print(f"File {a['image']} doesn't exist.")

    all_dict[d['id']]['content'] = content

def get_data(filepath, trucate_len = None, mode = "ans"):
    with open(filepath, 'r') as f:
        data = json.load(f)
    if trucate_len is not None:
        data = data[:trucate_len]

    all_dict = {}
    for _ in len(data):
        all_dict[d['id']] = {}
    for d in data:
        process_asking_content(d, all_dict, mode)

    return all_dict

def decode_answer(answer):
    match = re.search(r'<SCORE:\s*([-+]?\d*\.?\d+)>', answer) # change it to fit your own rule
    if match:
        return float(match.group(1))
    else:
        return None
