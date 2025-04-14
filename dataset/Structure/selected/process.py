import json
import shutil
import os

# 加载 JSON 数据
with open('/mnt/zeli/LRM_Benchmark/dataset/Structure/selected/structure_modified.json', 'r') as f:
    data = json.load(f)

# 定义目标目录
destination_dir = '/mnt/zeli/LRM_Benchmark/dataset/Structure/selected/images'

# 确保目标目录存在
os.makedirs(destination_dir, exist_ok=True)

# 遍历数据并复制图片
for item in data:
    if 'image_url' in item:
        for image_path in item['image_url']:
            # 获取原始图片路径
            source_path = image_path
            # 提取图片文件名
            filename = os.path.basename(source_path)
            # 构造目标路径
            destination_path = os.path.join(destination_dir, filename)

            print(f"Processing {source_path} to {destination_path}")
            
            # 复制图片到目标目录
            try:
                shutil.copy(source_path, destination_path)
                print(f"Copied {source_path} to {destination_path}")
            except FileNotFoundError:
                print(f"File not found: {source_path}")
            except Exception as e:
                print(f"Error copying {source_path}: {e}")