import os
import json
import random
from collections import Counter

def load_all_questions_from_folder(folder_path):
    all_questions = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.json'):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        items = data if isinstance(data, list) else [data]
                        for q in items:
                            # 过滤不合法问题
                            if "choices" not in q or not isinstance(q["choices"], list):
                                continue
                            if len(q["choices"]) < 2:
                                continue
                            if "correct" not in q:
                                continue
                            all_questions.append(q)
                except Exception as e:
                    print(f"跳过无法解析的文件: {full_path} ({e})")

    return all_questions


def normalize_answer(ans):
    if isinstance(ans, list) and len(ans) > 0:
        return ans[0]
    elif isinstance(ans, str):
        return ans.strip()
    return None


def random_choice_baseline(questions, output_file):
    with open(output_file, 'w', encoding='utf-8') as f_out:
        for q in questions:
            n = len(q["choices"])
            labels = [chr(ord('A') + i) for i in range(n)]
            prediction = random.choice(labels)
            correct = normalize_answer(q["correct"])

            result = {
                "question": q.get("question", ""),
                "prediction": prediction,
                "correct": correct
            }
            f_out.write(json.dumps(result, ensure_ascii=False) + '\n')


def frequent_choice_baseline(questions, output_file):
    counter = Counter()
    for q in questions:
        correct = normalize_answer(q["correct"])
        if correct:
            counter[correct] += 1

    if not counter:
        print("No valid answers found for frequent choice baseline. Skip.")
        return

    most_common_choice, _ = counter.most_common(1)[0]

    with open(output_file, 'w', encoding='utf-8') as f_out:
        for q in questions:
            correct = normalize_answer(q["correct"])
            result = {
                "question": q.get("question", ""),
                "prediction": most_common_choice,
                "correct": correct
            }
            f_out.write(json.dumps(result, ensure_ascii=False) + '\n')


if __name__ == "__main__":
    folder = "./MMMR" 
    questions = load_all_questions_from_folder(folder)
    print(f"共加载有效题目数: {len(questions)}")

    random_choice_baseline(questions, "random_output.jsonl")
    frequent_choice_baseline(questions, "frequent_output.jsonl")

    print("✅ Random 和 Frequent 策略生成完毕")
