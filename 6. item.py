with open("npc/items.txt") as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines, 1):
    if i == 6096:  # "ItemInitialStockTime"			"990.0"
        line = line.replace("990.0", "0.0")
    new_lines.append(line)

with open("vpk/pak01_dir/scripts/npc/items.txt", "w") as f:
    f.writelines(new_lines)
