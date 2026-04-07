
def mask_ticker(ticker: str) -> str:
    if ticker is None:
        return ""
    value = str(ticker).strip()
    if not value:
        return ""
    value = value.upper()
    
    # NEW: Handle dot-separated tickers like BRK.B
    if "." in value:
        parts = value.split(".", 1)
        prefix = parts[0]
        suffix = parts[1]
        
        # Mask the prefix using the standard logic
        if not prefix:
             return f"*.{suffix}"
        
        # Inlined simple masking for prefix to avoid recursion overhead or issues
        p_len = len(prefix)
        if p_len == 1: masked_prefix = prefix + "*"
        elif p_len == 2: masked_prefix = prefix[0] + "*"
        elif p_len == 3: masked_prefix = prefix[0] + "**"
        else: masked_prefix = prefix[0] + ("*" * (p_len - 2)) + prefix[-1]
        
        return f"{masked_prefix}.{suffix}"

    length = len(value)
    if length == 1:
        return f"{value[0]}*"
    if length == 2:
        return f"{value[0]}*"
    if length == 3:
        return f"{value[0]}**"
    return f"{value[0]}{'*' * (length - 2)}{value[-1]}"

tickers = ["POWL", "PPC", "WLDN", "CRDO", "OKTA", "APP", "CVSA", "GM", "EAT", "BRK.B"]
for t in tickers:
    print(f"'{t}' -> '{mask_ticker(t)}'")
