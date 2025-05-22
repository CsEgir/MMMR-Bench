import re
import os
import json
from tqdm import tqdm
import argparse
import sys
import torch
import time
import os
import base64
sys.path.append('/mnt/zeli/LRM_Benchmark')

# Ensure CUDA_VISIBLE_DEVICES is set
os.environ['CUDA_VISIBLE_DEVICES'] = '1'
print("CUDA是否可用:", torch.cuda.is_available())
print("可用的GPU数量:", torch.cuda.device_count())
for i in range(torch.cuda.device_count()):
    print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
 
def process_images_to_base64(image_urls):
    """将图片文件转换为base64编码"""
    base64_images = []
    
    for image_url in image_urls:
        try:
            # 确保路径使用正确的分隔符
            image_path = image_url.replace('\\', '/')
            
            # 检查文件是否存在
            if not os.path.exists(image_path):
                print(f"文件不存在: {image_path}")
                continue
                
            # 读取图片文件并转换为base64
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode("utf-8")
                base64_images.append(base64_image)
                #print(f"成功处理: {image_path}")
                
        except Exception as e:
            print(f"处理文件 {image_path} 时出错: {e}")
    
    return base64_images

def extract_outputs(json_file_path):
    outputs = []
    
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
        # 检查 'results' 键是否存在且是一个列表
        if 'results' in data and isinstance(data['results'], list):
            for idx, result in enumerate(data['results']):
                output = result.get('output')
                if output:
                    outputs.append(output)
                else:
                    print(f"警告: 'output' 在结果索引 {idx} 中不存在。")
        else:
            print("错误: JSON 中缺少 'results' 键或其格式不正确。")
    
    total_token_count = sum(len(o.split()) for o in outputs)
    
    return outputs, total_token_count


class Prompt_based:
    def __init__(
        self, 
        model, 
        task=None
    ):
        self.model = model
        self.task = task
        #self.thinking_outputs = thinking_outputs if thinking_outputs else []

    def get_answer(self, output):
        """
        Extracts the answer from the model's output. It looks for the pattern \boxed{answer}.
        """
        answer = re.findall(r'\\boxed{(.+?)}', output)
        #answer = extract_boxed_content(output)
        if answer:
            # 尝试转换为数字
            try:
                return int(answer[0])
            except ValueError:
                try:
                    return float(answer[0])
                except ValueError:
                    return answer[0]  # 如果不是数字，就返回原字符串
        else:
            return None  # 表示没有找到答案

    def __call__(self, question, answer,output,i):
        
        prompt_based = "Please provide the final answer and store it in \\boxed{answer}.Please think deeply before your response."
        # few_shot = ''
        initial_input = output + '\n\n' + prompt_based

        content_reasoning,content,rt = self.model.query(initial_input)
        
        final_answer = self.get_answer(output)
                
        record = {}
        record['original_question'] = question
        record['processed_question'] = output
        record['reasoning_output'] = content_reasoning
        record['output'] = content
        # record['img_url'] = img_url
        record['running_time'] = rt
        record['final_answer'] = final_answer
        record['correct_answer'] = answer
        
        print("-----------------------------------------")
        print(f"final_answer: {final_answer}")
        print(f"correct_answer: {answer}")
        print("-----------------------------------------")
        
        if final_answer is None:
            record['correct'] = False
            record['error'] = 'No boxed answer found'
        elif str(final_answer) == str(answer):
            record['correct'] = True
        else:
            record['correct'] = False

        if not record.get('correct', False):
            record['error'] = 'Final answer and answer do not match'
        return record,rt


def test_and_save(args):
    """
    1. 加载模型
    2. 加载 single task 配置文件 (从 --task_config_file，而不是目录)
    3. 如果指定 --extra_json，则提取其中的 output 并统计 token 数，作为 thinking 传给 Prompt_based
    4. 逐条处理问题并保存结果
    """
    from utils.process_config import open_config
    from model import create_model


    start_time = time.time()


    model_config = open_config(config_path=args.model_config)
    model = create_model(model_config)

    if not os.path.isfile(args.task_config_file):
        print(f"[Error] {args.task_config_file} is not a valid file.")
        return

    with open(args.task_config_file, 'r') as f:
        task_data = json.load(f)
    # print(task_data)
    task_data = task_data.get('results', task_data)  # 处理不同格式的 JSON 文件
    task_name = os.path.splitext(os.path.basename(args.task_config_file))[0]
    print(f"\nProcessing Task: {task_name}")

    for item in task_data:
        if "question'" in item:
            item["question"] = item.pop("question'")

    questions = [item["question"] for item in task_data]
    correct_answers = [item["correct_answer"] for item in task_data]
    outputs = [item["output"] for item in task_data]
    # img_urls = [item["image_url"] for item in task_data]


    method = Prompt_based(
        model, 
        task=None
    )

    test_num = args.test_num

    start_idx = args.start
    end_idx = args.end if args.end is not None else (len(questions) - 1)

    # 确保索引不越界
    end_idx = min(end_idx, len(questions) - 1)
    test_num = end_idx - start_idx + 1  # 实际处理的数量
    results_file = args
    os.makedirs(os.path.dirname(results_file), exist_ok=True)

    print(f"Processing data from {start_idx} to {end_idx}, total {test_num} samples")
    print(f"Results will be saved to {results_file}")

    print(f"Making a new file {results_file} to save the result.")

    final_results = []
    correct_number = 0
    total_number = len(questions)
    #test_num = 1
    empty_answer_count = 0
    for i in tqdm(range(start_idx, end_idx + 1), desc=f"Processing {task_name} questions"):
        question = questions[i]
        answer = correct_answers[i]
        output = outputs[i]
        # img_url = img_urls[i]
        # base64_images = process_images_to_base64(img_url)
        # print(base64_images[0])
        record,running_time = method(question, answer, output, i)
        final_results.append(record)
        
        if record.get('correct', False):
            correct_number += 1
        if record.get('final_answer') is None:
            empty_answer_count += 1


        answered_count = (i + 1 - empty_answer_count)
        ACC = correct_number / answered_count if answered_count > 0 else 0
        

        results_dict = {
            "results": final_results
        }

        with open(results_file, 'w') as f:
            json.dump(results_dict, f, indent=4)


    end_time = time.time()
    total_time = end_time - start_time

    print(f"Method: {args.method}")
    print(f"Task: {task_name}")
    print(f"Model: {model.name}")
    # print(f"Thinking token count: {thinking_token_count}")
    print(f"Number of questions with empty answers: {empty_answer_count}")
    print(f"Total runtime: {total_time:.2f} seconds")

    results_dict["time"] = total_time
    with open(results_file, 'w') as f:
        json.dump(results_dict, f, indent=4)

    print(f"Results saved to {results_file}")


def main():
    parser = argparse.ArgumentParser(description="Prompt-based Testing and Saving Script for a Single Task")
    parser.add_argument('--model_config', type=str, default="",
                        help='Path to the model configuration file.')
    parser.add_argument('--task_config_file', type=str,default="",
                        help='Path to the single task JSON file (contains questions & images & answers).')
    parser.add_argument('--method', type=str, default='generated',
                        help='Method name to use.')
    parser.add_argument('--test_num', type=int, default=1,
                        help='test number of the dataset.')     
    parser.add_argument('--results_file', type=str, default="",
                        help='the results path.')                    
    parser.add_argument('--start', type=int, default=0)
    parser.add_argument('--end', type=int, default=None)

    args = parser.parse_args()

    test_and_save(args)


if __name__ == "__main__":
    main()

    #python Based_prompt.py --model_config /mnt/zeli/LRM_Benchmark/config/model_config/google/gemini-2.5-pro-exp-03-25:free_config.json --task_config_file /mnt/zeli/LRM_Benchmark/dataset/Logic_puzzle/MMRU-Logic/2D.json --test_num 96
    #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
