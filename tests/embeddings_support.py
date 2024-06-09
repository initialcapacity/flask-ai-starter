from typing import List


def embedding_vector(one_index: int) -> List[float]:
    vector = [0] * 1536
    vector[one_index] = 1
    return vector


def vector_to_string(vector: List[float]) -> str:
    return ",".join([str(v) for v in vector])
