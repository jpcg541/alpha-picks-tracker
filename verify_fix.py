
import re

def mask_ticker(ticker: str) -> str:
    if ticker is None:
        return ""
    value = str(ticker).strip().upper()
    if not value:
        return ""
    
    if "." in value:
        parts = value.split(".")
        masked_parts = [mask_ticker(p) if p else "*" for p in parts]
        return ".".join(masked_parts)

    length = len(value)
    if length <= 2:
        return value[0] + "*"
    if length == 3:
        return value[0] + "**"
    return f"{value[0]}{'*' * (length - 2)}{value[-1]}"

# Test cases
all_tickers = {"WLDN", "BRK.B", "B", "APP", "POWL", "PPC"}
summary_text = """
[AP-Clock]:
• $POWL 175/180
• $PPC 154/180

[ BREAKDOWNS ]
• $WLDN | NEWS+DVG
• $BRK.B | NEWS+INFLECT
"""

# Current (Correct) Logic
sorted_tickers = sorted(all_tickers, key=len, reverse=True)
pattern = "|".join(re.escape(t) for t in sorted_tickers)
fixed_text = re.sub(
    rf"\b({pattern})\b", 
    lambda m: mask_ticker(m.group(0)), 
    summary_text, 
    flags=re.IGNORECASE
)

print("--- Original ---")
print(summary_text)
print("\n--- Masked ---")
print(fixed_text)

# Check specifically for the ghost star issue
if "***" in fixed_text and "BRK" not in fixed_text: # Allow for longer tickers but check B
    print("\nWARNING: Possible ghost stars detected!")
else:
    print("\nSUCCESS: No redundant masking detected.")

print(f"\nWLDN -> {mask_ticker('WLDN')}")
print(f"BRK.B -> {mask_ticker('BRK.B')}")
