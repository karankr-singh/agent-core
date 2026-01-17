# llm.py

def antigravity_llm(prompt: str) -> str:
    """
    Replace the body of this function with
    Antigravity's actual LLM call.

    This wrapper is intentional.
    """

    # ---- PSEUDOCODE ----
    # response = antigravity.generate(
    #     model="gemini",
    #     prompt=prompt,
    #     temperature=0.3,
    #     max_tokens=300# llm.py

def antigravity_llm(prompt: str) -> str:
    # replace with real Antigravity call
    return "CONTINUE"


def antigravity_embed(text: str) -> list:
    """
    Return a list[float] embedding.
    Replace with Antigravity embedding API.
    """

    # ---- PSEUDOCODE ----
    # emb = antigravity.embed(
    #     model="embedding-model",
    #     input=text
    # )
    # return emb.vector

    # TEMP fake embedding (DO NOT keep long-term)
    return [float(ord(c) % 50) for c in text[:64]]

    # )
    # return response.text

    # TEMP fallback (until wired)
    return "CONTINUE"
