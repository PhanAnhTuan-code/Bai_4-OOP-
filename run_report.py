"""Chạy toàn bộ tình huống, in bảng kết quả và ghi test_results.json."""
import json
import sys

from cases import CASES

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

rows, passed = [], 0
for case_id, desc, expected, func in CASES:
    actual = func()
    ok = actual == expected
    passed += ok
    rows.append({"id": case_id, "desc": desc, "expected": expected,
                 "actual": actual, "pass": ok})
    print(f"{case_id} | {'PASS' if ok else 'FAIL'} | {desc} | "
          f"kỳ vọng={expected} | thực tế={actual}")
print(f"\nKết quả: {passed}/{len(CASES)} tình huống đạt")
with open("test_results.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)
sys.exit(0 if passed == len(CASES) else 1)
