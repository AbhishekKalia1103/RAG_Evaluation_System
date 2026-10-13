# RAG Evaluation System

A small Retrieval-Augmented Generation (RAG) agent over a PDF knowledge base, plus an evaluation pipeline that scores its answers with [DeepEval](https://github.com/confident-ai/deepeval) and compares experiments across retriever settings.

## How it works

1. **Indexing** – `RAG1/indexing.py` splits `pdfs/Penguins_ACL.pdf` into paragraphs and embeds them with OpenAI `text-embedding-3-large` into an in-memory vector store.
2. **Agent** – `RAG1/agent.py` runs a LangChain agent (`gpt-4o`) with one tool, `collecting_info`, which retrieves the top-`k` chunks (`RAG1/tools.py`).
3. **Evaluation** – each question in `eval_dataset.jsonl` is answered by the agent, then scored with four metrics:
   - **Answer Relevancy** – does the answer address the question?
   - **Faithfulness** – is the answer grounded in the retrieved context?
   - **Context Relevancy** – is the retrieved context relevant to the question?
   - **Correctness** (G-Eval) – does the answer match the expected answer?

## Experiments

Each version varies the retriever's `k` (number of chunks retrieved) and is stored under `versions/vN/`.

| Experiment | k | Answer Relevancy | Faithfulness | Context Relevancy | Correctness |
|---|---|---|---|---|---|
| v1 | 3 | 0.98 | 1.00 | 0.77 | 0.86 |
| v2 | 1 | 0.96 | 1.00 | 0.79 | 0.86 |
| v3 | 2 | 1.00 | 1.00 | 0.77 | 0.90 |

`k=2` gives the best overall results on the 20-question dataset.

## Project structure

```
RAG1/                    RAG agent (indexing, tools, prompts, agent)
pdfs/                    Source document
eval_dataset.jsonl       Questions + expected answers
versions/vN/             Per-experiment scripts and results
  eval_runner{N}.py          run the agent over the dataset -> results{N}.jsonl
  eval_all_metrics{N}_fast.py score with DeepEval -> evaluated_results{N}.jsonl
  evaluation_summary{N}.py   print averages and pass rates
save_experiments.py      save averaged metrics -> experiment_vN.jsonl
compare_experiments.py   compare all experiments in the terminal
dashboard.py             Streamlit dashboard of the experiments
single_tests/            single-metric test examples
```

## Setup

Requires Python 3.12+ and [uv](https://github.com/astral-sh/uv).

```bash
uv sync
cp .env.example .env   # then add your OPENAI_API_KEY (and optionally LangSmith keys)
```

## Running an experiment

Set `k` in `RAG1/tools.py`, then from the project root:

```bash
uv run python -m versions.v3.eval_runner3
uv run python -m versions.v3.eval_all_metrics3_fast
uv run python -m versions.v3.evaluation_summary3
uv run python save_experiments.py
```

## Comparing results

```bash
uv run python compare_experiments.py
uv run streamlit run dashboard.py
```
