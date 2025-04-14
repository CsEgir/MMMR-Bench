import json

# 追加的目标 ID
append_ids = {7, 27, 270, 130, 106, 70, 272, 401, 390, 286}

# 路径配置
filtered_path = "/mnt/zeli/LRM_Benchmark/dataset/Logic_puzzle/test/logic_filtered.json"
logicvista_path = "/mnt/zeli/LRM_Benchmark/dataset/Logic_puzzle/LogicVista/LogicVista.json"
output_path = "/mnt/zeli/LRM_Benchmark/dataset/Logic_puzzle/test/logic_final.json"

# 读取已过滤的 JSON 文件
with open(filtered_path, "r", encoding="utf-8") as f:
    filtered_data = json.load(f)

# 读取 LogicVista 数据
with open(logicvista_path, "r", encoding="utf-8") as f:
    logicvista_data = json.load(f)

# 查找并追加目标 ID 的条目
appended_items = []
for item in logicvista_data:
    if item["id"] in append_ids:
        appended_items.append({
            "id": item["id"],
            "question": item["question"],
            "answer": item["answer"],
            "image_url": item["image_url"] if isinstance(item["image_url"], list) else [item["image_url"]],
            "category": "LogicVista"
        })

# 合并两个列表
merged_data = filtered_data + appended_items

# 重新设置 newid，从 1 开始递增
for index, item in enumerate(merged_data):
    item["newid"] = index + 1

# 写入最终文件
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(merged_data, f, indent=4, ensure_ascii=False)

print(f"✅ 已追加 LogicVista 中指定 ID 的 10 条数据，总数：{len(merged_data)}，newid 已重排。输出路径：{output_path}")
