def get_attr_or_callable(obj, name: str):
    target = getattr(obj, name)
    if callable(target):
        return target()
    return target
