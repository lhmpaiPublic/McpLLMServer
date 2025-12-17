from llm.ollama_client import generate

async def chat_with_llm(prompt: str) -> dict:
    answer = await generate(prompt)
    return {
        "prompt": prompt,
        "answer": answer
    }
