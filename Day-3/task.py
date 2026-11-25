import os, csv
from pathlib import Path
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import create_agent

SYSTEM = """ROLE: Friendly assistant for Sweet Crumbs Home Bakery.
FACTS: Plum cake Rs 500. Chocolate cake Rs 650. Cupcake Rs 80 each.
Orders need 24 hours' notice. All cakes have eggless versions.
RULES: Never promise a delivery time or place. If unknown, say I'll check with the owner.
Calculate totals carefully. Keep replies under 50 words, English or Telugu matching customer."""

def build_chain(llm):
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM),
        MessagesPlaceholder("history"),
        ("human", "{question}"),
    ])
    return prompt | llm | StrOutputParser()

def run_tests(chain, path):
    rows = list(csv.DictReader(Path(path).open(encoding="utf-8")))
    passed = 0
    for row in rows:
        answer = chain.invoke({"history": [], "question": row["question"]})
        ok = row["must_include"].lower() in answer.lower()
        passed += int(ok)
        print(("PASS" if ok else "FAIL"), "|", row["question"], "->", answer)
    print(f"\n{passed}/{len(rows)} tests passed ({passed / len(rows):.0%})")

def main():
    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError("Set GROQ_API_KEY environment variable.")
    llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.3)
    chain = build_chain(llm)
    history = []
    print("LangChain Bakery Bot (type exit to quit)")
    while True:
        question = input("You: ").strip()
        if question.lower() in {"bye", "exit", "quit"}:
            break
        answer = chain.invoke({"history": history, "question": question})
        history.extend([("human", question), ("ai", answer)])
        print("Bot:", answer)

    run_tests(chain, Path(__file__).with_name("test.csv"))
    agent = create_agent(model=llm, tools=[], system_prompt=SYSTEM)
    result = agent.invoke({"messages": [{"role": "user", "content": "Do you make eggless cakes?"}]})
    print("Agent:", result["messages"][-1].content)

if __name__ == "__main__":
    main()
