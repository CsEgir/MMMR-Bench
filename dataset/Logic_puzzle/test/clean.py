import json

# 要排除的原始 ID
exclude_ids = {444, 147, 340, 255, 159, 369, 140, 327, 144,424}

# 文件路径
input_path = "/mnt/zeli/LRM_Benchmark/dataset/Logic_puzzle/test/logic.json"
output_path = "/mnt/zeli/LRM_Benchmark/dataset/Logic_puzzle/test/logic_filtered.json"

# 读取原始 JSON 文件
with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 移除指定 id 的条目
filtered_data = [item for item in data if item["id"] not in exclude_ids]

# 重新赋值 newid，从 1 开始递增
for index, item in enumerate(filtered_data):
    item["newid"] = index + 1

# 写入到新文件
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(filtered_data, f, indent=4, ensure_ascii=False)

print(f"✅ 已移除指定 id 条目，共保留 {len(filtered_data)} 条数据，newid 已从 1 递增重排。输出路径: {output_path}")
