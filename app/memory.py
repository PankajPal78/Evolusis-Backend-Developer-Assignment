from collections import deque

class ShortTermMemory:
    """
    Keeps last N (query, answer) pairs in memory.
    """
    def __init__(self, capacity: int = 5):
        self.buffer = deque(maxlen=capacity)

    def push(self, query: str, answer: str):
        self.buffer.append({"query": query, "answer": answer})

    def as_text(self) -> str:
        if not self.buffer:
            return "No recent conversation."
        lines = []
        for i, qa in enumerate(list(self.buffer)[-self.buffer.maxlen:], 1):
            lines.append(f"{i}. Q: {qa['query']} | A: {qa['answer']}")
        return "\n".join(lines)
