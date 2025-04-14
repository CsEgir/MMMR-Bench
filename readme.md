# Connecting to a Server via VPN and VSCode Remote-SSH

This guide will walk you through the process of connecting to a remote server using a VPN and Visual Studio Code with the Remote-SSH extension.

## Prerequisites

Before you begin, ensure you have the following:

- Visual Studio Code installed on your local machine
- The Remote-SSH extension for Visual Studio Code

## Connect to the Server Using VSCode Remote-SSH

After you are connected to the VPN, proceed with the following steps to connect to the server using VSCode:

1. Open Visual Studio Code.
2. Press `Ctrl+Shift+P` to open the Command Palette.
3. Type `Remote-SSH: Add New SSH Host` and select it.
4. You will be prompted to enter the SSH connection command. Use the following format:

```bash
ssh 1004hzeli@222.20.126.192
```
5. After entering the command, the system may prompt you to enter the password for the SSH connection. Use the following password:
**SSH Password:** 123456789

6. Once authenticated, VSCode will connect to the remote server, and you will be able to work on your projects as if you were working locally.
# test.py README

## Overview
`test.py` is a Python script located in the `/mnt/zeli/LRM_Benchmark/method` directory. This script is designed for the LRM-Benchmark project and performs a set of specific operations. Please follow the instructions below to ensure the script runs correctly.

## Prerequisites
Before running `test.py`, make sure to meet the following prerequisites:

- You have activate a Conda environment named `critic`.

## Running the Script
To execute `test.py`, carefully follow these steps:

1. **Accessing the Directory**:
Before you begin, ensure you are in the correct directory:

```bash
bash
cd /mnt/zeli/LRM_Benchmark/method
```
2. **Activate the Conda Environment**:
   It is crucial to activate the Conda environment `critic` before running the script. This ensures that all necessary dependencies and environment variables are set correctly. Use the following command in your terminal:

```bash
conda activate /mnt/zeli/miniconda3/envs/critic
```

3. **Run the Script**:
After activating the Conda environment, navigate to the directory containing `test.py` and run the script using Python.
Also, you need to set model_config and task_config_file to determine the model and the dataset we use.
like:

```bash
proxy_off ( make the network connected)
python Based_prompt.py --model_config /mnt/zeli/LRM_Benchmark/config/model_config/api_qwen2.5_vl_32b_instruct_config.json --task_config_file /mnt/zeli/LRM_Benchmark/dataset/Space-Time/MME-CoT/Spatial-Temporal.json --test_num 2
```
The script will use model qwen2.5_vl_32b_instruct and MME-CoT Spatial-Temporal dataset to excute.
Then, the script starts executing, and you may see various output messages in the terminal.

## How to introduce a dataset in right forms
Firstly, you should put the dataset in right categories, such as the dataset MathVerse in category Math. Also remember a dataset has different parts and they may belong to different categories, such as MME-CoT Logic dataset in category Logic_puzzle and Math in category Math.

Secondly, you should download the dataset from huggingface or github, and process the data in right forms. For example,in dataset Marvel, you should create the dir path:/mnt/zeli/LRM_Benchmark/dataset/Logic_puzzle/Marvel, and then create a json file and images dir in it. The json file should contain information about id, question, answer, image_url and other necessary information. The image_url should contain the path to the image, and the images should be put in the images dir.

The pictures below are the forms example of one datset.(If you can not open the picture, just follow the url and find the picture)
image.png![1742958839465](/mnt/zeli/LRM_Benchmark/readme_img/1742958839465.png)
![1742958859742](/mnt/zeli/LRM_Benchmark/readme_img/1742958859742.png)

Finally, you can test if the dataset is set in right forms by running the script, setting the task_config_file as your dataset config file. The results file is in /mnt/zeli/LRM_Benchmark/results.
Also, you can set the test_num in test.py if want to test more examples in the dataset.

![1742959114782](/mnt/zeli/LRM_Benchmark/readme_img/1742959114782.png)

## MME-Cot Method
The script is in path:/mnt/zeli/LRM_Benchmark/method/MME-CoT/generate.py.
You should set the prompt path(/mnt/zeli/LRM_Benchmark/method/MME-CoT/prompt/prompt_precision.txt,/mnt/zeli/LRM_Benchmark/method/MME-CoT/prompt/prompt_reflection_quality.txt,/mnt/zeli/LRM_Benchmark/method/MME-CoT/prompt/prompt_relevance_rate.txt,these three prompt files are available) and the task_config_file, method, test_num, dataset.

The task_config_file should be your results file.
The method should be your prompt type(precison,reflection_quality,relevance_rate).
The dataset should be your type of dataset(Math,Logical,etc)