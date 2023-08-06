from typing import Iterable, Optional


def optional_array_query_param(inputs: Optional[Iterable[str]]) -> Optional[str]:
    if inputs:
        return array_query_param(inputs)
    return None


def array_query_param(inputs: Iterable[str]) -> str:
    return ",".join(inputs)
