import csv
from ask import answer


def classify(r):
    """Turn the app's response into a category."""
    text = r["text"].lower().replace("’", "'")
    if r["blocked"]:
        return "blocked"
    if "can't find" in text or "cannot find" in text:
        return "not_found"
    return "answer"


with open("eval/questions.csv", encoding="utf-8") as f:
    tests = list(csv.DictReader(f))

results = []
for t in tests:
    r = answer(t["question"])
    actual = classify(r)
    expected = "answer" if t["expected"] == "greeting" else t["expected"]

    uris = [s["uri"] for s in r["sources"]]
    paper = t["expected_paper"]
    retrieval_hit = any(paper in u for u in uris) if paper else ""
    top1_hit = (paper in uris[0]) if (paper and uris) else ""

    passed = actual == expected and (retrieval_hit is not False)
    results.append({
        "question": t["question"],
        "expected": t["expected"],
        "actual": actual,
        "passed": passed,
        "retrieval_hit": retrieval_hit,
        "top1_hit": top1_hit,
        "answer": r["text"][:200].replace("\n", " "),
    })
    print(("✅" if passed else "❌"), t["question"], "→", actual)

with open("eval/results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

# Summary
total = len(results)
passed = sum(r["passed"] for r in results)
answer_rows = [r for r in results if r["expected"] == "answer"]
hits = sum(r["retrieval_hit"] is True for r in answer_rows)
top1 = sum(r["top1_hit"] is True for r in answer_rows)

print("\n===== SUMMARY =====")
print(f"Overall pass rate : {passed}/{total} ({passed/total:.0%})")
print(f"Retrieval hit@5   : {hits}/{len(answer_rows)}")
print(f"Retrieval hit@1   : {top1}/{len(answer_rows)}")
print("Details saved to  : eval/results.csv")