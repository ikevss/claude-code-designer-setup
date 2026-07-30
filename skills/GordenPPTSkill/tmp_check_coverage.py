import json

# Read template detail
d = json.load(open(r"C:\Users\EDY\.claude\skills\GordenPPTSkill\templates\report-massive-charts\detail.json"))

# Read current edits
master = json.load(open(r"C:\Users\EDY\.claude\skills\GordenPPTSkill\_tmp_edits_master.json"))

# Build set of already-edited (slide, slot_id) pairs
edited = set()
for e in master["edits"]:
    edited.add((e["slide"], e["slot_id"]))

# For each selected slide, find editable slots and check coverage
slides = master["selected_slides"]
missing_by_slide = {}

for p in d["pages"]:
    sn = p["slide_number"]
    if sn not in slides:
        continue
    missing = []
    for s in p.get("text_slots", []):
        if not s.get("editable"):
            continue
        if (sn, s["slot_id"]) not in edited:
            missing.append({
                "slot_id": s["slot_id"],
                "role": s.get("role", ""),
                "max_chars": s.get("max_chars"),
                "current": s.get("current_text", "")[:60]
            })
    if missing:
        missing_by_slide[sn] = missing

print("Slides with missing slots:", len(missing_by_slide))
for sn, ms in missing_by_slide.items():
    print("  slide %d: %d missing" % (sn, len(ms)))
