# Day 1 – LLM Assistant and Prompt Guard

## Objective
Build a simple bakery assistant using a system prompt and demonstrate Prompt Guard.

## Concepts
- Groq LLM using `ChatGroq`
- System and user messages
- Prompt roles, facts, rules, and response formatting
- Prompt Guard model demonstration

## Setup
```bash
pip install langchain-groq groq
```
Set `GROQ_API_KEY` as an environment variable. Never commit your API key.

Windows PowerShell:
```powershell
$env:GROQ_API_KEY="your_key"
```

## Run
```bash
python task.py
```
The chatbot answers bakery questions. After exiting, the script demonstrates a Prompt Guard check.
