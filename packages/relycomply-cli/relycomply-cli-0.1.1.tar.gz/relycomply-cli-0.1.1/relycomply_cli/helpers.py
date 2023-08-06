def first_value(dct: dict):
    # TODO surely we want the *only* value?
    return next(iter(dct.values()))


def deep_get(obj, path):
    if not path:
        return obj
    elif isinstance(obj, dict):
        return deep_get(obj[path[0]], path[1:])
    elif isinstance(obj, list):
        return [deep_get(child, path) for child in obj]
    else:
        return obj
