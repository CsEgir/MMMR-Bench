import json
import os
import argparse

def extract_elements(input_dir, output_dir):
    """
    从目录中的所有json文件中提取指定索引的元素
    
    Args:
        input_dir (str): 输入目录路径
        output_dir (str): 输出目录路径
        element_index (int): 要提取的元素的索引
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    #index = 0
    
    # 获取目录下所有json文件
    json_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]
    
    for json_file in json_files:
        input_path = os.path.join(input_dir, json_file)
        
        try:
            # 读取json文件
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            #name = os.path.splitext(input_path)[0]    
            name = os.path.splitext(os.path.basename(input_path))[0]
            index = int(name)
            print(index)

            data = data["results"][index]    

            # 创建输出文件名
            output_filename = f"{index}.json"
            output_path = os.path.join(output_dir, output_filename)

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            # # 检查数据是否为列表且索引有效
            # if isinstance(data, list) and 0 <= element_index < len(data):
            #     # 提取指定索引的元素
            #     element = data[element_index]
                
            #     # 创建输出文件名
            #     output_filename = f"{os.path.splitext(json_file)[0]}_element_{element_index}.json"
            #     output_path = os.path.join(output_dir, output_filename)
                
            #     # 保存提取的元素
            #     with open(output_path, 'w', encoding='utf-8') as f:
            #         json.dump(element, f, indent=4, ensure_ascii=False)
                
            #     print(f"已处理文件: {json_file} -> {output_filename}")
            # else:
            #     print(f"警告: {json_file} 不包含有效的第 {element_index} 个元素")
                
        except Exception as e:
            print(f"处理文件 {json_file} 时出错: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='从json文件中提取指定索引的元素')
    # parser.add_argument('--input_dir', type=str, required=True, help='输入目录路径')
    # parser.add_argument('--output_dir', type=str, required=True, help='输出目录路径')
    # parser.add_argument('--index', type=int, required=True, help='要提取的元素的索引')
    
    args = parser.parse_args()
    input_path = "/mnt/zeli/LRM_Benchmark/method/MME-CoT/cache/Logic_puzzle/relevance_rate/Qwen/Qwen2.5-VL-32B-Instruct"
    extract_elements(input_path,input_path)

if __name__ == '__main__':
    main()