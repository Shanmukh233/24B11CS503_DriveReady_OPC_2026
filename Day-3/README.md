# Day 3 – LangChain Chain, Memory, Testing and Agent Introduction

## Objective
Build a LangChain bakery chatbot with conversation history, CSV response tests, and a basic agent example.

## Concepts
- `ChatGroq`
- `ChatPromptTemplate` and `MessagesPlaceholder`
- LCEL chain: prompt → LLM → `StrOutputParser`
- Chat history
- CSV-based tests
- Introductory `create_agent` without tools

## Setup
```bash
pip install langchain langchain-groq
```
Set `GROQ_API_KEY` as an environment variable. Do not commit the key.

## Files
- `task.py`: chatbot, CSV test runner, and agent demo
- `test.csv`: test questions and expected text fragments

## Run
Keep `task.py` and `test.csv` together:
```bash
python task.py
```
The test runner checks whether responses contain expected phrases. Since model output varies, results may vary.
