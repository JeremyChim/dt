with open("lua/general.lua", encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines, 1):
    new_lines.append(line)

with open("general.lua", "w", encoding='utf-8') as f:
    f.writelines(new_lines)
