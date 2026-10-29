"""Writes SOURCES.md: the source list (S-ids used in every data/*.csv row) and a register of every headline figure
quoted in the dashboard and README, with its source URL."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
D = json.loads((ROOT / "docs" / "data.js").read_text()[len("window.D="):-2])
M, C, K, G = D["der"]["MGM"], D["der"]["Caesars"], D["mk"], D["sig"]
P = D["pos"]
SEC_M, SEC_C = "https://www.sec.gov/Archives/edgar/data/789570/", "https://www.sec.gov/Archives/edgar/data/1590895/"
SV = "https://assets.simpleviewcms.com/simpleview/"
S = {
 "S1": ("MGM Resorts: Q4 and full-year 2025 earnings release (8-K Ex. 99.1, Feb 5 2026)", SEC_M + "000078957026000013/mgmexhibit991q42025er.htm"),
 "S2": ("MGM Resorts: Form 10-K for FY2025 (filed Feb 11 2026)", SEC_M + "000078957026000018/mgm-20251231.htm"),
 "S3": ("Caesars Entertainment: Q4 and full-year 2025 earnings release (8-K Ex. 99.1, Feb 17 2026)", SEC_C + "000159089526000010/ex991-2025q4ceiearningsrel.htm"),
 "S4": ("Caesars Entertainment: Form 10-K for FY2025 (filed Feb 17 2026); segment table also in XBRL R104", SEC_C + "000159089526000011/czr-20251231.htm"),
 "S5": ("MGM Resorts: Q4 2024 earnings release (cross-check of 2024 figures)", SEC_M + "000078957025000005/mgmexhibit991q42024er.htm"),
 "S6": ("MGM Resorts: Q1 2025 earnings release", SEC_M + "000078957025000019/mgmex991q12025earningrelea.htm"),
 "S7": ("MGM Resorts: Q2 2025 earnings release", SEC_M + "000078957025000032/mgmex991q22025earningrelea.htm"),
 "S8": ("MGM Resorts: Q3 2025 earnings release", SEC_M + "000078957025000073/mgmex991q32025earningrelea.htm"),
 "S9": ("MGM Resorts: Q1 2026 earnings release", SEC_M + "000078957026000034/mgmex991q12026earningrelea.htm"),
 "S10": ("MGM Resorts: Q2 2026 earnings release", SEC_M + "000078957026000075/mgmex991q22026earningrelea.htm"),
 "S11": ("Caesars: Q4 2024 earnings release", SEC_C + "000159089525000065/ex991-2024q4ceiearningsrel.htm"),
 "S12": ("Caesars: Q1 2025 earnings release", SEC_C + "000159089525000108/ex991-2025q1ceiearningsrel.htm"),
 "S13": ("Caesars: Q2 2025 earnings release", SEC_C + "000159089525000125/ex991-2025q2ceiearningsrel.htm"),
 "S14": ("Caesars: Q3 2025 earnings release", SEC_C + "000159089525000129/ex991-2025q3ceiearningsrel.htm"),
 "S15": ("Caesars: Q1 2026 earnings release", SEC_C + "000159089526000015/ex991-2026q1ceiearningsrel.htm"),
 "S16": ("Caesars: Q2 2026 earnings release", SEC_C + "000159089526000027/ex991-2026q2ceiearningsrel.htm"),
 "S17": ("LVCVA Year-End Summary 2025 (revised, as of Aug 20 2026), xlsx", SV + "raw/upload/v1/clients/lasvegas/Year_to_Date_Summary_for_2025_revised_cd675d1a-2e15-4a20-aeeb-e6a6d871b10a.xlsx"),
 "S18": ("LVCVA Year-End Summary 2024 (as of Feb 26 2025), xlsx", SV + "raw/upload/v1/clients/lasvegas/Year_to_Date_Summary_for_2024_0d625f44-ecbe-4fc2-917b-a2e6b3c794d3.xlsx"),
 "S19": ("LVCVA Year-End Summary 2023 (revised), xlsx", SV + "raw/upload/v1/clients/lasvegas/Year_to_Date_Summary_for_2023_Revised_770fdfda-2ef5-4b3a-ba37-c0e8dbb0384b.xlsx"),
 "S20": ("LVCVA Year-End Summary 2022, xlsx", SV + "raw/upload/v1/clients/lasvegas/Year_to_Date_Summary_for_2022_4ae9840a-74b0-42c5-ba75-830b8b627eb6.xlsx"),
 "S21": ("LVCVA Year-End Summary 2019 (revised), xlsx", SV + "raw/upload/v1/clients/lasvegas/Year_End_Summary_for_2019_Revised_55959cc8-b556-4835-90da-c1d2d05c5332.xlsx"),
 "S22": ("LVCVA Year-to-Date Summary 2026 (Jan-Aug, as of Sep 30 2026), xlsx", SV + "raw/upload/v1/clients/lasvegas/Year_to_Date_Summary_for_2026_04a9b26c-a10f-4212-a95b-96e76402e16c.xlsx"),
 "S23": ("Nevada Gaming Control Board: Monthly Revenue Report, December 2025 (Strip 12-month totals)", "https://www.gaming.nv.gov/siteassets/content/about/gaming-revenue/december-2025-monthly-revenue-report.pdf"),
 "S24": ("Nevada Gaming Control Board: Abbreviated Revenue Release, December 2025", "https://www.gaming.nv.gov/siteassets/content/about/abb-revenue/mrrdec2025.pdf"),
 "S25": ("LVCVA: 2025 Las Vegas Visitor Profile Study (Figures 25, 26, 45; visitor origin table)", SV + "image/upload/v1/clients/lasvegas/2025_Las_Vegas_Visitor_Profile_Study_db57c923-1f87-4ab8-868d-d6fc0bf2f972.pdf"),
 "S26": ("LVCVA / Applied Analysis: The Economic Impact of Southern Nevada's Tourism Industry, 2025 (July 2026)", "https://res.cloudinary.com/simpleview/image/upload/v1784063295/clients/lasvegas/Economic_Impact_of_Visitors_2025_FINAL_6fa0ea36-212f-4b24-beb8-d407ceea05b7.pdf"),
 "S27": ("LVCVA: Executive Summary of Southern Nevada Tourism Indicators (index page linking S17-S22)", "https://www.lvcva.com/research/reports/post/lvcva-executive-summary-of-southern-nevada-tourism-indicators/"),
 "S28": ("MGM Resorts: Q3 2026 earnings release (Oct 28 2026)", "https://investors.mgmresorts.com/2026-10-28-MGM-RESORTS-INTERNATIONAL-REPORTS-THIRD-QUARTER-2026-FINANCIAL-AND-OPERATING-RESULTS"),
 "S29": ("MGM Resorts: Form 10-Q for the quarter ended Sep 30 2026", SEC_M + "000078957026000107/mgm-20260930.htm"),
 "S30": ("LVCVA: September 2026 Executive Summary (Strip occupancy 80.1%, released Oct 29 2026; figures as reported by FOX5 Las Vegas)", "https://www.fox5vegas.com/2026/10/29/las-vegas-visitor-volume-remains-steady-hotel-occupancy-drops-september-lvcva-reports/"),
}
def u(sid): return S[sid][1]
R = [
 ("MGM Strip net revenue 2025 / 2024", f"${M['rev25']:,.1f}M / ${M['rev24']:,.1f}M ({M['rev_pct']:+.1f}%)", "S2", "reported"),
 ("MGM Strip Segment Adj. EBITDAR 2025 / 2024", f"${M['prof25']:,.1f}M / ${M['prof24']:,.1f}M ({M['prof_pct']:+.1f}%)", "S2", "reported"),
 ("MGM Strip EBITDAR margin 2025 / 2024", f"{M['margin25']:.1f}% / {M['margin24']:.1f}%", "S2", "reported (recomputed, ties)"),
 ("Caesars Las Vegas net revenue 2025 / 2024", f"${C['rev25']:,.0f}M / ${C['rev24']:,.0f}M ({C['rev_pct']:+.1f}%)", "S4", "reported"),
 ("Caesars Las Vegas Adj. EBITDA 2025 / 2024", f"${C['prof25']:,.0f}M / ${C['prof24']:,.0f}M ({C['prof_pct']:+.1f}%)", "S4", "reported; same-store -8.6% per S3"),
 ("Caesars Las Vegas margin 2025 / 2024", f"{C['margin25']:.1f}% / {C['margin24']:.1f}%", "S4", "reported"),
 ("MGM Strip casino revenue change", f"{M['mix_chg']['Casino']:+.1f} $M ({M['mix_pct']['Casino']:+.1f}%)", "S2", "derived from reported"),
 ("MGM Strip rooms revenue change", f"{M['mix_chg']['Rooms']:+.1f} $M ({M['mix_pct']['Rooms']:+.1f}%)", "S2", "derived from reported"),
 ("MGM Strip F&B / entertainment change", f"{M['mix_chg']['Food & beverage']:+.1f} / {M['mix_chg']['Entertainment, retail & other']:+.1f} $M", "S2", "derived"),
 ("MGM Strip non-casino revenue change", f"{M['noncasino_chg']:+.1f} $M = {100*M['noncasino_chg']/M['rev_chg']:.0f}% of total decline", "S2", "derived"),
 ("MGM non-casino share of Strip revenue 2025", f"{M['noncasino_share25']:.1f}%", "S2", "derived"),
 ("Caesars LV casino / hotel / F&B / other change", f"{C['mix_chg']['Casino']:+.0f} / {C['mix_chg']['Rooms']:+.0f} / {C['mix_chg']['Food & beverage']:+.0f} / {C['mix_chg']['Entertainment, retail & other']:+.0f} $M", "S4", "reported variance"),
 ("MGM Strip occupancy / ADR / RevPAR 2025 vs 2024", f"{M['occ25']:.0f}% vs {M['occ24']:.0f}%; ${M['adr25']:.0f} vs ${M['adr24']:.0f}; ${M['revpar25']:.0f} vs ${M['revpar24']:.0f}", "S2", "reported"),
 ("Caesars LV hotel occupancy 2025 / 2024", f"{C['occ25']:.1f}% / {C['occ24']:.1f}%", "S4", "reported"),
 ("MGM Strip payroll 2025 / 2024", f"${M['labor25']:,.1f}M / ${M['labor24']:,.1f}M ({M['labor_pct']:+.1f}%)", "S2", "reported (segment expense note)"),
 ("Caesars LV labor expense 2025 / 2024", f"${C['labor25']:,.0f}M / ${C['labor24']:,.0f}M ({C['labor_pct']:+.1f}%)", "S4", "reported (segment note / XBRL R104)"),
 ("Decremental margin MGM / Caesars", f"{M['decremental']:.0f}% / {C['decremental']:.0f}%", "S2,S4", "derived"),
 ("MGM Strip H1 2026 revenue / EBITDAR YoY", f"{M['h1_26_rev_pct']:+.1f}% / {M['h1_26_prof_pct']:+.1f}%", "S9,S10,S6,S7", "derived from reported quarters"),
 ("Caesars LV H1 2026 revenue / EBITDA YoY", f"{C['h1_26_rev_pct']:+.1f}% / {C['h1_26_prof_pct']:+.1f}%", "S15,S16,S12,S13", "derived from reported quarters"),
 ("MGM Strip rooms (10-K property table)", f"37,000; value tier (Luxor, Excalibur, NYNY) {M['value_rooms']:,} = {M['value_room_share']:.0f}%", "S2", "reported; value-tier grouping is my own"),
 ("MGM share of BetMGM operating income 2025 / 2024", f"${M['betmgm25']:.1f}M / ${M['betmgm24']:.1f}M", "S2", "reported"),
 ("MGM Digital (mainly LeoVegas; BetMGM JV reported separately) revenue / EBITDAR 2025", "$654.2M / -$90.3M", "S2", "reported"),
 ("Caesars Digital revenue / Adj. EBITDA 2025 (2024)", "$1,408M / $236M ($1,163M / $117M)", "S4", "reported"),
 ("Las Vegas visitor volume 2025 / 2024 / 2019", f"{K['visitors25']:,.0f} / {K['visitors24']:,.0f} / 42,523,700 ({K['visitors_pct']:+.1f}% YoY; {K['visitors_vs2019_pct']:+.1f}% vs 2019)", "S17,S18,S21", "reported"),
 ("Convention attendance 2025 / 2024", f"{K['conv25']:,.0f} / {K['conv24']:,.0f} ({K['conv_pct']:+.1f}%)", "S17,S18", "reported"),
 ("Strip ADR 2025 / 2024 / 2019", f"${K['adr25']:.2f} / ${K['adr24']:.2f} / ${K['adr19']:.2f}", "S17,S18,S21", "reported (2025 revised; original Jan 2026 release showed $196.54)"),
 ("Strip RevPAR 2025 / 2024", f"${K['revpar25']:.2f} / ${K['revpar24']:.2f} ({K['revpar_pct']:+.1f}%)", "S17,S18", "reported"),
 ("Strip occupancy 2025 / 2024", f"{K['occ25']:.1f}% / {K['occ24']:.1f}%", "S17,S18", "reported"),
 ("Midweek / weekend occupancy 2025 vs 2024 (all Las Vegas)", f"{K['mid25']:.1f}% vs {K['mid24']:.1f}%; {K['wkd25']:.1f}% vs {K['wkd24']:.1f}%", "S17,S18", "reported"),
 ("Strip gaming win 2025 / 2024", f"${K['gaming25']:,.1f}M / ${K['gaming24']:,.1f}M ({K['gaming_pct']:+.2f}%)", "S23,S18", "reported (NGCB)"),
 ("Airport passengers 2025 YoY", f"{K['air_pct']:+.1f}%", "S17,S18", "reported"),
 ("2026 Jan-Aug YoY: visitors / conventions / airport", f"{K['ytd26_visitors_pct']:+.1f}% / {K['ytd26_conv_pct']:+.1f}% / {K['ytd26_air_pct']:+.1f}%", "S22,S17", "derived from reported months"),
 ("'Too expensive' share of somewhat-satisfied visitors 2025 / 2024 / 2022", "22% / 18% / 14%", "S25", "reported (Figure 45)"),
 ("Avg lodging spend per night 2025 / 2024", "$174.52 / $179.10", "S25", "reported (Figure 26)"),
 ("International share of visitors 2023-2025", "12% each year", "S25", "reported"),
 ("Convention vs leisure spend per trip 2025", "$1,795 vs $1,230", "S26", "reported"),
 ("MGM consolidated net revenue 2025 / 2024", f"${P['cons_rev25']:,.1f}M / ${P['cons_rev24']:,.1f}M ({P['cons_rev_pct']:+.1f}%)", "S1,S2", "reported"),
 ("MGM China net revenue / Segment Adj. EBITDAR change 2025", f"{P['china_rev_pct']:+.1f}% / {P['china_prof_pct']:+.1f}%", "S1,S2", "derived from reported"),
 ("MGM Regional Operations revenue / EBITDAR change 2025", f"{P['regional_rev_pct']:+.1f}% / {P['regional_prof_pct']:+.1f}%", "S1,S2", "derived from reported"),
 ("MGM Digital net revenue change 2025", f"{P['digital_rev_pct']:+.1f}%", "S1,S2", "derived from reported"),
 ("BetMGM distribution to MGM Resorts, Q4 2025", f"${P['betmgm_dist25']:.0f}M", "S1", "reported"),
 ("MGM Strip casino revenue Q4 2025 / Q4 2024", "$569M / $501M (+13% as reported)", "S1", "reported (key gaming statistics)"),
 ("MGM Strip table games win Q4 2025 / Q4 2024", "$473M / $392M (+21% as reported)", "S1", "reported"),
 ("MGM Strip table games drop / slot handle change 2025", f"{P['mgm_drop_pct']:+.1f}% / {P['mgm_handle_pct']:+.1f}%", "S2", "derived from reported"),
 ("Caesars LV table games drop / slot handle change 2025", f"{P['czr_drop_pct']:+.1f}% / {P['czr_handle_pct']:+.1f}%", "S4", "derived from reported"),
 ("MGM Strip occupancy vs Strip average 2025", f"{M['occ25']:.0f}% vs {K['occ25']:.1f}% ({P['occ_gap_pts']:+.1f} pts)", "S2,S17", "derived; company-reported vs LVCVA survey, directional"),
 ("MGM Strip ADR vs Strip average ADR 2025", f"${M['adr25']:.0f} vs ${K['adr25']:.2f} ({P['adr_premium_pct']:+.0f}%)", "S2,S17", "derived; company-reported vs LVCVA survey, directional"),
 ("MGM Strip net revenue Q1 / Q2 2026 YoY", f"{P['q1_26_rev_pct']:+.1f}% / {P['q2_26_rev_pct']:+.1f}%", "S9,S10,S6,S7", "derived from reported quarters"),
 ("MGM Strip net revenue Q1 2026 / Q1 2025", f"${P['q1_26_rev']:,.1f}M / ${P['q1_25_rev']:,.1f}M ({P['q1_26_rev_pct']:+.1f}%)", "S9", "reported"),
 ("MGM Strip net revenue Q2 2026 / Q2 2025", f"${P['q2_26_rev']:,.1f}M / ${P['q2_25_rev']:,.1f}M ({P['q2_26_rev_pct']:+.1f}%)", "S10", "reported"),
 ("MGM Strip Segment Adj. EBITDAR Q1 2026 / Q1 2025", f"${P['q1_26_prof']:,.1f}M / ${P['q1_25_prof']:,.1f}M ({P['q1_26_prof_pct']:+.1f}%)", "S9", "reported"),
 ("MGM Strip Segment Adj. EBITDAR Q2 2026 / Q2 2025", f"${P['q2_26_prof']:,.1f}M / ${P['q2_25_prof']:,.1f}M ({P['q2_26_prof_pct']:+.1f}%)", "S10", "reported"),
 ("MGM Strip EBITDAR margin Q1 / Q2 2026 (prior year)", f"{P['q1_26_margin']:.1f}% ({P['q1_25_margin']:.1f}%) / {P['q2_26_margin']:.1f}% ({P['q2_25_margin']:.1f}%)", "S9,S10", "derived from reported"),
 ("MGM Strip net revenue / EBITDAR, first half 2026 vs 2025", f"${P['h1_26_rev']:,.1f}M vs ${P['h1_25_rev']:,.1f}M; ${P['h1_26_prof']:,.1f}M vs ${P['h1_25_prof']:,.1f}M", "S10", "reported (six-month columns; ties to Q1 + Q2)"),
 ("MGM Strip casino revenue Q2 2026 / Q2 2025", f"${P['q2_26_casino']:.0f}M / ${P['q2_25_casino']:.0f}M (+17% as reported)", "S10", "reported (key gaming statistics)"),
 ("MGM Strip table games win Q2 2026 / Q2 2025", "$451M / $355M (+27% as reported); win % 29.6% vs 22.9%", "S10", "reported"),
 ("MGM Strip casino revenue Q1 2026 / Q1 2025", "$513M / $538M ((5)% as reported)", "S9", "reported"),
 ("MGM Strip room revenue Q1 / Q2 2026 (prior year)", "$751M ($750M) / $717M ($735M)", "S9,S10", "reported"),
 ("MGM Strip occupancy / ADR / RevPAR Q1 2026 (Q1 2025)", "92% (94%); $257 ($257); $238 ($242)", "S9", "reported"),
 ("MGM Strip occupancy / ADR / RevPAR Q2 2026 (Q2 2025)", "93% (93%); $242 ($252); $224 ($235)", "S10", "reported"),
 ("Strip occupancy, average of Apr to Jun 2026", f"{K['q2_26_strip_occ']:.1f}%", "S22", "derived (simple average of reported months); LVCVA survey vs company data, directional"),
 ("MGM consolidated net revenue, first half 2026 / 2025", f"${P['h1_26_cons_rev']:,.1f}M ({P['h1_26_cons_pct']:+.1f}%); record Q1 and record Q2", "S9,S10", "reported"),
 ("MGM China / MGM Digital net revenue change, first half 2026", f"{P['h1_26_china_pct']:+.1f}% / {P['h1_26_digital_pct']:+.1f}%", "S10", "derived from reported six-month columns"),
 ("MGM share of BetMGM operating income, first half 2026 / 2025", f"${P['h1_26_betmgm']:.1f}M / ${P['h1_25_betmgm']:.1f}M", "S9,S10", "derived (sum of reported quarters)"),
 ("Las Vegas 2026 YTD (Jan to Aug): conventions / visitors", f"{K['ytd26_conv']:,.0f} ({K['ytd26_conv_pct']:+.1f}%) / {K['ytd26_visitors_pct']:+.1f}%", "S22", "reported"),
 ("Strip gaming win 2026 YTD (Jan to Aug)", f"${K['ytd26_gaming']:,.1f}M ({K['ytd26_gaming_pct']:+.1f}%)", "S22", "reported (LVCVA citing NGCB)"),
 ("Strip ADR 2026 YTD (Jan to Aug)", f"${K['ytd26_adr']:.2f} ({K['ytd26_adr_pct']:+.1f}%)", "S22", "reported"),
 ("Weekend / midweek occupancy 2026 YTD (all Las Vegas)", f"{K['ytd26_wkd']:.1f}% / {K['ytd26_mid']:.1f}%", "S22", "reported"),
 ("Midweek occupancy gap, 2026 Jan to Aug (all Las Vegas)", f"{G['midweek_gap_pts']:.1f} pts (weekend {K['ytd26_wkd']:.1f}% minus midweek {K['ytd26_mid']:.1f}%); a third of the gap = {G['midweek_third_pts']:.1f} pts, to about {G['midweek_target']:.0f}%", "S22", "derived; target is a simple illustrative goal"),
 ("MGM Strip payroll as share of Strip revenue 2025 / 2024", f"{G['payroll_share25']:.1f}% / {G['payroll_share24']:.1f}%", "S2", "derived"),
 ("MGM Strip EBITDAR margin 2023 / 2024 / 2025 / H1 2026 (H1 2025)", f"{G['margin23']:.1f}% / {G['margin24']:.1f}% / {G['margin25']:.1f}% / {G['h1_26_margin']:.1f}% ({G['h1_25_margin']:.1f}%)", "S2,S10", "derived from reported"),
 ("MGM Strip costs (revenue minus Segment Adj. EBITDAR) change, H1 2026 / Q1 2026", f"{G['h1_26_cost_pct']:+.1f}% / {G['q1_26_cost_pct']:+.1f}%", "S9,S10", "derived from reported"),
 ("MGM Strip net revenue Q3 2026 / Q3 2025", f"${P['q3_26_rev']:,.1f}M / ${P['q3_25_rev']:,.1f}M ({P['q3_26_rev_pct']:+.1f}%)", "S28", "reported"),
 ("MGM Strip Segment Adj. EBITDAR Q3 2026 / Q3 2025", f"${P['q3_26_prof']:,.1f}M / ${P['q3_25_prof']:,.1f}M ({P['q3_26_prof_pct']:+.1f}%)", "S28", "reported"),
 ("MGM Strip EBITDAR margin Q3 2026 (Q3 2025)", f"{P['q3_26_margin']:.1f}% ({P['q3_25_margin']:.1f}%)", "S28", "derived from reported"),
 ("MGM Strip casino revenue Q3 2026 / Q3 2025", f"${P['q3_26_casino']:.1f}M / ${P['q3_25_casino']:.1f}M ({P['q3_26_casino_pct']:+.1f}%)", "S28", "reported (key gaming statistics)"),
 ("MGM Strip table games drop / win Q3 2026 change", f"{P['q3_26_drop_pct']:+.1f}% / {P['q3_26_tablewin_pct']:+.1f}% ($1,435M / $363M; win % 25.3% vs 22.6%)", "S28", "reported"),
 ("MGM Strip room revenue Q3 2026 / Q3 2025", f"${P['q3_26_roomrev']:.1f}M / ${P['q3_25_roomrev']:.1f}M ({P['q3_26_roomrev_pct']:+.1f}%)", "S28", "reported"),
 ("MGM Strip occupancy / ADR / RevPAR Q3 2026 (Q3 2025)", "89% (89%); $218 ($236); $193 ($210)", "S28", "reported"),
 ("Strip occupancy, average of Jul to Sep 2026", f"{K['q3_26_strip_occ']:.1f}%", "S22,S30", "derived (simple average of reported months); LVCVA survey vs company data, directional"),
 ("MGM Strip net revenue / EBITDAR, first nine months 2026 vs 2025", f"${P['n9_26_rev']:,.1f}M vs ${P['n9_25_rev']:,.1f}M ({P['n9_26_rev_pct']:+.1f}%); ${P['n9_26_prof']:,.1f}M vs ${P['n9_25_prof']:,.1f}M ({P['n9_26_prof_pct']:+.1f}%)", "S28", "reported (nine-month columns; ties to Q1 + Q2 + Q3)"),
 ("MGM Strip EBITDAR margin, first nine months 2026 (2025)", f"{G['n9_26_margin']:.1f}% ({G['n9_25_margin']:.1f}%)", "S28", "derived from reported"),
 ("MGM Strip costs (revenue minus Segment Adj. EBITDAR) change, first nine months 2026 / Q3 2026", f"{G['n9_26_cost_pct']:+.1f}% / {G['q3_26_cost_pct']:+.1f}%", "S28", "derived from reported"),
 ("MGM Strip payroll as share of revenue, first nine months 2026 (2025)", f"{G['n9_26_payroll_share']:.1f}% ({G['n9_25_payroll_share']:.1f}%); payroll ${P['n9_26_payroll']:,.1f}M vs ${P['n9_25_payroll']:,.1f}M", "S29", "derived from reported segment expense table"),
 ("MGM consolidated net revenue, first nine months 2026 / 2025", f"${P['n9_26_cons_rev']:,.1f}M ({P['n9_26_cons_pct']:+.1f}%)", "S28", "reported"),
 ("MGM China / MGM Digital net revenue change, first nine months 2026", f"{P['n9_26_china_pct']:+.1f}% / {P['n9_26_digital_pct']:+.1f}%; MGM China record quarterly revenue and 17.1% market share in Q3", "S28", "derived from reported nine-month columns"),
 ("MGM share of BetMGM operating income, first nine months 2026 / 2025", f"${P['n9_26_betmgm']:.1f}M / ${P['n9_25_betmgm']:.1f}M", "S9,S10,S28", "derived (sum of reported quarters)"),
 ("Convention vs leisure visitor spend per trip premium 2025", f"{G['conv_spend_premium_pct']:.0f}%", "S26", "derived from reported"),
]
lines = ["# Sources", "", "All figures come from primary public sources I pulled and checked on **October 24, 2026**, refreshed with Q3 2026 results on **October 29, 2026**: SEC EDGAR filings (Form 10-K and 8-K earnings releases), the Nevada Gaming Control Board (NGCB), and the Las Vegas Convention and Visitors Authority (LVCVA).",
         "Every row in `data/*.csv` has a `source_id` that maps to this table. Recommendations are based on reported KPIs only; the dashboard gives no dollar impact estimates.", "",
         "## Source list", "", "| ID | Source | URL |", "|---|---|---|"]
lines += [f"| {k} | {v[0]} | {v[1]} |" for k, v in S.items()]
lines += ["", "## Figure register", "", "| Figure | Value | Source ID(s) | Type |", "|---|---|---|---|"]
for name, val, sid, typ in R:
    lines.append(f"| {name} | {val} | {sid} | {typ} |")
lines += ["", "## Notes and items not verified", "",
 "- **Caesars ADR / RevPAR** for Las Vegas are not disclosed in its 10-K or earnings releases; only hotel occupancy is reported. Caesars is used only as a benchmark (revenue, labor and profit change).",
 "- **MGM Digital vs BetMGM.** MGM's FY2025 10-K (S2, Item 1, Segments) says: \"MGM Digital is our consolidated online gaming portfolio which is primarily comprised of LeoVegas\" (acquired September 7, 2022). BetMGM North America Venture is a 50/50 venture with Entain, accounted for under the equity method (\"Corporate and Other ... our investments in unconsolidated affiliates are primarily comprised of our ventures, such as BetMGM North America Venture\"), so its revenue is not in MGM Digital. Neither is part of the Strip analysis.",
 "- **Midweek vs weekend occupancy** is LVCVA's market-wide figure (all Las Vegas), not company data. Neither MGM nor Caesars discloses it.",
 "- **Property-level results** (for example Luxor and Excalibur EBITDAR) are not disclosed in filings. The value-tier sizing uses 10-K room counts only.",
 "- **Profit measures differ.** MGM's Segment Adjusted EBITDAR is before triple-net lease rent. Caesars' Adjusted EBITDA is after rent. Compare trends, not margin levels.",
 "- **LVCVA revisions.** The 2025 file used here is the August 20, 2026 revision (for example, Strip ADR $197.45 vs $196.54 in the January 2026 release). LVCVA hotel metrics are survey-based (more than 75% of inventory).",
 "- **2024 Strip gaming win** is taken from the LVCVA 2024 summary ($8,812.5M), which compiles NGCB data. The NGCB December 2025 report's +0.03% change ties to it.",
 "- **Q3 2026.** MGM reported third quarter 2026 results on October 28, 2026 (S28, S29). The LVCVA September 2026 workbook could not be downloaded on October 29, 2026, so the market charts and midweek and weekend occupancy stay on January to August 2026 (S22); only September Strip occupancy (80.1%, S30) is used, for the Q3 Strip average.",
 "- **Canada visitor counts** and **the 'Luxor/Excalibur ~6% of Las Vegas EBITDAR'** figure appear in press coverage and earnings-call transcripts, not in the primary sources above, so I left them out.",
]

# Neutral peer framing: peers appear only in the Company tab revenue view.
import re as _re
PEER_NOTE = "- **Peers.** Caesars and Wynn Resorts appear only in one neutral company revenue view on the Company tab (FY2025: MGM $17.54B, Caesars $11.49B, Wynn Resorts $7.14B, each from its Form 10-K). Caesars filings also feed a few benchmark rows in the data files that the dashboard does not display."
COMPANY_TAB = """
## Company tab (fetched October 24, 2026, updated October 29, 2026)

| Figure | Value | Source |
|---|---|---|
| Employees, Dec 31 2025 | About 78,000 (44,000 full time and 18,000 part time in the US, 16,000 international) | MGM Form 10-K FY2025 (S2) |
| Las Vegas Strip resorts / segments | 9 resorts / 4 segments | S2 |
| Company revenue 2023 / 2024 / 2025 | $16,164M / $17,241M / $17,538M | MGM Form 10-K (SEC XBRL) |
| Peer company revenue 2025 | Caesars $11,486M; Wynn Resorts $7,138M | Caesars and Wynn Resorts Form 10-K FY2025 |
| MGM Osaka construction start | April 24 2025, opening planned around autumn 2030 | https://mgmosaka.co.jp/news_en/2025/04/24/commencement-of-construction-work-on-the-osaka-ir-japanese-only/ |
| BetMGM Q3 2026 net revenue | $710M, up 7% | https://investors.mgmresorts.com/2026-10-13-BETMGM-Q3-2026-BUSINESS-UPDATE |
| Q3 2026 results | Revenue $4.2B; MGM China record quarterly revenue and 17.1% market share; BetMGM distributions and license fees to MGM $34M | S28 |
| Four Sixes Ranch Steakhouse at MGM Grand | Announced Oct 22 2026, opening early 2027 | https://investors.mgmresorts.com/news-releases |
| Las Vegas Grand Prix race week | Nov 19 to 21 2026, MGM Zone at Bellagio, Aria and other Strip resorts | https://investors.mgmresorts.com/news-releases |
| Share price | Yahoo Finance daily closes, Oct 30 2025 to Oct 29 2026 | Yahoo Finance |
"""
def _neutral(text):
    out = []
    for line in text.split("\n"):
        if _re.match(r"\| (Caesars|Decremental margin)", line):
            continue
        if "Caesars ADR / RevPAR" in line:
            line = PEER_NOTE
        if "**Profit measures differ.**" in line:
            continue
        out.append(line.replace(" pts", " percentage points").replace("H1 2026", "first half 2026").replace("H1 2025", "first half 2025"))
    text = "\n".join(out)
    return text.replace("\n## Notes and items not verified", COMPANY_TAB + "\n## Notes and items not verified", 1)
(ROOT / "SOURCES.md").write_text(_neutral("\n".join(lines)) + "\n")
(ROOT / "data" / "sources.csv").write_text("source_id,title,url\n" + "\n".join(f'{k},"{v[0]}",{v[1]}' for k, v in S.items()) + "\n")
print("wrote SOURCES.md", len(R), "figures")
