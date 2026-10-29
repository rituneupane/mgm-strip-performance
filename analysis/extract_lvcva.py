"""Extract Las Vegas indicators from the LVCVA Year-End / YTD summary workbooks in data/raw/.
Writes data/lvcva_annual.csv and data/lvcva_monthly.csv. Values are copied as published (no modeling)."""
import openpyxl, datetime, csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
FILES = {2019: ("lvcva_ye2019.xlsx", "S21"), 2022: ("lvcva_ye2022.xlsx", "S20"), 2023: ("lvcva_ye2023.xlsx", "S19"),
         2024: ("lvcva_ye2024.xlsx", "S18"), 2025: ("lvcva_ye2025.xlsx", "S17"), 2026: ("lvcva_ytd2026.xlsx", "S22")}
KEEP = {"Visitor Volume": "visitor_volume", "Convention Attendance": "convention_attendance",
        "Available Room Inventory": "room_inventory", "Strip Occupancy": "strip_occupancy",
        "Weekend Occupancy": "weekend_occupancy", "Midweek Occupancy": "midweek_occupancy",
        "Total Occupancy": "total_occupancy", "Strip ADR": "strip_adr", "Strip RevPAR": "strip_revpar",
        "Total Room Nights Occupied": "room_nights_occupied", "Total En/Deplaned Passengers": "airport_passengers",
        "Gaming Revenue: Las Vegas Strip": "strip_gaming_win_usd"}

def read(path):
    ws = openpyxl.load_workbook(path, data_only=True).worksheets[0]
    hdr, out = None, {}
    for r in ws.iter_rows(values_only=True):
        if not r or not isinstance(r[0], str):
            continue
        name = r[0].strip()
        if name == "Tourism Indicators":
            hdr = {i: (c.strftime("%Y-%m") if isinstance(c, datetime.datetime) else str(c)) for i, c in enumerate(r) if c is not None and i > 0}
            continue
        if name == "Change from Previous Year":
            break  # levels only
        if hdr and name in KEEP:
            out[KEEP[name]] = {hdr[i]: r[i] for i in hdr if i < len(r) and isinstance(r[i], (int, float))}
    return out

annual, monthly = [], []
for year, (fn, sid) in FILES.items():
    d = read(RAW / fn)
    ytd_key = f"{year} YTD"
    row = {"year": year, "period": "Jan-Aug YTD" if year == 2026 else "Full year", "source_id": sid}
    for k in KEEP.values():
        row[k] = d.get(k, {}).get(ytd_key, "")
    annual.append(row)
    if year in (2024, 2025, 2026):
        months = sorted({m for v in d.values() for m in v if m[:4].isdigit() and len(m) == 7})
        for m in months:
            mr = {"month": m, "year": int(m[:4]), "source_id": sid}
            for k in KEEP.values():
                mr[k] = d.get(k, {}).get(m, "")
            monthly.append(mr)

for name, rows in (("lvcva_annual.csv", annual), ("lvcva_monthly.csv", monthly)):
    with open(ROOT / "data" / name, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print("wrote", name, len(rows))
