import os
import json

# 源json文件路径
source_json_path = '/mnt/zeli/LRM_Benchmark/dataset/Math/Math-new/selected/math-new.json'
# 目标文件夹路径
target_folder = '/mnt/zeli/LRM_Benchmark/results/math/Math'

# 读取源json文件，获取所有question字段
with open(source_json_path, 'r', encoding='utf-8') as f:
    source_data = json.load(f)
#source_data = source_data[0]    
#print(source_data[:5])  # 打印前5个问题以供检查
source_questions = [item['question'] for item in source_data]
#print(source_questions[:5])  # 打印前5个问题以供检查

# 遍历目标文件夹及其子文件夹下所有json文件
for root, dirs, files in os.walk(target_folder):
    for file in files:
        if file.endswith('.json'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                target_data = json.load(f)
            target_data = target_data["results"]    
            # 替换question字段
            min_len = min(len(source_questions), len(target_data))
            for i in range(min_len):
                target_data[i]['question'] = source_questions[i]
            # 保存修改后的json文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(target_data, f, ensure_ascii=False, indent=2)
            print(f'已处理：{file_path}')

print('所有文件处理完成！')