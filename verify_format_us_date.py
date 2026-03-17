import sys
from app import format_us_date

def run_tests():
    test_cases = [
        # Edge Case tests
        (None, ""),
        ("", ""),
        ("N/A", "N/A"),
        ("TBD", "TBD"),
        ("None", ""),
        
        # Original Regression
        ("2026-03-26", "03/26/26"),
        ("📅 2026-03-26", "📅 03/26/26"),
        ("⚠️ 2024-04-25 TBD", "⚠️ 04/25/24 TBD"),
        
        # New Logic Integrity Cases
        ("1/2/2025", "01/02/25"),
        ("10/15/2024", "10/15/24"),
        ("1/2/25", "01/02/25"),
        ("📅 4/1/2025", "📅 04/01/25"),
        ("⚠️ 12/2/24 TBD", "⚠️ 12/02/24 TBD"),
        ("01/05/2024", "01/05/24")
    ]
    
    failures = 0
    for i, (input_val, expected) in enumerate(test_cases, 1):
        result = format_us_date(input_val)
        if result != expected:
            print(f"[FAIL] Test {i}: Input ({input_val!r}) -> expected: ({expected!r}), but got: ({result!r})")
            failures += 1
        else:
            print(f"[PASS] Test {i}: Input ({input_val!r}) -> ({result!r})")
            
    if failures > 0:
        print(f"\nResult: FAILED. {failures} failures.")
        sys.exit(1)
    else:
        print(f"\nResult: PASSED. All {len(test_cases)} tests passed.")
        sys.exit(0)

if __name__ == "__main__":
    run_tests()
