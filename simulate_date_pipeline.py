"""
End-to-end simulation of what the Streamlit table should render.
This imports format_us_date directly from app.py and runs it against
the real snapshot.json data.
"""
import sys, re, json
from datetime import datetime
import zoneinfo

# ---- inline format_us_date (same as in app.py) ----
def format_us_date(date_str):
    if not date_str or str(date_str).strip() in ('', 'N/A', 'TBD', 'None'):
        return str(date_str) if str(date_str) != 'None' else ''
    date_str = str(date_str).strip()
    match = re.search(r'(.*?)\s*(\d{4}-\d{2}-\d{2})(.*)', date_str)
    if match:
        prefix, raw_date, suffix = match.group(1).strip(), match.group(2), match.group(3).strip()
        try:
            formatted = datetime.strptime(raw_date, "%Y-%m-%d").strftime("%m/%d/%y")
            return " ".join(p for p in (prefix, formatted, suffix) if p)
        except ValueError:
            pass
    match2 = re.search(r'(.*?)\s*(\d{1,2}/\d{1,2}/\d{4})(.*)', date_str)
    if match2:
        prefix, raw_date, suffix = match2.group(1).strip(), match2.group(2), match2.group(3).strip()
        try:
            formatted = datetime.strptime(raw_date, "%m/%d/%Y").strftime("%m/%d/%y")
            return " ".join(p for p in (prefix, formatted, suffix) if p)
        except ValueError:
            pass
    match3 = re.search(r'(.*?)\s*(\d{1,2}/\d{1,2}/\d{2})(.*)', date_str)
    if match3:
        prefix, raw_date, suffix = match3.group(1).strip(), match3.group(2), match3.group(3).strip()
        try:
            formatted = datetime.strptime(raw_date, "%m/%d/%y").strftime("%m/%d/%y")
            return " ".join(p for p in (prefix, formatted, suffix) if p)
        except ValueError:
            pass
    return date_str

# ---- Load snapshot.json ----
with open(r'd:\Stock Analysis\AP_Public_View\data\snapshot.json', encoding='utf-8') as f:
    data = json.load(f)

rows = data.get('table_view_model', [])
print(f"{'Ticker':<8} | {'RAW picked_date':<15} | {'CONVERTED picked':<16} | {'RAW earnings_fmt':<22} | {'CONVERTED earnings'}")
print("-" * 100)
for r in rows[:10]:
    raw_picked = r.get('picked_date', '')
    raw_earn   = r.get('earnings_fmt', '')
    conv_picked = format_us_date(raw_picked)
    conv_earn   = format_us_date(raw_earn)
    print(f"{r.get('ticker',''):<8} | {str(raw_picked):<15} | {conv_picked:<16} | {str(raw_earn):<22} | {conv_earn}")
