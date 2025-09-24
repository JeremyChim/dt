mul = 2

with open("npc/npc_units.txt") as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines, 1):
    if "BountyXP" in line or "BountyGoldMin" in line or "BountyGoldMax" in line:
        val = line.split('"')[3]
        new_val = int(val) * mul
        line = line.replace(val, str(new_val))
        print(i, line, end="")
    new_lines.append(line)

with open("vpk/pak01_dir/scripts/npc/npc_units.txt", "w") as f:
    f.writelines(new_lines)
