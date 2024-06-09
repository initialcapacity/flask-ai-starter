from typing import List


def vector_to_string(vector: List[float]) -> str:
    return "[" + ",".join([str(v) for v in vector]) + "]"
