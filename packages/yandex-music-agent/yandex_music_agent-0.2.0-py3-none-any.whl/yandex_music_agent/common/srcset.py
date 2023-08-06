import re
from collections import namedtuple
from typing import List


class SrcSetValue(namedtuple("SrcSetValue", ["src", "size"])):
    pass


class SrcSet:

    def __init__(self, values: List[SrcSetValue]):
        self.values = values

    @property
    def best(self) -> SrcSetValue:
        result = self.values[0]
        for value in self.values[1:]:
            if value.size > result.size:
                result = value
        return result

    @classmethod
    def parse(cls, raw: str) -> "SrcSet":
        values = []
        item_re = re.compile("^(.*?)( (\\d+)x)?$")
        for item in raw.split(", "):
            m = item_re.match(item)
            values.append(SrcSetValue(f"https:{m.group(1)}", int(m.group(3) or 1)))
        return cls(values)
