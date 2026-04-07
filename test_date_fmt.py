import re
from datetime import datetime

def format_us_date(date_str: str) -> str:
    if not date_str or str(date_str).strip() in ('', 'N/A', 'TBD', 'None'):
        return str(date_str) if str(date_str) != 'None' else ''
    
    date_str = str(date_str).strip()
    
    # Check for YYYY-MM-DD pattern
    match = re.search(r'(.*?)\s*(\d{4}-\d{2}-\d{2})(.*)', date_str)
    if match:
        prefix = match.group(1).strip()
        raw_date = match.group(2)
        suffix = match.group(3).strip()
        try:
            d_obj = datetime.strptime(raw_date, "%Y-%m-%d")
            formatted = d_obj.strftime("%m/%d/%y")
            parts = [p for p in (prefix, formatted, suffix) if p]
            return " ".join(parts)
        except ValueError:
            pass

    # Check for M/D/YYYY or MM/DD/YYYY pattern
    match2 = re.search(r'(.*?)\s*(\d{1,2}/\d{1,2}/\d{4})(.*)', date_str)
    if match2:
        prefix = match2.group(1).strip()
        raw_date = match2.group(2)
        suffix = match2.group(3).strip()
        try:
            d_obj = datetime.strptime(raw_date, "%m/%d/%Y")
            formatted = d_obj.strftime("%m/%d/%y")
            parts = [p for p in (prefix, formatted, suffix) if p]
            return " ".join(parts)
        except ValueError:
            pass
            
    # Check for M/D/YY or MM/DD/YY pattern to ensure zero-padding
    match3 = re.search(r'(.*?)\s*(\d{1,2}/\d{1,2}/\d{2})(.*)', date_str)
    if match3:
        prefix = match3.group(1).strip()
        raw_date = match3.group(2)
        suffix = match3.group(3).strip()
        try:
            d_obj = datetime.strptime(raw_date, "%m/%d/%y")
            formatted = d_obj.strftime("%m/%d/%y")
            parts = [p for p in (prefix, formatted, suffix) if p]
            return " ".join(parts)
        except ValueError:
            pass

    return date_str

test_cases = [
    "10/15/2024",
    "1/2/2025",
    "📅 2026-03-26",
    "2026-04-29",
    "⚠️ 2024-04-25 TBD",
    "1/2/25"
]

for t in test_cases:
    print(f"'{t}' -> '{format_us_date(t)}'")
