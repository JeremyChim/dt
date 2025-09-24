reset = False  # 是否重置
path = r"E:\GAME\steamapps\common\dota 2 beta\game\dota\gameinfo_branchspecific.gi"

# 读取文件
if reset:
    with open("gi/gameinfo_branchspecific2.gi", encoding='utf-8') as f:  # 新的gameinfo_branchspecific.gi
        lines = f.readlines()
else:
    with open("gi/gameinfo_branchspecific.gi", encoding='utf-8') as f:  # 旧的gameinfo_branchspecific.gi
        lines = f.readlines()

new_lines = []
for i, line in enumerate(lines, 1):
    new_lines.append(line)

# 写入文件
with open(path, "w", encoding='utf-8') as f:
    f.writelines(new_lines)
