import shutil
import os

source_dir = '/路径/源文件夹'
target_dir = '/路径/目标文件夹'

# 自动创建目标文件夹
os.makedirs(target_dir, exist_ok=True)

for filename in os.listdir(source_dir):
    src_file = os.path.join(source_dir, filename)
    if os.path.isfile(src_file):  # 仅处理文件（不包含子文件夹）
        shutil.move(src_file, target_dir)