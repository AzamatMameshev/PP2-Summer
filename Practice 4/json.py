import json

with open("sample-data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Interface Status")
print("=" * 70)
print(f"{'DN':50} {'Speed':10} {'MTU':5}")
print("-" * 70)

for item in data["imdata"]:
    attrs = item["l1PhysIf"]["attributes"]
    dn = attrs.get("dn", "")
    speed = attrs.get("speed", "")
    mtu = attrs.get("mtu", "")
    print(f"{dn:50} {speed:10} {mtu:5}")
    