# MMMR 🔍🧠
**Benchmarking Massive Multi-Modal Reasoning Tasks**

Official repository for **“Benchmarking Massive Multi-Modal Reasoning Tasks”**

[**🌐 Homepage**](https://mmmr-benchmark.github.io/) | [**🏆 Leaderboard**](https://mmmr-benchmark.github.io/#leaderboard) | [**🤗 MMMR**](https://huggingface.co/datasets/csegirl/MMMR) | [**💡 Examples**](https://mmmr-benchmark.github.io/#Examples)

---

## 📢 News

- **2025.05.21** 🎉 We are very proud to launch MMMR, a new benchmark designed to rigorously evaluate multi-modal reasoning with explicit thinking.

---

## 📘 About MMMR-Bench

Recent advances in Multi-Modal Large Language Models (MLLMs) have enabled unified processing of language, vision, and structured inputs, opening the door to complex tasks such as logical deduction, spatial reasoning, and scientific analysis. Despite their promise, the reasoning capabilities of MLLMs—particularly those augmented with intermediate thinking traces (MLLMs-T)—remain poorly understood and lack standardized evaluation benchmarks. Existing work focuses primarily on perception or final answer correctness, offering limited insight into how models reason or fail across modalities. 

To address this gap, we introduce the **MMMR**, a new benchmark designed to rigorously evaluate multi-modal reasoning with explicit thinking.

<p align="center"><strong>🧠 MMMR Overview</strong></p>
<p align="center">
    <img src="readme_imgs/overview.png" width="80%"> <br>
</p>

## The composition of MMMR
1) a high-difficulty dataset of **1,083** questions spanning **six** diverse reasoning types with symbolic depth and multi-hop demands。

<p align="center"><strong>📊 Dataset Composition</strong></p>
<p align="center">
    <img src="readme_imgs/data.png" width="80%"> <br>
</p>

2) a modular **Reasoning Trace Evaluation Pipeline (RTEP)** for assessing reasoning quality beyond accuracy through metrics like relevance, consistency, and structured error annotation.

<p align="center"><strong>🛠️ Reasoning Trace Evaluation Pipeline </strong></p>
<p align="center">
    <img src="readme_imgs/pipeline.png" width="80%"> <br>
</p>

## The Evaluation of MMMR

This benchmark reveals persistent gaps between accuracy and reasoning quality and provides an actionable evaluation pipeline for future model development.

our evaluation pipeline comprises three core stages: **(I) Reasoning Dataset Construction**, **(II) Thinking Quality Assessment**, and **(III) Reasoning Insights Synthesis**.

<p align="center"><strong>📈 Evaluation Metrics & Scoring</strong></p>
<p align="center">
    <img src="readme_imgs/eval.png" width="80%"> <br>
</p>

---

## Evaluation

To calculate the precision, please follow the following steps:
1. Install the required packages.

```bash
pip install -r requirements.txt
```

2. Fill the model config file

'''bash
cd config
'''

create your model config file as the form of sample.json.

3. Run the evaluation scripts

Run the evaluation with the based prompt

'''bash
cd code
python Based_prompt.py --model_config <your model path> --task_config_file <the dataset json file path> --test_num <test number> --results_file <your results path>
'''

Run the evaluation with the reasoing prompt (with models who have reasoing content)

'''bash
cd code
python Reasoning_prompt.py --model_config <your model path> --task_config_file <the dataset json file path> --test_num <test number> -results_file <your results path>
'''

Finally, you can fing your results in the results path.

## 🏆 Leaderboard

### Contributing to the Leaderboard

🚨 The [Leaderboard][https://mmmr-benchmark.github.io/#Leaderboard] is continuously being updated, welcoming the contribution of your excellent LMMs!


### Data Usage

We release the MMMR data and evaluation prompts for benchmarking on the leaderboard.

You can download the dataset from the [🤗 Huggingface](https://huggingface.co/datasets/csegirl/MMMR) by the following command (make sure that you have installed [related packages](https://huggingface.co/docs/datasets/quickstart)):

```python
from datasets import load_dataset

# Login using e.g. `huggingface-cli login` to access this dataset
ds = load_dataset("csegirl/MMMR")
```

## :white_check_mark: Citation

If you find **MMMR** useful for your research and applications, please kindly cite using this BibTeX:

```latex
@inproceedings{tie2025mmmr,
        title={MMMR: Benchmarking Massive Multi-Modal Reasoning Tasks},
        author={Guiyao Tie and Xueyang Zhou and Tianhe Gu and Ruihang Zhang and Chaoran Hu and Sizhe Zhang and Mengqu Sun and Yan Zhang and Pan Zhou and Lichao Sun},
        booktitle={Proceedings of the NeurIPS 2025 Datasets and Benchmarks Track},
        year={2025},
      }
```