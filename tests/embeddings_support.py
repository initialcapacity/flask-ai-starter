from typing import List


def embedding_vector(one_index: int) -> List[float]:
    vector = [0] * 1536
    vector[one_index] = 1
    return vector


def vector_to_string(vector: List[float]) -> str:
    return "[" + ",".join([str(v) for v in vector]) + "]"


def embedding_response(one_index: int):
    return f"""
    {"{"}
      "object": "list",
      "data": [
        {"{"}
          "object": "embedding",
          "embedding": {vector_to_string(embedding_vector(one_index))},
          "index": 0
        {"}"}
      ],
      "model": "text-embedding-3-small",
      "usage": {"{"}
        "prompt_tokens": 8,
        "total_tokens": 8
      {"}"}
    {"}"}
    """
