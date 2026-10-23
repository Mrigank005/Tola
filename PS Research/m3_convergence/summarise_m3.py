"""Tables behind M3_RESULTS.md, computed from the committed snapshot. Writes m3_tables.md next to this file.

Usage: python "PS Research/m3_convergence/summarise_m3.py"
"""
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
SNAP = HERE.parent.parent / "data" / "snapshot"
read = lambda n: pd.read_parquet(SNAP / f"{n}.parquet")
s, c, p, lv = read("convergence_summary"), read("convergence_cycles"), read("convergence_profile"), read("convergence_live")
c["year"] = pd.to_datetime(c.expiry).dt.year
BK = ["60+", "40-59", "20-39", "10-19", "5-9", "0-4"]
rng = np.random.default_rng(20261013)


def ci(x):
    x = np.asarray(x, float)
    m = x[rng.integers(0, len(x), (10_000, len(x)))].mean(1)
    return np.percentile(m, 2.5), np.percentile(m, 97.5)


out = ["# M3 tables", "", f"Generated from data/snapshot (data through {read('convergence_daily').date.max()}). "
       "Eligible day: both legs traded Rs 1 Cr+, neither in its tender window. A cycle counts with 10+ eligible days. "
       "Premiums are VWAP-based, bp = 1e4 x (small / big - 1), per gram at 999.", ""]

out += ["## 1. Pooled premium over expired cycles (cycle-bootstrap 95% CI)", ""]
cols = ["pair", "cycles", "first_expiry", "last_expiry", "pooled_vwap_bp", "ci_lo_bp", "ci_hi_bp", "hit_rate", "pooled_close_bp",
        "settlement_gap_bp_median", "given_up_bp_mean", "given_up_inr_g_mean"]
out += [s[cols].round(2).to_markdown(index=False), ""]

out += ["## 2. Convergence profile: premium by trading days to expiry (expired cycles, mean of cycle means)", ""]
out += [p.pivot(index="bucket", columns="pair", values="mean_vwap_bp").reindex(BK).round(1).to_markdown(), ""]

out += ["## 3. Premium by expiry year (mean of cycle means; live cycles included and marked in section 5)", ""]
out += [c[c.counts].pivot_table(index="year", columns="pair", values="mean_vwap_bp", aggfunc="mean").round(1).to_markdown(), ""]

out += ["## 4. Control pair GOLD / GOLDM by period (expired cycles)", ""]
g = c[(c.pair == "GOLD/GOLDM") & c.counts & (c.status == "expired")]
rows = []
for name, sel in [("2020-2025", g.year <= 2025), ("2026", g.year == 2026)]:
    x = g[sel].mean_vwap_bp
    lo, hi = ci(x)
    rows.append({"period": name, "cycles": len(x), "mean_bp": x.mean(), "ci_lo_bp": lo, "ci_hi_bp": hi, "hit_rate": (x > 0).mean()})
out += [pd.DataFrame(rows).round(2).to_markdown(index=False), ""]

out += ["## 5. Live cycles: latest premium vs expired cycles at the same stage", ""]
cols = ["pair", "expiry", "date", "tdte", "bucket", "eligible", "premium_vwap_bp", "change_5d_bp", "history_cycles", "history_mean_bp", "history_pct_rank"]
out += [lv[cols].round(2).to_markdown(index=False), ""]

out += ["## 6. Per-cycle detail, same-reference pairs (expired)", ""]
cols = ["pair", "expiry", "eligible_days", "mean_vwap_bp", "vwap_60+_bp", "vwap_5-9_bp", "last_premium_vwap_bp", "settlement_gap_bp", "given_up_bp", "given_up_inr_g"]
d = c[c.pair.isin(["GOLDGUINEA/GOLDTEN", "GOLDPETAL/GOLDTEN"]) & (c.status == "expired")][cols]
out += [d.round(1).to_markdown(index=False), ""]

out += ["## 7. Monthly median premium, same-reference pairs (eligible days, calendar months since Jan 2026)", ""]
dd = read("convergence_daily")
e = dd[dd.eligible & dd.pair.isin(["GOLDGUINEA/GOLDTEN", "GOLDPETAL/GOLDTEN"]) & (pd.to_datetime(dd.date) >= "2026-01-01")]
mm = e.groupby(["pair", pd.to_datetime(e.date).dt.to_period("M").astype(str)]).premium_vwap_bp.median().unstack(0)
out += [mm.round(0).to_markdown(), ""]

(HERE / "m3_tables.md").write_text("\n".join(out), encoding="utf-8")
print("\n".join(out))
