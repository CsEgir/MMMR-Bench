import os
import json

def process_directory(input_dir, output_dir):
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 遍历输入目录及其子目录中的所有JSON文件
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.json'):
                # 构建输入文件路径
                input_path = os.path.join(root, file)
                
                # 构建对应的输出路径
                relative_path = os.path.relpath(root, input_dir)
                output_subdir = os.path.join(output_dir, relative_path)
                os.makedirs(output_subdir, exist_ok=True)
                output_path = os.path.join(output_subdir, file)
                
                # 处理单个文件
                process_file(input_path, output_path)

def process_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    correct_count = 0
    error_results = []
    
    for item in data.get('results', []):
        if item.get('correct', False):
            correct_count += 1
        else:
            processed_item = {
                "question": item.get('question', ''),
                "output": item.get('output', ''),
                "img_url": item.get('img_url', []),
                "final_answer": item.get('final_answer', ''),
                "correct_answer": item.get('correct_answer', '')
            }
            error_results.append(processed_item)
    
    output_data = {
        "correct_num": correct_count,
        "results": error_results
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    # 直接在这里修改输入输出路径
    input_directory = "/mnt/zeli/LRM_Benchmark/results/Spatio-Temperal/Spatial-Temporal_copy"   # 输入目录（可改）
    output_directory = "/mnt/zeli/LRM_Benchmark/results/Spatio-Temperal/my_check" # 输出目录（可改）
    
    process_directory(input_directory, output_directory)
    print(f"处理完成！结果已保存到: {output_directory}")