from typing import List

from starter.search.vector_support import vector_to_string


def embedding_vector(one_index: int) -> List[float]:
    """

    :rtype: object
    """
    vector = [0] * 1536
    vector[one_index] = 1
    return vector


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
