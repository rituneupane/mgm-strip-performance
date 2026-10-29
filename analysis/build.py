"""MGM Resorts: Strip Performance Through Q3 2026 (portfolio case study).
Run:  python analysis/build.py
1. Loads the source-recorded CSVs in data/ (every row carries a source_id -> SOURCES.md).
2. Runs tie-out checks (segment sums, quarter sums, revenue mix, reported margins, RevPAR math) -> data/checks.csv
3. Computes derived metrics -> data/derived_metrics.csv
4. Writes docs/data.js (dashboard)
Requires: pandas.
"""
import json, pathlib, csv
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
D = ROOT / "data"
seg = pd.read_csv(D / "segments_annual.csv")
mix = pd.read_csv(D / "strip_revenue_mix.csv")
cost = pd.read_csv(D / "strip_costs.csv")
kpi = pd.read_csv(D / "strip_hotel_kpis.csv")
qtr = pd.read_csv(D / "strip_quarterly.csv")
gam = pd.read_csv(D / "strip_gaming.csv")
dig = pd.read_csv(D / "digital.csv")
vp = pd.read_csv(D / "visitor_profile.csv")
rooms = pd.read_csv(D / "mgm_strip_rooms.csv")
lva = pd.read_csv(D / "lvcva_annual.csv")
lvm = pd.read_csv(D / "lvcva_monthly.csv")
ytd = pd.read_csv(D / "lvcva_ytd2026.csv").set_index("metric")

checks = []
def check(name, actual, expected, tol, source):
    ok = abs(actual - expected) <= tol
    checks.append({"check": name, "actual": round(actual, 3), "expected": round(expected, 3), "tolerance": tol,
                   "result": "PASS" if ok else "FAIL", "source_ids": source})

def s(company, segment, year, col="net_revenue_musd"):
    r = seg[(seg.company == company) & (seg.segment == segment) & (seg.year == year)]
    return float(r[col].iloc[0])

MGM_STRIP, CZR_LV = "Las Vegas Strip Resorts", "Las Vegas"
# ---------- 1. Tie-outs ----------
for y in (2023, 2024, 2025):
    parts = seg[(seg.company == "MGM") & (seg.segment != "Consolidated") & (seg.year == y)].net_revenue_musd.sum()
    check(f"MGM {y}: segment net revenues sum to consolidated", parts, s("MGM", "Consolidated", y), 0.01, "S2")
    parts = seg[(seg.company == "Caesars") & (seg.segment != "Consolidated") & (seg.year == y)]
    check(f"Caesars {y}: segment net revenues sum to consolidated", parts.net_revenue_musd.sum(), s("Caesars", "Consolidated", y), 1.0, "S4")
    check(f"Caesars {y}: segment Adjusted EBITDA sums to consolidated", parts.segment_profit_musd.sum(), s("Caesars", "Consolidated", y, "segment_profit_musd"), 1.0, "S4")
    for co, sg, tol in (("MGM", MGM_STRIP, 0.01), ("Caesars", CZR_LV, 1.0)):
        m = mix[(mix.company == co) & (mix.year == y)].net_revenue_musd.sum()
        check(f"{co} {y}: Strip revenue mix sums to segment revenue", m, s(co, sg, y), tol, "S2/S4")
    if y >= 2024:
        for co, sg, tol in (("MGM", MGM_STRIP, 0.01), ("Caesars", CZR_LV, 0.5)):
            q = qtr[(qtr.company == co) & (qtr.quarter.str.startswith(str(y)))]
            check(f"{co} {y}: four quarters of Strip revenue sum to annual", q.net_revenue_musd.sum(), s(co, sg, y), tol, "S1,S6-S8,S11-S14")
            check(f"{co} {y}: four quarters of Strip profit sum to annual", q.segment_profit_musd.sum(), s(co, sg, y, "segment_profit_musd"), tol, "S1,S6-S8,S11-S14")
# MGM Strip expenses: revenue - segment expenses = EBITDAR
for y in (2023, 2024, 2025):
    ex = cost[(cost.company == "MGM") & (cost.year == y)].amount_musd.sum()
    check(f"MGM {y}: Strip revenue minus segment expenses = Segment Adj. EBITDAR", s("MGM", MGM_STRIP, y) - ex, s("MGM", MGM_STRIP, y, "segment_profit_musd"), 0.01, "S2")
    ex = cost[(cost.company == "Caesars") & (cost.year == y)].amount_musd.sum()
    check(f"Caesars {y}: LV revenue minus segment expenses = Adj. EBITDA", s("Caesars", CZR_LV, y) - ex, s("Caesars", CZR_LV, y, "segment_profit_musd"), 1.0, "S4")
# Reported margins
for co, sg, y, rep in (("MGM", MGM_STRIP, 2025, 33.9), ("MGM", MGM_STRIP, 2024, 35.2), ("Caesars", CZR_LV, 2025, 42.7), ("Caesars", CZR_LV, 2024, 44.6)):
    check(f"{co} {y}: recomputed Strip margin matches reported {rep}%", 100 * s(co, sg, y, "segment_profit_musd") / s(co, sg, y), rep, 0.05, "S2/S4")
# RevPAR ~= occupancy x ADR (MGM rounds to whole % and $)
for _, r in kpi[(kpi.company == "MGM")].iterrows():
    check(f"MGM {r.period}: occupancy x ADR ~= RevPAR", r.occupancy * r.adr_usd, r.revpar_usd, 3.0, r.source_id)
for _, r in lva.iterrows():
    check(f"LVCVA {r.year}: Strip occupancy x Strip ADR ~= Strip RevPAR", r.strip_occupancy * r.strip_adr, r.strip_revpar, 1.0, r.source_id)
# LVCVA monthly sums
for y in (2024, 2025):
    m = lvm[lvm.year == y]
    a = lva[lva.year == y].iloc[0]
    check(f"LVCVA {y}: monthly visitor volume sums to annual", m.visitor_volume.sum(), a.visitor_volume, 1000, a.source_id)
    check(f"LVCVA {y}: monthly convention attendance sums to annual", m.convention_attendance.sum(), a.convention_attendance, 1000, a.source_id)
    check(f"LVCVA {y}: monthly Strip gaming win sums to annual ($M)", m.strip_gaming_win_usd.sum() / 1e6, a.strip_gaming_win_usd / 1e6, 1.0, a.source_id)
# NGCB vs LVCVA Strip gaming win 2025 (two primary sources)
ngcb25 = float(gam[(gam.company_or_market.str.contains("NGCB")) & (gam.year == 2025) & (gam.metric == "Gaming win")].value_musd.iloc[0])
check("2025 Strip gaming win: NGCB report vs LVCVA summary ($M)", ngcb25, lva[lva.year == 2025].strip_gaming_win_usd.iloc[0] / 1e6, 1.0, "S23,S17")
tbl = gam[(gam.year == 2025) & gam.metric.isin(["Table/counter/card win", "Slot win"])].value_musd.sum()
check("2025 Strip gaming win: table + slot = total (NGCB, $M)", tbl, ngcb25, 0.01, "S23")
hl0 = pd.read_csv(D / "highlights.csv").set_index(["item", "period"]).value_musd
for y in (2025, 2026):
    qq = qtr[(qtr.company == "MGM") & qtr.quarter.isin([f"{y}-Q1", f"{y}-Q2"])]
    check(f"MGM {y}: Q1 + Q2 Strip revenue = reported six months", qq.net_revenue_musd.sum(), float(hl0[("Las Vegas Strip Resorts net revenue (six months)", f"{y}-H1")]), 0.01, "S6,S7,S9,S10")
    check(f"MGM {y}: Q1 + Q2 Strip EBITDAR = reported six months", qq.segment_profit_musd.sum(), float(hl0[("Las Vegas Strip Resorts Segment Adjusted EBITDAR (six months)", f"{y}-H1")]), 0.01, "S6,S7,S9,S10")
lm26 = lvm[lvm.year == 2026]
check("LVCVA 2026 Jan-Aug: monthly visitors sum to YTD", lm26.visitor_volume.sum(), ytd.loc["Visitor volume", "ytd_2026"], 1000, "S22")
check("LVCVA 2026 Jan-Aug: monthly Strip gaming win sums to YTD ($M)", lm26.strip_gaming_win_usd.sum() / 1e6, ytd.loc["Strip gaming win (USD)", "ytd_2026"] / 1e6, 1.0, "S22")
check("MGM Strip rooms: property rooms sum to 10-K subtotal (37,000)", rooms.rooms.sum(), 37000, 0, "S2")

pd.DataFrame(checks).to_csv(D / "checks.csv", index=False)
n_fail = sum(c["result"] == "FAIL" for c in checks)
print(f"checks: {len(checks)} run, {len(checks) - n_fail} pass, {n_fail} fail")

# ---------- 2. Derived metrics (computed from reported figures) ----------
def pct(a, b): return 100 * (a / b - 1)
der = {}
for co, sg in (("MGM", MGM_STRIP), ("Caesars", CZR_LV)):
    r24, r25 = s(co, sg, 2024), s(co, sg, 2025)
    e24, e25 = s(co, sg, 2024, "segment_profit_musd"), s(co, sg, 2025, "segment_profit_musd")
    der[co] = {
        "rev24": r24, "rev25": r25, "rev_chg": r25 - r24, "rev_pct": pct(r25, r24),
        "prof24": e24, "prof25": e25, "prof_chg": e25 - e24, "prof_pct": pct(e25, e24),
        "margin24": 100 * e24 / r24, "margin25": 100 * e25 / r25,
        "decremental": 100 * (e24 - e25) / (r24 - r25),
    }
    m = mix[mix.company == co].pivot(index="category", columns="year", values="net_revenue_musd")
    der[co]["mix_chg"] = {c: float(m.loc[c, 2025] - m.loc[c, 2024]) for c in m.index}
    der[co]["mix_pct"] = {c: float(pct(m.loc[c, 2025], m.loc[c, 2024])) for c in m.index}
    der[co]["noncasino_share24"] = 100 * (1 - m.loc["Casino", 2024] / r24)
    der[co]["noncasino_share25"] = 100 * (1 - m.loc["Casino", 2025] / r25)
    der[co]["noncasino_chg"] = float(sum(v for k, v in der[co]["mix_chg"].items() if k != "Casino"))
lab = {"MGM": "Payroll related", "Caesars": "Labor expense"}
for co in der:
    c = cost[(cost.company == co) & (cost.cost_line == lab[co])].set_index("year").amount_musd
    der[co]["labor24"], der[co]["labor25"], der[co]["labor_pct"] = float(c[2024]), float(c[2025]), float(pct(c[2025], c[2024]))
    der[co]["labor_share24"] = 100 * c[2024] / der[co]["rev24"]; der[co]["labor_share25"] = 100 * c[2025] / der[co]["rev25"]
a = lva.set_index("year")
mk = {
    "visitors24": a.loc[2024, "visitor_volume"], "visitors25": a.loc[2025, "visitor_volume"],
    "visitors_pct": pct(a.loc[2025, "visitor_volume"], a.loc[2024, "visitor_volume"]),
    "visitors_vs2019_pct": pct(a.loc[2025, "visitor_volume"], a.loc[2019, "visitor_volume"]),
    "conv24": a.loc[2024, "convention_attendance"], "conv25": a.loc[2025, "convention_attendance"],
    "conv_pct": pct(a.loc[2025, "convention_attendance"], a.loc[2024, "convention_attendance"]),
    "adr19": a.loc[2019, "strip_adr"], "adr24": a.loc[2024, "strip_adr"], "adr25": a.loc[2025, "strip_adr"],
    "adr_pct": pct(a.loc[2025, "strip_adr"], a.loc[2024, "strip_adr"]),
    "adr24_vs2019_pct": pct(a.loc[2024, "strip_adr"], a.loc[2019, "strip_adr"]),
    "adr25_vs2019_pct": pct(a.loc[2025, "strip_adr"], a.loc[2019, "strip_adr"]),
    "revpar24": a.loc[2024, "strip_revpar"], "revpar25": a.loc[2025, "strip_revpar"],
    "revpar_pct": pct(a.loc[2025, "strip_revpar"], a.loc[2024, "strip_revpar"]),
    "occ24": 100 * a.loc[2024, "strip_occupancy"], "occ25": 100 * a.loc[2025, "strip_occupancy"],
    "mid24": 100 * a.loc[2024, "midweek_occupancy"], "mid25": 100 * a.loc[2025, "midweek_occupancy"],
    "wkd24": 100 * a.loc[2024, "weekend_occupancy"], "wkd25": 100 * a.loc[2025, "weekend_occupancy"],
    "gaming24": a.loc[2024, "strip_gaming_win_usd"] / 1e6, "gaming25": ngcb25,
    "gaming_pct": pct(ngcb25, a.loc[2024, "strip_gaming_win_usd"] / 1e6),
    "win_per_visitor24": a.loc[2024, "strip_gaming_win_usd"] / a.loc[2024, "visitor_volume"],
    "win_per_visitor25": ngcb25 * 1e6 / a.loc[2025, "visitor_volume"],
    "air_pct": pct(a.loc[2025, "airport_passengers"], a.loc[2024, "airport_passengers"]),
}
# 2026 YTD (Jan-Aug) vs same months of 2025
m25 = lvm[(lvm.year == 2025) & (lvm.month <= "2025-08")]
m26 = lvm[lvm.year == 2026]
mk["ytd26_visitors_pct"] = pct(m26.visitor_volume.sum(), m25.visitor_volume.sum())
mk["ytd26_conv_pct"] = pct(m26.convention_attendance.sum(), m25.convention_attendance.sum())
mk["ytd26_air_pct"] = pct(m26.airport_passengers.sum(), m25.airport_passengers.sum())
mk["ytd26_months"] = "Jan-Aug"
# MGM H1 2026
def qsum(co, prefix, col): return qtr[(qtr.company == co) & qtr.quarter.isin([f"{prefix}-Q1", f"{prefix}-Q2"])][col].sum()
for co in ("MGM", "Caesars"):
    der[co]["h1_26_rev_pct"] = pct(qsum(co, 2026, "net_revenue_musd"), qsum(co, 2025, "net_revenue_musd"))
    der[co]["h1_26_prof_pct"] = pct(qsum(co, 2026, "segment_profit_musd"), qsum(co, 2025, "segment_profit_musd"))
k = kpi[(kpi.company == "MGM") & (kpi.period_type == "Annual")].set_index("period")
der["MGM"].update({"occ24": 100 * k.loc["2024", "occupancy"], "occ25": 100 * k.loc["2025", "occupancy"],
                   "adr24": k.loc["2024", "adr_usd"], "adr25": k.loc["2025", "adr_usd"],
                   "revpar24": k.loc["2024", "revpar_usd"], "revpar25": k.loc["2025", "revpar_usd"]})
kc = kpi[(kpi.company == "Caesars")].set_index("period")
der["Caesars"].update({"occ24": 100 * kc.loc["2024", "occupancy"], "occ25": 100 * kc.loc["2025", "occupancy"]})
vps = vp.set_index(["metric", "year"]).value
mk["too_exp22"], mk["too_exp25"] = 100 * vps[("Share of somewhat-satisfied visitors citing 'Too expensive'", 2022)], 100 * vps[("Share of somewhat-satisfied visitors citing 'Too expensive'", 2025)]
mk["too_exp24"] = 100 * vps[("Share of somewhat-satisfied visitors citing 'Too expensive'", 2024)]
mk["intl_share25"] = 100 * vps[("International share of visitors", 2025)]
mk["conv_spend"], mk["leis_spend"] = vps[("Convention visitor spend per trip", 2025)], vps[("Leisure visitor spend per trip", 2025)]
value_rooms = int(rooms[rooms.tier == "Value"].rooms.sum())
der["MGM"]["value_rooms"], der["MGM"]["value_room_share"] = value_rooms, 100 * value_rooms / rooms.rooms.sum()
dg = dig.set_index(["company", "item", "year"]).value_musd
der["MGM"]["betmgm24"], der["MGM"]["betmgm25"] = dg[("MGM", "MGM share of BetMGM North America Venture operating income (loss)", 2024)], dg[("MGM", "MGM share of BetMGM North America Venture operating income (loss)", 2025)]

# Highlights (strengths), all from reported figures
hl = pd.read_csv(D / "highlights.csv").set_index(["item", "period"]).value_musd
def segv(sg, y, col="net_revenue_musd"): return float(seg[(seg.company == "MGM") & (seg.segment == sg) & (seg.year == y)][col].iloc[0])
DIG = "MGM Digital (mainly LeoVegas; BetMGM JV not included)"
gm = gam.set_index(["company_or_market", "year", "metric"]).value_musd
pos = {
    "cons_rev24": segv("Consolidated", 2024), "cons_rev25": segv("Consolidated", 2025),
    "cons_rev_pct": pct(segv("Consolidated", 2025), segv("Consolidated", 2024)),
    "china_rev_pct": pct(segv("MGM China", 2025), segv("MGM China", 2024)),
    "china_prof_pct": pct(segv("MGM China", 2025, "segment_profit_musd"), segv("MGM China", 2024, "segment_profit_musd")),
    "regional_rev_pct": pct(segv("Regional Operations", 2025), segv("Regional Operations", 2024)),
    "regional_prof_pct": pct(segv("Regional Operations", 2025, "segment_profit_musd"), segv("Regional Operations", 2024, "segment_profit_musd")),
    "digital_rev_pct": pct(segv(DIG, 2025), segv(DIG, 2024)),
    "betmgm_dist25": float(hl[("BetMGM North America Venture distributions to MGM Resorts", "2025-Q4")]),
    "q4_casino_pct": pct(hl[("Las Vegas Strip Resorts casino revenue", "2025-Q4")], hl[("Las Vegas Strip Resorts casino revenue", "2024-Q4")]),
    "q4_table_win_pct": pct(hl[("Las Vegas Strip Resorts table games win", "2025-Q4")], hl[("Las Vegas Strip Resorts table games win", "2024-Q4")]),
    "mgm_drop_pct": pct(gm[("MGM Las Vegas Strip Resorts", 2025, "Table games drop")], gm[("MGM Las Vegas Strip Resorts", 2024, "Table games drop")]),
    "mgm_handle_pct": pct(gm[("MGM Las Vegas Strip Resorts", 2025, "Slot handle")], gm[("MGM Las Vegas Strip Resorts", 2024, "Slot handle")]),
    "czr_drop_pct": pct(gm[("Caesars Las Vegas", 2025, "Table games drop")], gm[("Caesars Las Vegas", 2024, "Table games drop")]),
    "czr_handle_pct": pct(gm[("Caesars Las Vegas", 2025, "Slot handle")], gm[("Caesars Las Vegas", 2024, "Slot handle")]),
    "occ_gap_pts": der["MGM"]["occ25"] - mk["occ25"],
    "adr_premium_pct": pct(der["MGM"]["adr25"], mk["adr25"]),
}
q = qtr[qtr.company == "MGM"].set_index("quarter").net_revenue_musd
pos["q2_26_rev_pct"] = pct(q["2026-Q2"], q["2025-Q2"])
pos["q1_26_rev_pct"] = pct(q["2026-Q1"], q["2025-Q1"])
# 2026 so far (reported Q1 and Q2 2026; Q3 2026 results due Oct 28 2026)
qp = qtr[qtr.company == "MGM"].set_index("quarter").segment_profit_musd
for qn in ("Q1", "Q2"):
    pos[f"{qn.lower()}_26_rev"], pos[f"{qn.lower()}_25_rev"] = q[f"2026-{qn}"], q[f"2025-{qn}"]
    pos[f"{qn.lower()}_26_prof"], pos[f"{qn.lower()}_25_prof"] = qp[f"2026-{qn}"], qp[f"2025-{qn}"]
    pos[f"{qn.lower()}_26_prof_pct"] = pct(qp[f"2026-{qn}"], qp[f"2025-{qn}"])
    pos[f"{qn.lower()}_26_margin"], pos[f"{qn.lower()}_25_margin"] = 100 * qp[f"2026-{qn}"] / q[f"2026-{qn}"], 100 * qp[f"2025-{qn}"] / q[f"2025-{qn}"]
def h(item, a, b): return float(hl[(item, a)]), float(hl[(item, b)])
pos["h1_26_rev"], pos["h1_25_rev"] = h("Las Vegas Strip Resorts net revenue (six months)", "2026-H1", "2025-H1")
pos["h1_26_prof"], pos["h1_25_prof"] = h("Las Vegas Strip Resorts Segment Adjusted EBITDAR (six months)", "2026-H1", "2025-H1")
pos["q2_26_casino"], pos["q2_25_casino"] = h("Las Vegas Strip Resorts casino revenue", "2026-Q2", "2025-Q2")
pos["q2_26_casino_pct"] = pct(pos["q2_26_casino"], pos["q2_25_casino"])
pos["q2_26_tablewin_pct"] = pct(*h("Las Vegas Strip Resorts table games win", "2026-Q2", "2025-Q2"))
pos["q2_26_roomrev"], pos["q2_25_roomrev"] = h("Las Vegas Strip Resorts room revenue", "2026-Q2", "2025-Q2")
for item, kk in (("Consolidated net revenues (six months)", "cons"), ("MGM China net revenues (six months)", "china"), ("MGM Digital net revenues (six months)", "digital")):
    a26, a25 = h(item, "2026-H1", "2025-H1"); pos[f"h1_26_{kk}_rev"], pos[f"h1_26_{kk}_pct"] = a26, pct(a26, a25)
pos["h1_26_betmgm"], pos["h1_25_betmgm"] = h("MGM share of BetMGM North America Venture operating income (six months)", "2026-H1", "2025-H1")
kq = kpi[(kpi.company == "MGM")].set_index("period")
for qn in ("2026-Q1", "2026-Q2", "2025-Q2"):
    t = qn.replace("-", "_").lower()
    pos[f"occ_{t}"], pos[f"adr_{t}"], pos[f"revpar_{t}"] = 100 * kq.loc[qn, "occupancy"], kq.loc[qn, "adr_usd"], kq.loc[qn, "revpar_usd"]
mq2 = lvm[lvm.month.isin(["2026-04", "2026-05", "2026-06"])]
mk["q2_26_strip_occ"] = 100 * mq2.strip_occupancy.mean()
mk["ytd26_gaming_pct"] = 100 * ytd.loc["Strip gaming win (USD)", "yoy_change"]
mk["ytd26_gaming"] = ytd.loc["Strip gaming win (USD)", "ytd_2026"] / 1e6
mk["ytd26_adr"], mk["ytd26_adr_pct"] = ytd.loc["Strip ADR (USD)", "ytd_2026"], 100 * ytd.loc["Strip ADR (USD)", "yoy_change"]
mk["ytd26_conv"] = ytd.loc["Convention attendance", "ytd_2026"]
mk["ytd26_visitors"] = ytd.loc["Visitor volume", "ytd_2026"]
mk["ytd26_wkd"], mk["ytd26_mid"] = 100 * ytd.loc["Weekend occupancy (all Las Vegas)", "ytd_2026"], 100 * ytd.loc["Midweek occupancy (all Las Vegas)", "ytd_2026"]
mk["ytd26_strip_occ"] = 100 * ytd.loc["Strip occupancy", "ytd_2026"]
# Q3 2026 and first nine months 2026 (MGM Q3 2026 release Oct 28 2026, S28; 10-Q, S29)
for qn in ("Q3",):
    pos[f"{qn.lower()}_26_rev"], pos[f"{qn.lower()}_25_rev"] = q[f"2026-{qn}"], q[f"2025-{qn}"]
    pos[f"{qn.lower()}_26_prof"], pos[f"{qn.lower()}_25_prof"] = qp[f"2026-{qn}"], qp[f"2025-{qn}"]
    pos[f"{qn.lower()}_26_rev_pct"] = pct(q[f"2026-{qn}"], q[f"2025-{qn}"])
    pos[f"{qn.lower()}_26_prof_pct"] = pct(qp[f"2026-{qn}"], qp[f"2025-{qn}"])
    pos[f"{qn.lower()}_26_margin"], pos[f"{qn.lower()}_25_margin"] = 100 * qp[f"2026-{qn}"] / q[f"2026-{qn}"], 100 * qp[f"2025-{qn}"] / q[f"2025-{qn}"]
pos["q3_26_casino"], pos["q3_25_casino"] = h("Las Vegas Strip Resorts casino revenue", "2026-Q3", "2025-Q3")
pos["q3_26_casino_pct"] = pct(pos["q3_26_casino"], pos["q3_25_casino"])
pos["q3_26_tablewin_pct"] = pct(*h("Las Vegas Strip Resorts table games win", "2026-Q3", "2025-Q3"))
pos["q3_26_drop_pct"] = pct(*h("Las Vegas Strip Resorts table games drop", "2026-Q3", "2025-Q3"))
pos["q3_26_roomrev"], pos["q3_25_roomrev"] = h("Las Vegas Strip Resorts room revenue", "2026-Q3", "2025-Q3")
pos["q3_26_roomrev_pct"] = pct(pos["q3_26_roomrev"], pos["q3_25_roomrev"])
pos["n9_26_rev"], pos["n9_25_rev"] = h("Las Vegas Strip Resorts net revenue (nine months)", "2026-9M", "2025-9M")
pos["n9_26_prof"], pos["n9_25_prof"] = h("Las Vegas Strip Resorts Segment Adjusted EBITDAR (nine months)", "2026-9M", "2025-9M")
pos["n9_26_rev_pct"], pos["n9_26_prof_pct"] = pct(pos["n9_26_rev"], pos["n9_25_rev"]), pct(pos["n9_26_prof"], pos["n9_25_prof"])
pos["n9_26_payroll"], pos["n9_25_payroll"] = h("Las Vegas Strip Resorts payroll related expense (nine months)", "2026-9M", "2025-9M")
for item, kk in (("Consolidated net revenues (nine months)", "cons"), ("MGM China net revenues (nine months)", "china"), ("MGM Digital net revenues (nine months)", "digital")):
    a26, a25 = h(item, "2026-9M", "2025-9M"); pos[f"n9_26_{kk}_rev"], pos[f"n9_26_{kk}_pct"] = a26, pct(a26, a25)
pos["n9_26_betmgm"], pos["n9_25_betmgm"] = h("MGM share of BetMGM North America Venture operating income (nine months)", "2026-9M", "2025-9M")
for qn in ("2026-Q3", "2025-Q3"):
    t = qn.replace("-", "_").lower()
    pos[f"occ_{t}"], pos[f"adr_{t}"], pos[f"revpar_{t}"] = 100 * kq.loc[qn, "occupancy"], kq.loc[qn, "adr_usd"], kq.loc[qn, "revpar_usd"]
# Q3 2026 Strip average occupancy: LVCVA July and August (S22) plus September 80.1% (S30)
mk["q3_26_strip_occ"] = 100 * (lvm[lvm.month.isin(["2026-07", "2026-08"])].strip_occupancy.sum() + 0.801) / 3
for y in (2025, 2026):
    qq = qtr[(qtr.company == "MGM") & qtr.quarter.isin([f"{y}-Q1", f"{y}-Q2", f"{y}-Q3"])]
    check(f"MGM {y}: Q1 + Q2 + Q3 Strip revenue = reported nine months", qq.net_revenue_musd.sum(), float(hl0[("Las Vegas Strip Resorts net revenue (nine months)", f"{y}-9M")]), 0.01, "S6-S10,S28")
    check(f"MGM {y}: Q1 + Q2 + Q3 Strip EBITDAR = reported nine months", qq.segment_profit_musd.sum(), float(hl0[("Las Vegas Strip Resorts Segment Adjusted EBITDAR (nine months)", f"{y}-9M")]), 0.01, "S6-S10,S28")
pd.DataFrame(checks).to_csv(D / "checks.csv", index=False)
n_fail = sum(c["result"] == "FAIL" for c in checks)
print(f"checks incl. nine months: {len(checks)} run, {len(checks) - n_fail} pass, {n_fail} fail")

flat = []
for co in der:
    for kk, v in der[co].items():
        if not isinstance(v, dict): flat.append({"scope": co, "metric": kk, "value": round(float(v), 4)})
for kk, v in pos.items():
    flat.append({"scope": "MGM highlights", "metric": kk, "value": round(float(v), 4)})
for kk, v in mk.items():
    if not isinstance(v, str): flat.append({"scope": "Las Vegas market", "metric": kk, "value": round(float(v), 4)})
pd.DataFrame(flat).to_csv(D / "derived_metrics.csv", index=False)

# ---------- 3. KPI signals behind the recommendations (no dollar estimates) ----------
M = der["MGM"]
sig = {
    "midweek_gap_pts": mk["ytd26_wkd"] - mk["ytd26_mid"],                 # weekend minus midweek occupancy, Jan-Aug 2026
    "conv_spend_premium_pct": 100 * (mk["conv_spend"] / mk["leis_spend"] - 1),  # convention vs leisure spend per trip, 2025
    "payroll_share25": M["labor_share25"],
}
sig["midweek_third_pts"] = sig["midweek_gap_pts"] / 3
# cost efficiency signals: segment costs = net revenue minus Segment Adjusted EBITDAR (reported figures)
for y in (2023, 2024, 2025):
    sig[f"margin{y % 100}"] = 100 * s("MGM", MGM_STRIP, y, "segment_profit_musd") / s("MGM", MGM_STRIP, y)
sig["h1_26_margin"] = 100 * pos["h1_26_prof"] / pos["h1_26_rev"]
sig["h1_25_margin"] = 100 * pos["h1_25_prof"] / pos["h1_25_rev"]
sig["h1_26_cost_pct"] = pct(pos["h1_26_rev"] - pos["h1_26_prof"], pos["h1_25_rev"] - pos["h1_25_prof"])
sig["q1_26_cost_pct"] = pct(pos["q1_26_rev"] - pos["q1_26_prof"], pos["q1_25_rev"] - pos["q1_25_prof"])
sig["payroll_share24"] = M["labor_share24"]
sig["n9_26_margin"] = 100 * pos["n9_26_prof"] / pos["n9_26_rev"]
sig["n9_25_margin"] = 100 * pos["n9_25_prof"] / pos["n9_25_rev"]
sig["n9_26_cost_pct"] = pct(pos["n9_26_rev"] - pos["n9_26_prof"], pos["n9_25_rev"] - pos["n9_25_prof"])
sig["q3_26_cost_pct"] = pct(pos["q3_26_rev"] - pos["q3_26_prof"], pos["q3_25_rev"] - pos["q3_25_prof"])
sig["n9_26_payroll_share"] = 100 * pos["n9_26_payroll"] / pos["n9_26_rev"]
sig["n9_25_payroll_share"] = 100 * pos["n9_25_payroll"] / pos["n9_25_rev"]
sig["midweek_target"] = mk["ytd26_mid"] + sig["midweek_third_pts"]
print({k: round(v, 2) for k, v in sig.items()})

# ---------- 4. Dashboard data ----------
out = {
    "der": der, "mk": mk, "sig": sig, "pos": pos,
    "segments": seg.to_dict("records"), "mix": mix.to_dict("records"), "costs": cost.to_dict("records"),
    "kpi": kpi.astype(object).fillna("").to_dict("records"), "qtr": qtr.to_dict("records"), "lva": lva.astype(object).fillna("").to_dict("records"),
    "lvm": lvm.astype(object).fillna("").to_dict("records"), "vp": vp.to_dict("records"), "digital": dig.astype(object).fillna("").to_dict("records"),
    "checks": {"n": len(checks), "pass": len(checks) - n_fail}, "rooms": rooms.to_dict("records"),
}
(ROOT / "docs" / "data.js").write_text("window.D=" + json.dumps(out, default=float) + ";\n")
print("wrote docs/data.js")

if n_fail:
    raise SystemExit(f"{n_fail} checks failed")
