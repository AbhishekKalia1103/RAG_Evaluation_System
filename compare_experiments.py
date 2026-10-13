import json


with open("experiment_v1.jsonl", "r", encoding="utf-8") as file:
    k3 = json.load(file)

with open("experiment_v2.jsonl", "r", encoding="utf-8") as file:
    k1 = json.load(file)

with open("experiment_v3.jsonl", "r", encoding="utf-8") as file:
    k2 = json.load(file)


print("\n============= ALL EXPERIMENTS COMPARISON =============\n")

print(
    f"{'Metric':<22} "
    f"{'k=3':<10} "
    f"{'k=2':<10} "
    f"{'k=1':<10} "
    f"{'Best':<10}"
)
print("-" * 62)

for metric in k3["metrics"]:

    scores = {
        "k=3": k3["metrics"][metric],
        "k=2": k2["metrics"][metric],
        "k=1": k1["metrics"][metric],
    }

    best = max(scores, key=scores.get)

    print(
        f"{metric.replace('_', ' ').title():<22} "
        f"{scores['k=3']:<10.2f} "
        f"{scores['k=2']:<10.2f} "
        f"{scores['k=1']:<10.2f} "
        f"{best:<10}"
    )
