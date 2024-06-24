def truncate_string(s: str, max_length: int = 10) -> str:
    if len(s) > max_length:
        return s[:max_length - 3] + '...'
    else:
        return s