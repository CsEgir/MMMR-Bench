import json
import random
import requests
import os
import shutil

# 手动填写你的 JSON 文件路径
json_files = [
    '/LRM_Benchmark/dataset/Coding/MMRU-Coding/MMRU-Coding.json',
    '/LRM_Benchmark/dataset/Coding/web_to_code/question/question.json',
    '/LRM_Benchmark/dataset/Logic_puzzle/MMRU-Logic/2D.json',
    '/LRM_Benchmark/dataset/Logic_puzzle/MMRU-Logic/3D.json',
    '/LRM_Benchmark/dataset/MAP/MMRU-Map/MMRU-Map.json',
    '/LRM_Benchmark/dataset/Math/Math-new/selected/Math.json',
    '/LRM_Benchmark/dataset/Space-Time/MMRU-Space-Time/Spatial-Temporal_copy.json',
    '/LRM_Benchmark/dataset/Science/science.json'
]

all_data = []

# 读取并合并所有 JSON 文件的数据
for file_path in json_files:
    parts = file_path.split('/')
    if len(parts) > 6:
        category = parts[5]
    else:
        category = "Unknown"
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            item['Category'] = category
        all_data.extend(data)

# 随机抽取 1/10 的数据
sample_size = max(1, len(all_data) // 10)
sampled_data = random.sample(all_data, sample_size)



# 保存为新的 JSON 文件
with open('/LRM_Benchmark/method/sampled_Data/sampled_output.json', 'w', encoding='utf-8') as f:
    json.dump(sampled_data, f, ensure_ascii=False, indent=2)

print(f"已从 {len(all_data)} 条数据中随机抽取 {sample_size} 条，结果已保存到 sampled_output.json")

# 创建图片保存文件夹
output_folder = "/LRM_Benchmark/method/sampled_Data/images"
os.makedirs(output_folder, exist_ok=True)

# 下载图片
img_count = 0
# 下载图片并修改 image_url 字段为本地路径
for idx, item in enumerate(sampled_data):
    image_urls = item.get('image_url', [])
    new_paths = []
    for url_idx, src_path in enumerate(image_urls):
        if not os.path.isfile(src_path):
            print(f"图片不存在: {src_path}")
            continue
        ext = os.path.splitext(src_path)[-1]
        new_filename = f"{idx}_{url_idx}{ext}"
        dst_path = os.path.join(output_folder, new_filename)
        shutil.copy(src_path, dst_path)
        new_paths.append(dst_path)
    # 替换 image_url 字段为新路径
    item['image_url'] = new_paths

# # 保存修改后的 JSON 文件
# with open("/mnt/zeli/LRM_Benchmark/method/sampled_Data/images", 'w', encoding='utf-8') as f:
#     json.dump(sampled_data, f, ensure_ascii=False, indent=2)
sampled_json_with_local_img = '/LRM_Benchmark/method/sampled_Data/sampled_output2.json'
with open(sampled_json_with_local_img, 'w', encoding='utf-8') as f:
    json.dump(sampled_data, f, ensure_ascii=False, indent=2)


print(f"图片下载完成，image_url 字段已替换为本地路径，结果已保存到 /mnt/zeli/LRM_Benchmark/method/sampled_Data/images")


# 1. 获取未被抽样的数据
sampled_set = set(map(id, sampled_data))
unsampled_data = [item for item in all_data if id(item) not in sampled_set]

# 1. 读取额外的 JSON 文件
extra_json_path = '/LRM_Benchmark/dataset/MAP/Map_data/question.json'  # 替换为你的实际路径
with open(extra_json_path, 'r', encoding='utf-8') as f:
    extra_data = json.load(f)

# 2. 合并到 unsampled_data
unsampled_data.extend(extra_data)
print(f"已将 {len(extra_data)} 条数据合并到 unsampled_data，总数为 {len(unsampled_data)}")

# 2. 保存未抽样数据为新的 JSON 文件
unsampled_json_path = '/LRM_Benchmark/method/unsampled_Data/unsampled_output.json'
with open(unsampled_json_path, 'w', encoding='utf-8') as f:
    json.dump(unsampled_data, f, ensure_ascii=False, indent=2)
print(f"未被抽样的 {len(unsampled_data)} 条数据已保存到 {unsampled_json_path}")

# 3. 创建未抽样图片保存文件夹
unsampled_img_folder = "/LRM_Benchmark/method/unsampled_Data/images"
os.makedirs(unsampled_img_folder, exist_ok=True)

# 4. 下载未抽样图片并修改 image_url 字段为本地路径
for idx, item in enumerate(unsampled_data):
    image_urls = item.get('image_url', [])
    new_paths = []
    for url_idx, src_path in enumerate(image_urls):
        if not os.path.isfile(src_path):
            print(f"图片不存在: {src_path}")
            continue
        ext = os.path.splitext(src_path)[-1]
        new_filename = f"{idx}_{url_idx}{ext}"
        dst_path = os.path.join(unsampled_img_folder, new_filename)
        shutil.copy(src_path, dst_path)
        new_paths.append(dst_path)
    item['image_url'] = new_paths

# 5. 保存修改后的未抽样 JSON 文件
unsampled_json_with_local_img = '/LRM_Benchmark/method/unsampled_Data/unsampled_output2.json'
with open(unsampled_json_with_local_img, 'w', encoding='utf-8') as f:
    json.dump(unsampled_data, f, ensure_ascii=False, indent=2)
print(f"未抽样图片下载完成，image_url 字段已替换为本地路径，结果已保存到 {unsampled_json_with_local_img}")