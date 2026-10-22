"""Validation results. Errors block the snapshot; warnings are written to the report and the manifest."""
from collections import defaultdict


class Report:
    def __init__(self):
        self.items = defaultdict(lambda: {"level": None, "count": 0, "examples": [], "note": ""})
        self.passed = {}

    def add(self, check, level, example=None, note="", n=1):
        it = self.items[check]
        it["level"] = "error" if "error" in (it["level"], level) else level
        it["count"] += n
        it["note"] = note or it["note"]
        if example is not None and len(it["examples"]) < 5:
            it["examples"].append(str(example))

    def ok(self, check, note):
        """Record a check that ran clean, so the report shows what was verified, not only what failed."""
        if check not in self.items:
            self.passed[check] = note

    def errors(self):
        return {k: v for k, v in self.items.items() if v["level"] == "error"}

    def summary(self):
        return {
            "errors": {k: v["count"] for k, v in self.items.items() if v["level"] == "error"},
            "warnings": {k: v["count"] for k, v in self.items.items() if v["level"] == "warn"},
            "info": {k: v["count"] for k, v in self.items.items() if v["level"] == "info"},
            "passed": sorted(self.passed),
        }

    def markdown(self):
        lines = ["| Check | Result | Count | Note | Examples |", "|---|---|---|---|---|"]
        order = {"error": 0, "warn": 1, "info": 2}
        for k, v in sorted(self.items.items(), key=lambda kv: (order[kv[1]["level"]], kv[0])):
            ex = "<br>".join(e.replace("|", "\\|") for e in v["examples"])
            lines.append(f"| `{k}` | **{v['level'].upper()}** | {v['count']} | {v['note']} | {ex} |")
        for k, note in sorted(self.passed.items()):
            lines.append(f"| `{k}` | pass | 0 | {note} | |")
        return "\n".join(lines)
