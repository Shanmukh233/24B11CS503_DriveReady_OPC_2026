import os, json, functools
from openai import OpenAI, RateLimitError, APIConnectionError

MODEL = "openai/gpt-oss-120b"
MENU = {"plum cake": 500, "chocolate cake": 650, "cupcake": 80}
SYSTEM = f"""ROLE: Friendly assistant for Sweet Crumbs Home Bakery.
Menu/prices (Rs): {json.dumps(MENU)}
We bake to order; orders need 24 hours' notice; cakes have eggless versions.
Never promise delivery time. If information is unknown, say: I'll check with the owner.
Keep replies under 50 words, English or Telugu matching the customer.
Remember the customer's name and order during the conversation."""

def log_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"[log] {func.__name__}{args} -> {result!r}")
        return result
    return wrapper

@log_call
def get_price(item, qty=1):
    key = item.lower().strip()
    if key not in MENU:
        raise ValueError(f"Item not available: {item}")
    if qty < 1:
        raise ValueError("Quantity must be at least 1")
    return MENU[key] * qty

def main():
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise RuntimeError("Set GROQ_API_KEY environment variable.")
    client = OpenAI(api_key=key, base_url="https://api.groq.com/openai/v1")
    history = [{"role": "system", "content": SYSTEM}]
    max_turns = 8
    print("Bakery chatbot (type exit to quit)")
    while True:
        user_text = input("You: ").strip()
        if user_text.lower() in {"bye", "exit", "quit"}:
            print("Bot: Thank you for visiting Sweet Crumbs!")
            break
        history.append({"role": "user", "content": user_text})
        recent = [history[0]] + history[1:][-max_turns:]
        try:
            response = client.chat.completions.create(
                model=MODEL, messages=recent, temperature=0.3
            )
            reply = response.choices[0].message.content
        except RateLimitError:
            reply = "We're a little busy. Please try again in a minute."
        except APIConnectionError:
            reply = "I can't reach the server right now. Please try again shortly."
        history.append({"role": "assistant", "content": reply})
        print("Bot:", reply)

if __name__ == "__main__":
    print("Sample price:", get_price("cupcake", 6))
    order = {"name": "Ravi", "item": "plum cake", "qty": 2, "eggless": True}
    serialized = json.dumps(order)
    print("JSON round trip:", json.loads(serialized))
    main()
