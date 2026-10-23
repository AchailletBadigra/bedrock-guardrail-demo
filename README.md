# 📚 AI Research Paper Assistant (Amazon Bedrock RAG + Guardrails)

A chat assistant that answers questions about 8 landmark AI papers, using only those papers as sources, with citations and safety guardrails.

## Architecture

```
User question
     │
     ▼
🛡️ Input guardrail (ApplyGuardrail) ── blocked? → custom message (no cost)
     │
     ▼
🔎 Retrieve: Bedrock Knowledge Base (managed, Titan embeddings)
     │
     ▼
🧑‍🍳 Generate: Amazon Nova Lite via Converse API (grounded prompt + citations)
     │
     ▼
🛡️ Output guardrail (Converse guardrailConfig)
     │
     ▼
💬 Streamlit chat UI (answer + sources)
```

## Papers in the knowledge base

Transformer · BERT · GPT-3 · RAG · LoRA · Chain-of-Thought · InstructGPT · ReAct

## Features

- **Grounded answers:** the model answers only from retrieved chunks and cites them like [1].
- **Out-of-scope handling:** "I can't find this in the papers I have."
- **Guardrails:** denied topics (financial and medical advice), content filters and prompt-attack detection.
- **Input guard before retrieval:** blocked questions never reach the Knowledge Base or the model.
- **Automated evaluation:** a golden set of 15 questions with pass rate and retrieval hit@k.

## Evaluation results

| Metric            | Score       |
| ----------------- | ----------- |
| Overall pass rate | 14/15 (93%) |
| Retrieval hit@5   | 8/8 (100%)  |
| Retrieval hit@1   | 8/8 (100%)  |

**Known limitation:** "What are the three steps of RLHF in InstructGPT?" fails. The right paper is retrieved, but not the method section, so it's a generation/precision miss rather than a retrieval miss. Next step: reranking.

## Debugging highlights

- **The managed Knowledge Base doesn't support RetrieveAndGenerate**, so I built the generation layer myself (Retrieve + Converse).
- **The denied topic wasn't firing.** ApplyGuardrail showed the code was fine; get-guardrail showed the topic policy had never been saved. I fixed it and added sample phrases.
- **Version 1 of the guardrail was frozen before the policies existed.** I created version 2 and verified it before deploying.
- **Data contamination:** unrelated PDFs in the bucket were being retrieved. I removed them and re-synced.

## Project structure

```
data/papers/   source PDFs (synced to S3)
src/ask.py     RAG pipeline (input guard → retrieve → generate)
src/app.py     Streamlit UI
src/evaluate.py evaluation script
eval/          golden test set + results
docs/          notes and diagrams
```

## How to run

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install boto3 streamlit
python -m streamlit run src/app.py
```

Requires AWS credentials with access to Amazon Bedrock in us-east-1.

## Tech stack

Amazon Bedrock (Knowledge Bases, Guardrails, Nova Lite, Titan Embeddings) · S3 · Python · boto3 · Streamlit
