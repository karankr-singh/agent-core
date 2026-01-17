# tools.py

def write_file(filename: str, content: str) -> str:
    with open(filename, "w") as f:
        f.write(content)
    return f"Saved output to {filename}"

def think(text: str) -> str:
    return f"Internal reasoning processed: {text}"
