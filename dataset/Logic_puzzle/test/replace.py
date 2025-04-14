import json

# 文件路径
logic_final_path = '/mnt/zeli/LRM_Benchmark/dataset/Logic_puzzle/test/logic_final.json'
logicvista_path = '/mnt/zeli/LRM_Benchmark/dataset/Logic_puzzle/LogicVista/LogicVista.json'

# 加载 JSON 数据
with open(logic_final_path, 'r') as f:
    logic_final = json.load(f)

with open(logicvista_path, 'r') as f:
    logicvista = json.load(f)

# 替换映射关系：final_id -> vista_id
id_mapping = {
    294: 32,
    306: 17,
    308: 104,
    3: 19
}

# 构建索引便于查找
final_index_map = {item['id']: idx for idx, item in enumerate(logic_final)}
vista_lookup = {item['id']: item for item in logicvista}

# 执行替换
for old_id, new_id in id_mapping.items():
    if old_id not in final_index_map or new_id not in vista_lookup:
        print(f"❌ Skipped: old_id {old_id} or new_id {new_id} not found")
        continue

    idx = final_index_map[old_id]
    original = logic_final[idx]
    replacement = vista_lookup[new_id]

    # 构造替换项，保留原来的 newid 和 category，但 id 更新为新 id
    logic_final[idx] = {
    'id': new_id,
    'question': replacement['question'],
    'answer': replacement['answer'],
    'image_url': replacement['image_url'],
    'category': original.get('category'),
    'newid': original.get('newid'),
    }


print("✅ Replacement and ID update complete.")

# 输出路径
output_path = '/mnt/zeli/LRM_Benchmark/dataset/Logic_puzzle/test/logic_final_updated.json'
with open(output_path, 'w') as f:
    json.dump(logic_final, f, indent=4)

print(f"📄 Updated JSON saved to: {output_path}")
