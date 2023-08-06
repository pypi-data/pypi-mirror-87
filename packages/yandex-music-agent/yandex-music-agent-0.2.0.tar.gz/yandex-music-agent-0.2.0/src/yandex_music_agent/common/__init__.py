

def enum_print(cls) -> str:
    return ", ".join(map(lambda v: f"{v.name}: {v.value}", cls))
