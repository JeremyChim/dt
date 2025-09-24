friend = ["friend2", "friend3", "friend4", "friend5"]
enemy = ["enemy1", "enemy2", "enemy3", "enemy4", "enemy5"]

with open("lua/general.lua", encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
x = 0
y = 0
for i, line in enumerate(lines, 1):
    if 49 <= i <= 52:
        val = line.split("'")[1]
        new_val = friend[x]
        line = line.replace(val, new_val)
        x += 1
        print(line, end="")
    if 57 <= i <= 61:
        val = line.split("'")[1]
        new_val = enemy[y]
        line = line.replace(val, new_val)
        y += 1
        print(line, end="")
    new_lines.append(line)

with open("general.lua", "w", encoding='utf-8') as f:
    f.writelines(new_lines)
