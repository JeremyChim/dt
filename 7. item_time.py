times = ["0:00", "5:00", "10:00", "15:00", "20:00", "25:00"]

with open("npc/neutral_items.txt") as f:
    lines = f.readlines()

new_lines = []
x = 0
for i, line in enumerate(lines, 1):
    if 'madstone_no_limit_time' in line:
        val = line.split('"')[3]
        new_val = times[-1]
        line = line.replace(val, new_val)
        print(i, line, end="")
    if 'start_time' in line:
        val = line.split('"')[3]
        new_val = times[x]
        line = line.replace(val, new_val)
        print(i, line, end="")
        x += 1
    new_lines.append(line)

with open("vpk/pak01_dir/scripts/npc/neutral_items.txt", "w") as f:
    f.writelines(new_lines)

input("...")