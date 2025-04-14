import json
import random
import os

# 原始 JSON 文件路径
file_paths = [
    "/mnt/zeli/LRM_Benchmark/dataset/Logic_puzzle/LogicVista/LogicVista.json",
    "/mnt/zeli/LRM_Benchmark/dataset/Logic_puzzle/Marvel/Marvel.json",
    "/mnt/zeli/LRM_Benchmark/dataset/Logic_puzzle/MLRQA/MLRQA.json",
    "/mnt/zeli/LRM_Benchmark/dataset/Logic_puzzle/MME-CoT/MME-CoT_Logic.json"
]

# 目标总数
num_samples_total = 87

# 存储最终合并的数据
final_data = []

# 处理每个文件
for file_path in file_paths:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 随机抽取数据
    sampled_data = random.sample(data, min(num_samples_total, len(data)))

    # 获取文件名作为 category
    category = os.path.basename(file_path).split(".")[0]

    # 处理每条数据
    for item in sampled_data:
        final_data.append({
            "id": item["id"],
            "question": item["question"],
            "answer": item["answer"],
            "image_url": item["image_url"],
            "category": category
        })

# 随机打乱数据
random.shuffle(final_data)

# 只保留 63 条，并添加 newid 字段
final_data = final_data[:num_samples_total]
for i, item in enumerate(final_data):
    item["newid"] = i + 1  # 从 1 递增到 63

# 生成新的 JSON 文件
output_path = "logic.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(final_data, f, indent=4, ensure_ascii=False)

print(f"随机抽取的样本已保存至 {output_path}，newid 从 1 递增到 87。")
