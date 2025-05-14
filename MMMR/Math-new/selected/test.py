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
    """
    从给定的 JSON 文件中提取所有 "output" 值并返回一个列表，
    同时计算这些 output 的总 token 数（使用空格简单切分）。
    
    参数:
    - json_file_path (str): JSON 文件的路径。

    返回:
    - Tuple[List[str], int]: (outputs 列表, outputs 总 token 数).
    """
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
        task=None, 
        prompting_style='zero-shot-cot', 
        correct_iteration=1, 
        #thinking_outputs=None
    ):
        self.model = model
        self.task = task
        self.prompting_style = prompting_style
        self.correct_iteration = correct_iteration
        self.initial_prompt = self.get_initial_prompt()
        self.critique_prompt = 'Review your previous answer and find problems with your answer.\n\n'
        self.improve_prompt = (
            'Based on the problems you found, improve your answer. '
            'in the form \\boxed{answer}.\n\n'
        )
        # 用于存放从 extra_json 中提取出的 output 作为 thinking
        #self.thinking_outputs = thinking_outputs if thinking_outputs else []

    def get_initial_prompt(self):
        if self.prompting_style == 'zero-shot-cot':
            return (
                "in the form \\boxed{answer}, at the end of your response.\n\nA:"
            )
        elif self.prompting_style == 'few-shot-cot':
            return "A:\n"  # TODO: 在此处添加 few-shot 示例
        elif self.prompting_style == 'zero-shot':
            return (
                "Your final answer in the form \\boxed{answer}, "
                "at the end of your response.\nA:\n"
            )
        else:
            print("WARNING: The prompting style is not given. Use zero-shot-cot as default.")
            return (
                "Let's think step by step.  "
                "in the form \\boxed{answer}, at the end of your response.\nA:\n"
            )
    

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

    def __call__(self, question, answer,i,base64_img_url,img_url):
        # # 将 thinking_outputs 拼接成一个字符串
        # thinking = ''.join(self.thinking_outputs[i]) if self.thinking_outputs else ''
        
        prompt_based = "Please provide the final answer and store it in \\boxed{answer}."
        # few_shot = ''
        
        # # 在 initial_input 中插入从 extra_json 提取的 thinking
        # initial_input = (
        #     'Given the question statement:' + question + '\n\n'
        #     + 'Use following thought to solve it:' + thinking + '\n\n'
        #     + 'Examples: ' + few_shot + '\n\n'
        #     + prompt_based
        # )
        initial_input = question + '\n\n' + prompt_based

        output = self.model.query(initial_input,base64_img_url)
        
        final_answer = self.get_answer(output)
                
        record = {}
        record['question'] = initial_input
        record['output'] = output
        record['img_url'] = img_url
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
        return record


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
    task_name = os.path.splitext(os.path.basename(args.task_config_file))[0]
    print(f"\nProcessing Task: {task_name}")

    # thinking_outputs = []
    # thinking_token_count = 0
    # if args.extra_json:
    #     if os.path.isfile(args.extra_json):
    #         thinking_outputs, thinking_token_count = extract_outputs(args.extra_json)
    #     else:
    #         print(f"[Warning] {args.extra_json} is not a valid file. Skip extracting outputs.")


    if not isinstance(task_data, list) or not all(
        ("question" in item or "question'" in item) and "answer" in item for item in task_data
    ):
        print(f"Skipping {args.task_config_file} because it does not contain 'Question' and 'Answer'.")
        return

    for item in task_data:
        if "question'" in item:
            item["question"] = item.pop("question'")

    questions = [item["question"] for item in task_data]
    correct_answers = [item["answer"] for item in task_data]
    img_urls = [item["image_url"] for item in task_data]

    print(img_urls[0])

    method = Prompt_based(
        model, 
        task=None, 
        prompting_style=args.prompting_style, 
        correct_iteration=args.correct_iteration,
        #thinking_outputs=thinking_outputs
    )

    test_num = args.test_num

    # results_path = f'/mnt/zeli/deep-thinking/results_zeroshot/{args.method}/{task_name}/'
    # results_file = f'{results_path}/{model.name}_results.json'
    results_file = f'/mnt/zeli/LRM_Benchmark/Math/selected/{task_name}/{model.name}_results_0_{test_num}.json'
    os.makedirs(os.path.dirname(results_file), exist_ok=True)

    print(f"Making a new file {results_file} to save the result.")

    final_results = []
    correct_number = 0
    total_number = len(questions)
    #test_num = 1
    empty_answer_count = 0
    test_num = args.test_num
    if test_num > len(questions):
        test_num = len(questions)
    for i in tqdm(range(test_num), desc=f"Processing {task_name} questions"):
        question = questions[i]
        answer = correct_answers[i]
        img_url = img_urls[i]
        base64_images = process_images_to_base64(img_url)
        # print(base64_images[0])
        record = method(question, answer,i,base64_images,img_url)
        final_results.append(record)
        
        if record.get('correct', False):
            correct_number += 1
        if record.get('final_answer') is None:
            empty_answer_count += 1


        answered_count = (i + 1 - empty_answer_count)
        ACC = correct_number / answered_count if answered_count > 0 else 0
        

        results_dict = {
            "ACC": ACC,
            "empty_answers": empty_answer_count,
            "results": final_results
        }

        with open(results_file, 'w') as f:
            json.dump(results_dict, f, indent=4)

    end_time = time.time()
    total_time = end_time - start_time

    print(f"Method: {args.method}")
    print(f"Task: {task_name}")
    print(f"Model: {model.name}")
    print(f"Final Accuracy: {ACC:.2f}")
    # print(f"Thinking token count: {thinking_token_count}")
    print(f"Number of questions with empty answers: {empty_answer_count}")
    print(f"Total runtime: {total_time:.2f} seconds")

    results_dict["time"] = total_time
    with open(results_file, 'w') as f:
        json.dump(results_dict, f, indent=4)

    print(f"Results saved to {results_file}")


def main():
    parser = argparse.ArgumentParser(description="Prompt-based Testing and Saving Script for a Single Task")
    parser.add_argument('--model_config', type=str, default="/mnt/zeli/LRM_Benchmark/config/model_config/api_qwen/qwen2.5-vl-3b-instruct_config.json",
                        help='Path to the model configuration file.')
    parser.add_argument('--task_config_file', type=str,default="/mnt/zeli/LRM_Benchmark/dataset/Math/selected/more.json",
                        help='Path to the single task JSON file (contains questions & images & answers).')
    parser.add_argument('--method', type=str, default='test',
                        help='Method name to use.')
    parser.add_argument('--test_num', type=int, default=87,
                        help='test number of the dataset.')                    
    parser.add_argument('--prompting_style', type=str, default='zero-shot-cot',
                        choices=['zero-shot-cot', 'few-shot-cot', 'zero-shot'],
                        help='Prompting style to use.')
    parser.add_argument('--correct_iteration', type=int, default=1,
                        help='Number of correction iterations.')

    # parser.add_argument('--extra_json', type=str, default=None,
    #                     help='Path to the additional JSON file containing outputs to be used as thinking.')
    args = parser.parse_args()

    test_and_save(args)


if __name__ == "__main__":
    main()

