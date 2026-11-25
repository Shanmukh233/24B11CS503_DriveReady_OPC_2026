# Day 2 – API Chatbot, Memory, Python and JSON

## Objective
Create a bakery chatbot using the OpenAI-compatible Groq API, preserve conversation history, and practice Python data handling.

## Concepts
- OpenAI SDK with Groq endpoint
- System prompts and conversation history
- Menu dictionary and price-calculation function
- JSON serialization/deserialization
- Logging decorator
- Handling API rate-limit and connection errors

## Setup
```bash
pip install openai
```
Set `GROQ_API_KEY` in your environment. Do not commit your key.

## Run
```bash
python task.py
```
The program demonstrates a six-cupcake calculation and JSON order round-trip before starting the chatbot.
