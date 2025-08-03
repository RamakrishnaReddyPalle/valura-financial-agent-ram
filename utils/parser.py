def parse_input(input_string: str) -> dict:
    """
    Converts a string like 'PMT=2000, r=0.06, n=12' into a lowercased key dictionary.
    Also converts values to float or int if possible.
    """
    parsed = {}
    for pair in input_string.split(","):
        if "=" in pair:
            k, v = pair.split("=")
            k = k.strip().lower()
            v = v.strip()
            if "." in v:
                parsed[k] = float(v)
            elif v.isdigit():
                parsed[k] = int(v)
            else:
                parsed[k] = v
    return parsed
